# AI Chatbot Orchestrator Architecture Plan

This document outlines the plan for creating an AI Chatbot that orchestrates an AI Software Development team using CrewAI.

## 1. Goals

*   Develop a chatbot interface (Web UI) for users to submit software development requests via text prompts.
*   Implement a backend using CrewAI to manage a team of AI agents.
*   Define initial agent roles: Development Manager and Senior Software Engineer.
*   Integrate Aider as a custom CrewAI tool for the Senior Software Engineer to perform coding tasks.
*   Utilize specific LLMs for different roles (Gemini 2.5 Pro Experimental for Manager/Engineer, Gemini 2.0 Flash for summarization/utility tasks).
*   Stream CrewAI agent outputs (thoughts, actions) and Aider logs (text, diffs) to the frontend in real-time.
*   Set up the project using `uv` for environment management.
*   Build the frontend using Vite + React.
*   Ensure the architecture supports parallel task execution for future scalability.
*   Implement an error handling strategy (retry then ask user).
*   Aim for high unit and integration test coverage (90% minimum) for the generated code (enforced via Aider prompts/checks).

## 2. Technology Stack

*   **Environment Management:** `uv`
*   **Backend Framework:** FastAPI (Python) - To serve the API and handle WebSocket/SSE connections.
*   **AI Orchestration:** CrewAI &amp; CrewAI Flows (Python)
*   **Coding Tool:** Aider (Python, integrated as a CrewAI tool)
*   **Frontend Framework:** Vite + React (TypeScript/JavaScript)
*   **Real-time Communication:** WebSockets or Server-Sent Events (SSE)
*   **LLMs:** Google Gemini API (2.5 Pro Experimental, 2.0 Flash)

## 3. Architecture Overview

```mermaid
graph TD
    subgraph User Interface (Vite + React)
        UI[Web Chat Interface]
    end

    subgraph Backend (FastAPI + CrewAI)
        API[FastAPI App]
        WS[WebSocket/SSE Endpoint]
        Orchestrator[Chatbot Orchestrator]
        CrewManager[CrewAI Manager]
        subgraph CrewAI Team
            DevManagerAgent[Development Manager Agent (Gemini 2.5 Pro)]
            SeniorEngineerAgent[Senior Software Engineer Agent (Gemini 2.5 Pro)]
            AiderTool[Custom Aider Tool Wrapper]
            UtilityAgent[Utility Agent (Gemini 2.0 Flash)]
        end
        AiderCLI[Aider CLI Process]
    end

    subgraph External Services
        LLM_API[LLM APIs (Google Gemini)]
    end

    UI -- User Request --> API
    API -- Initiate Task --> Orchestrator
    Orchestrator -- Create/Run Crew --> CrewManager
    CrewManager -- Assign Task --> DevManagerAgent
    DevManagerAgent -- Delegate Coding Task --> SeniorEngineerAgent
    SeniorEngineerAgent -- Use Tool --> AiderTool
    AiderTool -- Execute Command --> AiderCLI
    AiderCLI -- Interact With --> LLM_API
    AiderCLI -- Code Changes/Logs --> AiderTool
    AiderTool -- Results/Logs --> SeniorEngineerAgent
    SeniorEngineerAgent -- Report Status/Code --> DevManagerAgent
    DevManagerAgent -- Report Progress --> CrewManager
    CrewManager -- Stream Outputs --> WS
    AiderTool -- Stream Aider Logs --> WS
    WS -- Real-time Updates --> UI

    DevManagerAgent -- Use Utility --> UtilityAgent
    UtilityAgent -- Interact With --> LLM_API
    UtilityAgent -- Summarized Info --> DevManagerAgent

    %% LLM Interactions
    DevManagerAgent -- Interact With --> LLM_API
    SeniorEngineerAgent -- Interact With --> LLM_API
```

## 4. Key Components &amp; Workflow

1.  **User Interface (Vite + React):**
    *   Provides a chat input for users to describe software requirements.
    *   Establishes a WebSocket/SSE connection to the backend for real-time updates.
    *   Displays streamed logs from CrewAI agents (thoughts, actions) and Aider (text, diffs).
    *   Renders the final output/status of the development task.

2.  **Backend (FastAPI):**
    *   Provides an API endpoint to receive user requests.
    *   Manages WebSocket/SSE connections for streaming updates to the UI.
    *   Hosts the Chatbot Orchestrator logic.

3.  **Chatbot Orchestrator:**
    *   Receives the user's request from the API.
    *   Initializes the CrewAI Manager with the defined agents and tasks based on the request.
    *   Handles the overall lifecycle of the development task.
    *   Manages error handling (retries, user prompts).

4.  **CrewAI Manager (CrewAI Flows):**
    *   Configures and runs the CrewAI team (Crew or Flow).
    *   Defines the overall workflow and task delegation.
    *   Manages agent execution, potentially in parallel.
    *   Collects and streams agent outputs via the WebSocket/SSE endpoint.

5.  **Agents (CrewAI):**
    *   **Development Manager:**
        *   LLM: Gemini 2.5 Pro.
        *   Role: Understands user requirements, breaks them down into actionable tasks, assigns tasks to the engineer, reviews code/results, manages the overall development process.
        *   Tools: Potentially uses the Utility Agent for summarization.
    *   **Senior Software Engineer:**
        *   LLM: Gemini 2.5 Pro (via Aider configuration).
        *   Role: Takes tasks from the Manager, uses the Aider tool to write/modify code and tests, ensures code quality and test coverage.
        *   Tools: Custom Aider Tool.
    *   **Utility Agent (Optional but Recommended):**
        *   LLM: Gemini 2.0 Flash.
        *   Role: Performs smaller, focused tasks like summarizing long logs or test results before presenting them to other agents or the user.
        *   Tools: Basic text processing tools.

6.  **Custom Aider Tool (Python Wrapper):**
    *   A CrewAI tool specifically for the Senior Engineer Agent.
    *   Takes coding instructions (e.g., "Implement function X", "Fix bug Y", "Add tests for Z") as input.
    *   Uses Python's `subprocess` or similar to invoke the Aider CLI programmatically (`aider --message "instruction"`).
    *   Configures Aider to use the appropriate LLM (Gemini 2.5 Pro Exp) and API keys.
    *   Captures Aider's stdout/stderr in real-time.
    *   Parses Aider's output to extract logs, code diffs, and status updates.
    *   Streams these parsed outputs back to the CrewAI Manager/WebSocket endpoint.
    *   Handles Aider process management and error reporting.
    *   Ensures Aider operates within the correct project context/directory.

7.  **Aider CLI Process:**
    *   The actual Aider executable run by the wrapper tool.
    *   Interacts with the specified LLM (Gemini 2.5 Pro) via its API.
    *   Applies code changes directly to the filesystem within the project structure.
    *   Generates logs and diffs streamed to stdout/stderr.

## 5. Implementation Details

*   **Project Setup:** Use `uv init` and `uv pip install ...` to manage dependencies in a local virtual environment.
*   **Configuration:** Store API keys and LLM model names securely (e.g., environment variables, `.env` file).
*   **Streaming:** Implement robust WebSocket/SSE handling in FastAPI and React to manage real-time updates effectively. Structure the streamed messages clearly (e.g., JSON objects with `type: 'agent_log'`, `type: 'aider_log'`, `source: 'agent_name'`, `content: {...}`).
*   **Aider Integration:** The custom tool wrapper is critical. It needs to handle starting/stopping the Aider process, feeding it instructions, and continuously reading/parsing its output stream. Error handling for Aider failures (e.g., LLM errors, file access issues) is important.
*   **Parallelism:** Design CrewAI Flows to allow the Manager and Engineer agents to potentially work on different sub-tasks concurrently where appropriate.
*   **Testing:** Define prompts for Aider that explicitly require writing unit and integration tests to meet the 90% coverage goal. Potentially add a separate step/agent to run tests and report coverage after Aider completes its work.

## 6. Next Steps

*   Set up the initial project structure (`uv`, FastAPI, Vite/React).
*   Implement the basic FastAPI backend with WebSocket/SSE support.
*   Develop the core CrewAI agent definitions (Manager, Engineer).
*   Build and test the Custom Aider Tool wrapper.
*   Integrate the tool into the Engineer agent.
*   Develop the basic React frontend for chat input and log display.
*   Implement the Orchestrator logic to tie user requests to CrewAI execution.
*   Refine error handling and streaming mechanisms.
*   Add testing and validation steps.