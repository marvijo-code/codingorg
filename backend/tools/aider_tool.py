# backend/tools/aider_tool.py
from crewai.tools import BaseTool
import subprocess
import os  # Potentially needed later
# import asyncio  # Needed for async streaming implementation later
from pydantic import BaseModel, Field # Use Pydantic v2 BaseModel
from typing import Type, Any
# Remove v1 import: from pydantic.v1 import BaseModel, Field

# TODO: Define the input schema for the Aider tool
class AiderInputSchema(BaseModel):
    """Input schema for the Aider Tool."""
    instructions: str = Field(description="Detailed instructions for the coding task to be performed by Aider. Should include file paths if specific files need modification.")
    # project_path: str = Field(description="The root path of the project Aider should operate on.") # Might be managed globally or passed differently

class AiderTool(BaseTool):
    name: str = "Aider Coding Tool"
    description: str = (
        "A tool to interact with the Aider AI pair programming CLI. "
        "Use this tool to perform coding tasks like writing new code, modifying existing code, adding tests, or fixing bugs. "
        "Provide clear and specific instructions for the task."
    )
    args_schema: Type[BaseModel] = AiderInputSchema
    # Optional: Add attributes for configuration like Aider path, project path, model, API key if not handled globally
    # aider_path: str = "aider" # Or full path if needed
    # project_path: str = os.getcwd() # Default to current, but should be the actual project root

    # TODO: Implement the _run method to invoke Aider
    def _run(
        self,
        instructions: str,
        # project_path: str = None # Or get from self.project_path
        **kwargs: Any,
    ) -> str:
        """Synchronous execution method (required by BaseTool). Will delegate to async method."""
        # CrewAI typically runs tools in separate threads, allowing async operations
        # within the sync wrapper if needed, but direct async support might vary.
        # For simplicity, we might run the subprocess synchronously here,
        # but ideally, we want streaming output.
        # This synchronous wrapper might just kick off the async process
        # and potentially return an initial status or task ID.
        # The actual streaming would happen via the WebSocket manager.

        print(f"Aider Tool received instructions: {instructions}")

        # Determine project root directory (two levels up from backend/tools)
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        print(f"Project root determined as: {project_root}")
        # project_dir = project_path or self.project_path # Determine project directory

        # --- Placeholder for synchronous execution (replace with proper async/streaming later) ---
        try:
            # Construct the Aider command
            # Ensure AIDER_MODEL and relevant API keys (e.g., GOOGLE_API_KEY) are set as environment variables
            # Aider typically picks these up automatically.
            # We might need to explicitly pass the project context if not running from the root.
            # The command needs to be run within the project's root directory.
            aider_command = [
                "aider",  # Assuming aider is in PATH
                "--message", instructions,
                # Add other necessary aider flags if needed (e.g., --yes for auto-commit)
                # "--model", os.getenv("AIDER_MODEL", "gemini/gemini-1.5-pro-latest") # Aider might pick this from env
            ]

            print(f"Executing Aider command: {' '.join(aider_command)}")

            # Execute Aider - This blocks and captures all output at the end.
            # We need to replace this with async streaming.
            # Ensure the command runs in the correct directory (e.g., project root)
            # For now, assume execution context is correct or manage via `cwd`
            process = subprocess.run(
                aider_command,
                capture_output=True,  # Capture stdout/stderr
                text=True,  # Decode output as text
                check=True,  # Raise exception on non-zero exit code
                cwd=project_root  # <<< Run Aider in the project root directory
                # cwd=project_dir # Specify the working directory for Aider
            )

            output = process.stdout
            error_output = process.stderr
            print(f"Aider stdout:\n{output}")
            if error_output:
                print(f"Aider stderr:\n{error_output}")

            # Return the final output (or a summary)
            # Streaming will be handled separately.
            return f"Aider task completed. Output:\n{output}\n{error_output if error_output else ''}"

        except subprocess.CalledProcessError as e:
            print(f"Aider execution failed: {e}")
            print(f"Stderr: {e.stderr}")
            return f"Aider execution failed: {e}. Stderr: {e.stderr}"
        except FileNotFoundError:
            print("Error: 'aider' command not found. Make sure Aider is installed and in the system PATH.")
            return "Error: 'aider' command not found."
        except Exception as e:
            print(f"An unexpected error occurred while running Aider: {e}")
            return f"An unexpected error occurred: {e}"

    # TODO: Implement an async method for streaming output (if CrewAI/FastAPI setup allows)
    async def _arun(
        self,
        instructions: str,
        # project_path: str = None
        **kwargs: Any,
    ) -> str:
        """Asynchronous execution method for potential streaming."""
        # This is where the actual streaming logic would go, using asyncio.create_subprocess_exec
        # and reading stdout/stderr line by line, pushing updates via WebSocket manager.
        print(f"Aider Tool (async) received instructions: {instructions}")
        # Placeholder - delegate to sync version for now until streaming is implemented
        return self._run(instructions=instructions, **kwargs)


# Example usage (for testing purposes)
if __name__ == '__main__':
    from dotenv import load_dotenv
    # Load .env from the backend directory
    load_dotenv(dotenv_path='../.env')

    # Ensure Aider is installed and GOOGLE_API_KEY is set in .env
    # You might need to run `aider --model gemini/gemini-1.5-pro-latest` once manually
    # for Aider to cache model info if it hasn't been used before.

    tool = AiderTool()

    # --- Test Case 1: Simple instruction ---
    print("\n--- Test Case 1: Simple Instruction ---")
    test_instructions_1 = "Create a file named test_aider_tool.txt with the content 'Hello from Aider Tool test'."
    # Assuming the project path context is correct (e.g., running from backend/)
    # Aider needs to know where to create the file relative to the project root.
    # We might need to adjust instructions or manage CWD.
    # For this test, let's assume Aider runs in `c:/dev/codingorg`
    result_1 = tool._run(instructions=test_instructions_1)
    print(f"\nResult 1:\n{result_1}")

    # --- Test Case 2: Instruction causing potential error ---
    # print("\n--- Test Case 2: Error Instruction ---")
    # test_instructions_2 = "Modify a non-existent file non_existent_file.py"
    # result_2 = tool._run(instructions=test_instructions_2)
    # print(f"\nResult 2:\n{result_2}")

    # --- Test Case 3: Check if file was created (Manual Check) ---
    print("\n--- Manual Check ---")
    print("Check if 'test_aider_tool.txt' was created in the project root (c:/dev/codingorg).")