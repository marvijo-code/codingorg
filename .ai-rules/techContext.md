# Tech Context: AI Chatbot Orchestrator

## Core Technologies
*   **Python:** Backend language (using version 3.12 via Conda env `crewai`).
*   **CrewAI:** Framework for AI agent orchestration (`crewai==0.100.1`).
*   **LiteLLM:** Used internally by CrewAI for LLM interaction (`litellm==1.59.8`).
*   **Langchain:** Core components used by CrewAI (`langchain-google-genai`, `langchain-core`, etc.).
*   **Aider:** AI pair programming tool (`aider-chat==0.74.1`).
*   **FastAPI:** Async web framework for the backend.
*   **Uvicorn:** ASGI server for FastAPI.
*   **uv:** Python package installer and virtual environment manager.
*   **Node.js/npm:** For frontend development (Vite/React). Version in WSL seems to be v12.22.9, which might be too old for some frontend dependencies.
*   **React:** Frontend JavaScript library.
*   **Vite:** Frontend build tool.
*   **TypeScript:** Language for the frontend (optional, but used in setup).
*   **Google Gemini API:** Primary LLM provider.
    *   Target Models: `gemini/gemini-2.5-pro-exp-0325`, `gemini/gemini-2.0-flash-latest`.
    *   Authentication: API Key (`GEMINI_API_KEY` environment variable).

## Development Setup
*   **Environment:** Windows 11 with VSCode.
*   **Python Env:** Managed by `uv` within a Conda environment (`crewai`). Located at `C:\Users\marvi\.conda\envs\crewai`.
*   **Project Root:** `c:/dev/codingorg`.
*   **Backend Code:** Located in `c:/dev/codingorg/backend`.
*   **Frontend Code:** Located in `c:/dev/codingorg/frontend`.
*   **Running Backend:** `uvicorn backend.main:app --port 8000` (currently run without `--reload` for stability testing).
*   **Running Frontend (Standard):** `cd frontend && npm run dev`.
*   **Environment Variables:** Stored in `backend/.env` and loaded by `backend/main.py`. Currently includes `GEMINI_API_KEY`.

## Technical Constraints & Issues
*   **LLM Configuration:** Persistent difficulty getting CrewAI/LiteLLM to correctly recognize and use the Google Gemini provider via various configuration methods (explicit `ChatGoogleGenerativeAI`, environment variables, dictionary config). The current error is `litellm.BadRequestError: LLM Provider NOT provided`.
*   **Shell Environment:** The execution environment for `execute_command` seems restricted, causing issues with `npm install` (Node.js path) and `curl` (argument parsing). `npm install` was eventually run via WSL. `curl` requests were replaced with a Python script (`send_request.py`).
*   **Server Stability:** The Uvicorn server with `--reload` seemed unstable, possibly due to frequent file changes or watcher issues. Currently running without reload.
*   **Node.js Version:** The Node.js version detected in WSL (v12) might be incompatible with latest frontend dependencies (Vite, ESLint plugins often require v18+). This hasn't caused a runtime error yet but could later.