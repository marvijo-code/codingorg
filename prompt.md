# Create an AI Chatbot that will orchestrate an AI Software Development team. 

## Team Composition
- Use latest version of CrewAI Flows and CrewAI Crews to represent the Software Development team
- Use uv and a local venv environment
- The team should start with a Development Manager and a Senior Software Engineer
- Add Aider (https://github.com/Aider-AI/aider) as a CrewAI tool
- Use Aider to do all the coding tasks (https://github.com/Aider-AI/aider)
- Aider logs should be displayed in the frontend
- Use a management agent for the Development Manager
- Use Vite React for the Web frontend
- All CrewAI logs should be displayed in the frontend
- Use different Large Language Models for appropriate tasks
- Large Language Models to support:
  - Google Gemini 2.5 Pro Exp (0325) (default for coding)
  - Google Gemini 2.5 Pro Exp (0325) (default for Development Manager)
  - Google Gemini 2.0 Flash (default for the small model which will summarize text like test run logs before sending them to the Developer or any other crew member)
- Team members should be able to run tasks in parallel
- Thoughts and outputs from different team members should be displayed on click in the frontend
- Make sure you use the available MCP tools to search the internet when you're stuck or need up to date information
- Output should always be shown, like output from the terminal
- Always make sure you have a minimum of 90% unit test coverage for the code you write
- Always make sure you have a minimum of 90% integration test coverage for the code you write
- The final product that the team delivers should be working software, according to a user's requirements

## Crewai samples: https://github.com/microsoft/semantic-kernel/tree/main/prompt_template_samples
