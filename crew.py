from crewai import Crew, Process
from agents import support_agent, support_quality_assurance_agent
from tasks import inquiry_resolution, quality_assurance_review

# Create the crew
support_crew = Crew(
    agents=[support_agent, support_quality_assurance_agent],
    tasks=[inquiry_resolution, quality_assurance_review],
    process=Process.sequential,
    verbose=2,
    memory=True,
    embedder={
        "provider": "google",
        "config": {
            "model": "models/embedding-001",
            "task_type": "retrieval_document",
        }
    }
)

def run_support_crew(customer: str, person: str, inquiry: str):
    """
    Run the support crew to handle customer inquiries.
    
    Args:
        customer: Name of the customer company
        person: Name of the person who reached out
        inquiry: The customer's inquiry or question
        
    Returns:
        The final response from the quality assurance review
    """
    inputs = {
        'customer': customer,
        'person': person,
        'inquiry': inquiry
    }
    
    result = support_crew.kickoff(inputs=inputs)
    return result

if __name__ == "__main__":
    # Example usage
    result = run_support_crew(
        customer="TechCorp Inc",
        person="John Smith",
        inquiry="I'm having trouble setting up agents with custom tools in CrewAI. Can you help me understand the proper way to implement this?"
    )
    
    print("Final Response:")
    print(result)