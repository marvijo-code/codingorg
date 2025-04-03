# backend/crew/task_orchestrator.py
from crewai import Crew, Process, Task
import os
from crewai import Crew, Process, Task
# from langchain_google_genai import ChatGoogleGenerativeAI # Removed, using dict config
from backend.agents.manager import get_development_manager_agent
from backend.agents.engineer import get_senior_engineer_agent
from backend.tools.aider_tool import AiderTool
# from dotenv import load_dotenv # Removed as it's unused now

# Load environment variables (especially API keys)
# Assuming this module is run from the context where .env is accessible
# or loaded beforehand (e.g., in main.py)
# load_dotenv(dotenv_path='../.env') # Assuming .env is loaded by main.py

# TODO: Implement the main orchestration logic

class TaskOrchestrator:
    def __init__(self, websocket_manager=None):
        """
        Initializes the TaskOrchestrator.
        Args:
            websocket_manager: An instance of WebSocketManager to send updates.
        """
        self.websocket_manager = websocket_manager
        self.aider_tool = AiderTool()  # Initialize the Aider tool
        self.manager_agent = get_development_manager_agent()
        self.engineer_agent = get_senior_engineer_agent(self.aider_tool)
        # TODO: Initialize Utility Agent if needed

        # LLM config will be set directly on the agent

    def run_crew(self, user_prompt: str):
        """
        Sets up and runs the CrewAI crew based on the user prompt.
        Args:
            user_prompt: The initial requirement or task from the user.
        Returns:
            The result of the crew execution.
        """
        print(f"Orchestrator received prompt: {user_prompt}")
        if not os.getenv("GOOGLE_API_KEY"):
            error_msg = "GOOGLE_API_KEY not found. Cannot run crew."
            print(error_msg)
            # Send error back via WebSocket if manager exists
            if self.websocket_manager:
                # Assuming websocket_manager has a method like broadcast_message
                # self.websocket_manager.broadcast_message({"type": "error", "message": error_msg})
                pass  # Implement actual WebSocket sending
            return error_msg

        # --- Define Tasks ---
        # Task for the Manager: Break down the user prompt
        task_plan = Task(
            description=(
                f"Analyze the user requirement: '{user_prompt}'. Break it down into specific, "
                "actionable technical steps for the Senior Software Engineer. "
                "Define the expected output or changes for each step. "
                "Delegate the first implementation step to the Senior Software Engineer."
            ),
            expected_output="A clear, step-by-step technical plan and delegation of the first coding task to the Senior Software Engineer.",
            agent=self.manager_agent
        )

        # Task for the Engineer: Implement based on Manager's plan (example structure)
        # This will likely be dynamically created or managed within a Flow
        task_implement = Task(
            description=(
                "Receive the technical plan and specific task from the Development Manager. "
                "Use the Aider Coding Tool to implement the assigned task. "
                "Ensure you write necessary tests to meet the 90% coverage goal. "
                "Report the results, including any code changes or errors, back to the Development Manager."
            ),
            expected_output="Completed code changes, test results, and a status report including any issues encountered.",
            agent=self.engineer_agent,
            tools=[self.aider_tool],
            context=[task_plan]  # Depends on the output of the planning task
        )

        # Task for the Manager: Review the implementation (example structure)
        task_review = Task(
            description=(
                "Review the code changes and test results provided by the Senior Software Engineer. "
                "Verify if the implementation meets the requirements of the assigned task and the overall user prompt. "
                "Provide feedback or request revisions if necessary. If satisfied, prepare a summary for the user."
            ),
            expected_output="A review summary, potentially including feedback for the engineer or a final report for the user.",
            agent=self.manager_agent,
            context=[task_implement]  # Depends on the output of the implementation task
        )

        # --- Create and Run Crew ---
        # This is a simplified sequential example. CrewAI Flows might be better for complex logic.
        crew = Crew(
            agents=[self.manager_agent, self.engineer_agent],
            tasks=[task_plan, task_implement, task_review],
            process=Process.sequential,  # Start with sequential, consider hierarchical or Flows later
            verbose=True,  # Provides detailed logs (Added comma)
            # memory=True # Enable memory for context across tasks if needed
            # llm=... # Removed central LLM config
            # manager_llm=... # Can specify a different LLM for the crew manager itself if using hierarchical
        )

        print("Starting crew execution...")
        try:
            # TODO: Integrate WebSocket streaming for agent thoughts/actions here
            # CrewAI's `kickoff` is blocking. Need to investigate callbacks or custom loops for streaming.
            result = crew.kickoff()
            print("Crew execution finished.")
            print(f"Final Result:\n{result}")

            # Send final result via WebSocket
            if self.websocket_manager:
                # self.websocket_manager.broadcast_message({"type": "final_result", "data": result})
                pass  # Implement actual WebSocket sending

            return result
        except Exception as e:
            error_msg = f"An error occurred during crew execution: {e}"
            print(error_msg)
            if self.websocket_manager:
                # self.websocket_manager.broadcast_message({"type": "error", "message": error_msg})
                pass  # Implement actual WebSocket sending
            return error_msg

# Example usage (for testing purposes)
if __name__ == '__main__':
    # Ensure GOOGLE_API_KEY is set in backend/.env
    orchestrator = TaskOrchestrator()
    test_prompt = "Create a simple Python script in the root directory named 'hello.py' that prints 'Hello, CrewAI!'."
    final_result = orchestrator.run_crew(test_prompt)
    print("\n--- Orchestrator Test Run Complete ---")
    # print(f"Final output received by main script:\n{final_result}")