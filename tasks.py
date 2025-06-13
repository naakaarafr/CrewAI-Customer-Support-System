from crewai import Task
from agents import support_agent, support_quality_assurance_agent

# Try to import custom tool, fallback to built-in tools if it fails
try:
    from tools import docs_scrape_tool
    available_tools = [docs_scrape_tool]
except Exception as e:
    print(f"Custom tool import failed: {e}")
    print("Falling back to built-in CrewAI tools...")
    from crewai_tools import WebsiteSearchTool, ScrapeWebsiteTool
    website_search_tool = WebsiteSearchTool()
    scrape_website_tool = ScrapeWebsiteTool()
    available_tools = [website_search_tool, scrape_website_tool]

inquiry_resolution = Task(
    description=(
        "{customer} just reached out with a super important ask:\n"
        "{inquiry}\n\n"
        "{person} from {customer} is the one that reached out. "
        "Make sure to use everything you know to provide the best support possible. "
        "You must strive to provide a complete and accurate response to the customer's inquiry. "
        "Use the available web scraping and search tools to find relevant information from official sources "
        "like https://docs.crewai.com or other relevant documentation pages. "
        "Always verify your information and provide references to sources when possible."
    ),
    expected_output=(
        "A detailed, informative response to the customer's inquiry that addresses "
        "all aspects of their question.\n"
        "The response should include references to everything you used to find the answer, "
        "including external data or solutions. "
        "Ensure the answer is complete, leaving no questions unanswered, and maintain "
        "a helpful and friendly tone throughout. "
        "Include specific examples or code snippets where applicable."
    ),
    tools=available_tools,
    agent=support_agent,
)

quality_assurance_review = Task(
    description=(
        "Review the response drafted by the Senior Support Representative for {customer}'s inquiry. "
        "Ensure that the answer is comprehensive, accurate, and adheres to the "
        "high-quality standards expected for customer support.\n"
        "Verify that all parts of the customer's inquiry have been addressed "
        "thoroughly, with a helpful and friendly tone.\n"
        "Check for references and sources used to find the information, "
        "ensuring the response is well-supported and leaves no questions unanswered. "
        "Make sure the response is technically accurate and provides actionable solutions."
    ),
    expected_output=(
        "A final, detailed, and informative response ready to be sent to the customer.\n"
        "This response should fully address the customer's inquiry, incorporating all "
        "relevant feedback and improvements.\n"
        "Don't be too formal, we are a chill and cool company "
        "but maintain a professional and friendly tone throughout. "
        "Ensure the response includes clear next steps or solutions for the customer."
    ),
    agent=support_quality_assurance_agent,
)