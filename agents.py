from crewai import Agent
import os
import time
from langchain_google_genai import ChatGoogleGenerativeAI

def create_gemini_llm():
    """Create optimized Gemini LLM with rate limiting"""
    
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY not found in environment variables")
    
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",  # More stable than 2.0-flash-exp
        verbose=True,
        temperature=0.3,
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        max_retries=5,  # Increased retries
        request_timeout=120,  # Longer timeout
        max_tokens=1024,  # Reduced token limit to stay within quota
        # Conservative rate limiting
        max_output_tokens=1024,
        candidate_count=1,
        stop_sequences=None,
        safety_settings=None,
        # Add exponential backoff
        retry_delay=2.0,
        max_retry_delay=60.0,
    )

class SmartRateLimiter:
    """Intelligent rate limiter that adapts to API responses"""
    
    def __init__(self, base_delay=3, max_delay=30, backoff_factor=1.5):
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.backoff_factor = backoff_factor
        self.current_delay = base_delay
        self.last_call_time = 0
        self.consecutive_errors = 0
    
    def wait_if_needed(self):
        """Wait based on current delay settings"""
        current_time = time.time()
        time_since_last_call = current_time - self.last_call_time
        
        if time_since_last_call < self.current_delay:
            sleep_time = self.current_delay - time_since_last_call
            print(f"🕐 Rate limiting: waiting {sleep_time:.1f} seconds...")
            time.sleep(sleep_time)
        
        self.last_call_time = time.time()
    
    def on_success(self):
        """Reset delay on successful call"""
        self.consecutive_errors = 0
        self.current_delay = max(self.base_delay, self.current_delay * 0.9)
    
    def on_error(self):
        """Increase delay on error"""
        self.consecutive_errors += 1
        self.current_delay = min(
            self.max_delay, 
            self.current_delay * self.backoff_factor
        )
        print(f"⚠️ API error detected. Increasing delay to {self.current_delay:.1f}s")

class RateLimitedGeminiLLM:
    """Wrapper for Gemini LLM with intelligent rate limiting"""
    
    def __init__(self, llm):
        self.llm = llm
        self.rate_limiter = SmartRateLimiter(base_delay=5, max_delay=60)  # Start with 5 second delay
    
    def __getattr__(self, name):
        attr = getattr(self.llm, name)
        
        # If it's a callable method (like invoke, generate, etc.)
        if callable(attr):
            def rate_limited_call(*args, **kwargs):
                max_attempts = 3
                for attempt in range(max_attempts):
                    try:
                        self.rate_limiter.wait_if_needed()
                        result = attr(*args, **kwargs)
                        self.rate_limiter.on_success()
                        return result
                    except Exception as e:
                        error_msg = str(e).lower()
                        if "429" in error_msg or "quota" in error_msg or "rate" in error_msg:
                            self.rate_limiter.on_error()
                            if attempt < max_attempts - 1:
                                print(f"🔄 Rate limit hit. Retrying attempt {attempt + 2}/{max_attempts}...")
                                time.sleep(min(30, self.rate_limiter.current_delay * 2))  # Extra wait for rate limits
                                continue
                        raise e
                raise Exception("Max retry attempts reached")
            
            return rate_limited_call
        else:
            return attr

# Initialize the rate-limited Gemini LLM
print("🤖 Initializing Gemini LLM with rate limiting...")
base_gemini_llm = create_gemini_llm()
gemini_llm = RateLimitedGeminiLLM(base_gemini_llm)

support_agent = Agent(
    role="Senior Support Representative",
    goal="Be the most friendly and helpful support representative in your team",
    backstory=(
        "You work at crewAI (https://crewai.com) and are now working on providing "
        "support to {customer}, a super important customer for your company. "
        "You need to make sure that you provide the best support! "
        "Make sure to provide full complete answers, and make no assumptions. "
        "You have access to documentation scraping tools to help you find accurate "
        "information to assist customers with their inquiries."
    ),
    allow_delegation=False,
    verbose=True,
    llm=gemini_llm
)

support_quality_assurance_agent = Agent(
    role="Support Quality Assurance Specialist",
    goal="Get recognition for providing the best support quality assurance in your team",
    backstory=(
        "You work at crewAI (https://crewai.com) and are now working with your team "
        "on a request from {customer} ensuring that the support representative is "
        "providing the best support possible.\n"
        "You need to make sure that the support representative is providing full "
        "complete answers, and make no assumptions. Your job is to review responses "
        "for accuracy, completeness, and tone before they go to the customer."
    ),
    verbose=True,
    llm=gemini_llm
)