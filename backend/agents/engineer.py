# backend/agents/engineer.py
from crewai import Agent
# Note: The primary LLM interaction for coding will happen via the Aider tool.
# This agent definition might not need its own LLM instance directly,
# unless it needs to perform non-coding tasks or communicate complex reasoning.
# For now, we'll define it without a direct LLM, assuming the Crew/Flow handles
# passing tasks to its tool.

# Placeholder for the agent definition
senior_engineer_agent = None

def get_senior_engineer_agent(aider_tool):
    """Initializes and returns the Senior Software Engineer Agent."""
    global senior_engineer_agent
    if senior_engineer_agent is None:
        senior_engineer_agent = Agent(
            role='Senior Software Engineer',
            goal='Take development tasks, implement them using the Aider tool, write high-quality code and tests, ensure test coverage targets are met, and report results.',
            backstory=(
                "You are a highly skilled Senior Software Engineer specialized in using AI tools for development. "
                "You receive tasks from the Development Manager and utilize the Aider tool to write, modify, and test code efficiently. "
                "You are meticulous about code quality, testing (aiming for 90%+ coverage), and following instructions precisely."
            ),
            tools=[aider_tool], # Assign the custom Aider tool
            verbose=True,
            allow_delegation=False # This agent focuses on execution, not delegation
            # llm=... # Optional: Assign a simpler/faster LLM like Flash if needed for non-Aider communication
        )
        print("Senior Software Engineer Agent initialized.")
    return senior_engineer_agent

# Example usage (requires a dummy tool for testing)
if __name__ == '__main__':
    from crewai.tools import BaseTool
    from dotenv import load_dotenv

    # Define a dummy tool for testing purposes
    class DummyAiderTool(BaseTool):
        name: str = "Dummy Aider Tool"
        description: str = "A placeholder tool that simulates Aider."

        def _run(self, argument: str) -> str:
            print(f"Dummy Aider Tool received: {argument}")
            return f"Simulated Aider output for: {argument}"

    dummy_tool = DummyAiderTool()
    engineer = get_senior_engineer_agent(dummy_tool)
    print(f"Agent Role: {engineer.role}")
    # result = engineer.execute_task("Implement the '/hello' endpoint using the Aider tool.")
    # print(result) # Testing requires a Crew setup