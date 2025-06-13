from crewai_tools import tool
from pydantic import BaseModel, Field
import requests
from bs4 import BeautifulSoup
import time
import random

class RateLimitedScraper:
    """Rate limiter for web scraping to avoid overwhelming servers"""
    
    def __init__(self, min_delay=2, max_delay=5):
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.last_request_time = 0
    
    def wait_if_needed(self):
        """Add random delay between requests"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        # Random delay to avoid predictable patterns
        delay = random.uniform(self.min_delay, self.max_delay)
        
        if time_since_last < delay:
            sleep_time = delay - time_since_last
            print(f"🕐 Scraping rate limit: waiting {sleep_time:.1f} seconds...")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()

# Global rate limiter instance
scraper_limiter = RateLimitedScraper(min_delay=3, max_delay=6)

@tool("Documentation Scraper")
def docs_scrape_tool(url: str) -> str:
    """
    Scrape content from a documentation URL to extract relevant information.
    Useful for finding answers to customer inquiries by searching through
    official documentation and help pages.
    
    Args:
        url: The URL of the documentation page to scrape
        
    Returns:
        The scraped text content from the page
    """
    try:
        # Apply rate limiting
        scraper_limiter.wait_if_needed()
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        # Longer timeout and retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.get(
                    url, 
                    headers=headers, 
                    timeout=20,  # Increased timeout
                    allow_redirects=True
                )
                response.raise_for_status()
                break
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 2
                    print(f"🔄 Scraping attempt {attempt + 1} failed, retrying in {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                else:
                    return f"Error scraping {url} after {max_retries} attempts: {str(e)}"
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script, style, and other non-content elements
        for element in soup(["script", "style", "nav", "header", "footer", "aside"]):
            element.decompose()
        
        # Focus on main content areas
        main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content') or soup
        
        # Extract text content
        text = main_content.get_text()
        
        # Clean up the text more thoroughly
        lines = []
        for line in text.splitlines():
            cleaned_line = line.strip()
            if cleaned_line and len(cleaned_line) > 3:  # Skip very short lines
                lines.append(cleaned_line)
        
        # Join lines and clean up extra spaces
        text = ' '.join(lines)
        text = ' '.join(text.split())  # Normalize whitespace
        
        # Limit response length to avoid token limits (be more conservative)
        max_length = 3000  # Reduced from 4000
        if len(text) > max_length:
            # Try to cut at a sentence boundary
            truncated = text[:max_length]
            last_period = truncated.rfind('.')
            if last_period > max_length * 0.8:  # If we can find a good cutoff point
                text = truncated[:last_period + 1]
            else:
                text = truncated
            text += "\n\n[Content truncated to stay within limits]"
        
        return f"Successfully scraped content from {url}:\n\n{text}"
        
    except Exception as e:
        return f"Unexpected error while scraping {url}: {str(e)}"