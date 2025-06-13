#!/usr/bin/env python3
"""
CrewAI Customer Support System
A multi-agent system for handling customer support inquiries using Gemini 2.0
"""

import os
from dotenv import load_dotenv
from crew import run_support_crew

# Load environment variables
load_dotenv()

def main():
    """Main function to run the customer support system."""
    
    # Check if Google API key is set
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY not found in environment variables.")
        print("Please set your Google API key in the .env file.")
        return
    
    print("🤖 CrewAI Customer Support System")
    print("=" * 50)
    
    # Get customer information
    customer = input("Enter customer company name: ").strip()
    if not customer:
        customer = "Valued Customer"
    
    person = input("Enter contact person's name: ").strip()
    if not person:
        person = "Customer Representative"
    
    print("\nEnter the customer inquiry (press Enter twice to finish):")
    inquiry_lines = []
    while True:
        line = input()
        if line == "" and inquiry_lines:
            break
        if line != "":
            inquiry_lines.append(line)
    
    inquiry = "\n".join(inquiry_lines)
    
    if not inquiry.strip():
        print("❌ No inquiry provided. Exiting.")
        return
    
    print(f"\n🔄 Processing inquiry from {person} at {customer}...")
    print("-" * 50)
    
    try:
        # Run the support crew
        result = run_support_crew(
            customer=customer,
            person=person,
            inquiry=inquiry
        )
        
        print("\n✅ Support Response Generated!")
        print("=" * 50)
        print(result)
        
    except Exception as e:
        print(f"❌ Error processing inquiry: {str(e)}")
        print("Please check your API key and internet connection.")

if __name__ == "__main__":
    main()