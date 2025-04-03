# backend/agents/manager.py
from crewai import Agent
import os
from langchain_google_genai import ChatGoogleGenerativeAI  # Needed for Crew LLM config

# TODO: Configure LLM (e.g., Gemini 1.5 Pro) using environment variables
# llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", google_api_key=os.getenv("GOOGLE_API_KEY"))

# Placeholder for the agent definition
development_manager_agent = None

def get_development_manager_agent():
    """Initializes and returns the Development Manager Agent."""
    global development_manager_agent
    if development_manager_agent is None:
        # LLM config will be picked up by CrewAI default mechanism using GEMINI_API_KEY env var
        development_manager_agent = Agent(
            role='Development Manager',
            goal='Oversee the software development process from requirements to deployment, ensuring tasks are well-defined, assigned correctly to the Senior Software Engineer, and meet user requirements.',
            backstory=(
                "You are an experienced Development Manager, skilled in breaking down complex software requirements "
                "into actionable, specific, and testable tasks for your Senior Software Engineer. You excel at communication, coordination, "
                "reviewing the engineer's work, and ensuring the final product aligns perfectly with the user's needs and quality standards. "
                "You always ensure the engineer has clear instructions and context."
            ),
            # llm=... # Removed agent-specific LLM config
            verbose=True,
            allow_delegation=True,  # Allow delegation specifically to the engineer agent (handled in Crew definition)
            # memory=True # Consider adding memory if needed for longer conversations
        )
        print("Development Manager Agent initialized.")
    return development_manager_agent

# Example usage (for testing purposes)
if __name__ == '__main__':
    # Example usage (for testing purposes)
    # from dotenv import load_dotenv
    # load_dotenv(dotenv_path='../.env') # Load .env from the backend directory
    # if not os.getenv("GEMINI_API_KEY"):
    #     print("Error: GEMINI_API_KEY not found.")
    # else:
    #     manager = get_development_manager_agent()
    #     print(f"Agent Role: {manager.role}")
    pass # Keep __main__ block minimal or remove for now