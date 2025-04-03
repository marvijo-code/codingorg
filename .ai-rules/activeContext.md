# Active Context: AI Chatbot Orchestrator - Initial Setup & Debugging

## Current Focus
We are in the initial setup phase, establishing the basic project structure and dependencies for the backend (FastAPI, CrewAI) and frontend (Vite/React). We are currently debugging issues related to configuring the LLM (Google Gemini) within the CrewAI framework.

## Recent Changes
*   Initialized project using `uv`.
*   Installed backend dependencies (`fastapi`, `uvicorn`, `crewai`, `python-dotenv`, `aider-chat`, `requests`, `langchain-google-genai`).
*   Created basic backend structure (`main.py`, `.env`, directories/files for agents, tools, crew, utils).
*   Created Vite/React frontend structure and installed dependencies (`npm install` via WSL).
*   Attempted various methods to configure Google Gemini for CrewAI agents:
    *   Explicit `ChatGoogleGenerativeAI` initialization (led to `DefaultCredentialsError`).
    *   Environment variables (`OPENAI_...` style) (led to `LLM Provider NOT provided` error).
    *   Environment variable (`GEMINI_API_KEY`) (led to `LLM Provider NOT provided` error).
    *   Dictionary-based config for Crew (led to `LLM Provider NOT provided` error).
    *   Dictionary-based config for Agent (led to `LLM Provider NOT provided` error).
*   Terminated potentially conflicting Uvicorn server processes.
*   Modified `backend/agents/manager.py` to remove explicit LLM configuration, relying on CrewAI defaults and `GEMINI_API_KEY` env var.

## Current State
*   The FastAPI server (`backend/main.py`) is set up with basic endpoints (`/`, `/ws`, `/start_task`).
*   Placeholder files exist for agents, tools, orchestrator, and WebSocket manager.
*   `backend/.env` contains `GEMINI_API_KEY`.
*   `backend/main.py` correctly loads `.env`.
*   `backend/agents/manager.py` currently has no explicit LLM configuration.
*   Sending a request via `send_request.py` still results in a `litellm.BadRequestError: LLM Provider NOT provided` when the Development Manager agent tries to execute its first task.

## Next Steps
1.  Restart the Uvicorn server **without** the `--reload` flag for stability.
2.  Run `send_request.py` again to confirm the current error state with the simplified agent LLM configuration.
3.  If the error persists, investigate alternative CrewAI/LiteLLM configuration methods specifically for Google Gemini, potentially involving different environment variables or initialization parameters based on further documentation review or trying different model strings (e.g., without any prefix).
4.  Address any remaining Flake8 errors in `backend/agents/manager.py`.