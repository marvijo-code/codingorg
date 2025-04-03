# System Patterns: AI Chatbot Orchestrator

## Architecture
*   **Frontend:** Vite + React (TypeScript) single-page application providing the chat interface.
*   **Backend:** FastAPI (Python) serving a REST API and WebSocket endpoint.
*   **AI Orchestration:** CrewAI framework managing agents and tasks. CrewAI Flows might be used later for more complex workflows.
*   **Real-time Communication:** WebSockets (or potentially SSE) used to stream logs and updates from the backend (CrewAI agents, Aider tool) to the frontend.
*   **Environment Management:** `uv` for Python environment and dependency management. `npm` for frontend dependencies.

## Key Technical Decisions
*   **CrewAI:** Chosen for orchestrating multiple AI agents (Development Manager, Senior Engineer).
*   **Aider:** Selected as the primary tool for code generation and modification, integrated as a custom CrewAI tool wrapping the Aider CLI/Python script interface.
*   **FastAPI:** Provides an async framework suitable for handling WebSocket connections and API requests.
*   **Vite + React:** Modern stack for building the interactive frontend.
*   **Specific LLMs:**
    *   Gemini 2.5 Pro Exp (0325) for core agent reasoning (Manager, Engineer via Aider).
    *   Gemini 2.0 Flash for utility tasks (e.g., summarization).
*   **Streaming Output:** A core requirement is to stream agent thoughts/actions and Aider logs to the frontend for transparency.
*   **High Test Coverage:** Aider will be prompted to generate tests aiming for >90% coverage.

## Data Flow
1.  User sends prompt via React UI -> WebSocket/HTTP POST to FastAPI.
2.  FastAPI `/start_task` endpoint triggers `TaskOrchestrator`.
3.  `TaskOrchestrator` initializes agents and defines CrewAI tasks/workflow.
4.  CrewAI runs the workflow:
    *   Manager agent plans tasks using its LLM.
    *   Manager delegates coding task to Engineer agent.
    *   Engineer agent uses `AiderTool`.
    *   `AiderTool` executes Aider process (which uses its configured LLM).
    *   Aider modifies files on the filesystem.
    *   `AiderTool` captures Aider output.
    *   Engineer reports results back to Manager.
    *   Manager reviews/iterates or reports completion.
5.  Throughout the process, agent actions/thoughts and Aider logs are streamed back via WebSocket Manager -> FastAPI WebSocket endpoint -> React UI.

## Error Handling
*   Initial strategy: Attempt automatic retries for transient errors (e.g., LLM API issues), then pause and prompt the user for guidance via the chatbot interface if retries fail or for unrecoverable errors.