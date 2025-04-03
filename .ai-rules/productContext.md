# Product Context: AI Chatbot Orchestrator

## Core Goal
Create an AI Chatbot that acts as an orchestrator for an AI software development team. The chatbot receives user requirements via text prompts and manages the AI team to deliver working software.

## Problem Solved
Automates the software development lifecycle using AI agents, streamlining the process from requirement gathering to code generation and testing.

## How it Should Work
1.  **User Interaction:** Users interact with a web-based chatbot (Vite + React frontend).
2.  **Input:** Users provide software requirements through text prompts.
3.  **Orchestration:** The chatbot backend (FastAPI + CrewAI) receives the prompt.
4.  **Team Management:** A CrewAI setup manages a team of AI agents.
    *   **Initial Team:** Development Manager, Senior Software Engineer.
    *   **Development Manager:** Analyzes requirements, breaks down tasks, assigns work to the engineer, reviews output. Uses Google Gemini 2.5 Pro Exp (0325).
    *   **Senior Software Engineer:** Receives tasks, uses the Aider tool to write/modify/test code. Aider uses Google Gemini 2.5 Pro Exp (0325).
    *   **Utility Agent (Future):** Summarizes logs/text using Google Gemini 2.0 Flash.
5.  **Coding:** The Senior Engineer uses Aider (integrated as a custom CrewAI tool) for all coding tasks.
6.  **Logging:** All CrewAI agent outputs (thoughts, actions) and Aider logs (including streamed text/diffs) should be displayed in the frontend in real-time.
7.  **Parallelism:** The system should support parallel task execution by agents.
8.  **Testing:** Generated code must have high unit and integration test coverage (minimum 90%).
9.  **Output:** The final deliverable is working software based on the user's requirements.