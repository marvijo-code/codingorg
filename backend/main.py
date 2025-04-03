from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.websockets import WebSocketDisconnect
import uvicorn
import os
# import asyncio  # For running crew in background potentially
from pydantic import BaseModel  # Moved import to top
from backend.utils.websocket_manager import WebSocketManager
from backend.crew.task_orchestrator import TaskOrchestrator
from dotenv import load_dotenv

# Load environment variables from backend/.env file
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
print(f"Attempting to load .env file from: {dotenv_path}")
load_dotenv(dotenv_path=dotenv_path)

# Debug: Check if the key is loaded immediately after
print(f"GOOGLE_API_KEY loaded in main.py: {'Yes' if os.getenv('GOOGLE_API_KEY') else 'No'}")

app = FastAPI()
manager = WebSocketManager()  # Create a single instance

# Basic HTML for testing WebSocket connection (optional, can be removed later)
html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket(`ws://${location.host}/ws`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

@app.get("/")
async def get():
    # Serve a simple HTML page for testing, will be replaced by Vite frontend
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection open, listening for potential messages from client
            # (though primary communication is server -> client for logs)
            data = await websocket.receive_text()
            print(f"Received message via WebSocket: {data}")
            # Handle client messages if needed (e.g., pause/resume commands)
            # For now, just acknowledge receipt
            await manager.send_personal_message({"type": "ack", "message": f"Received: {data}"}, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error in endpoint: {e}")
        manager.disconnect(websocket)
        # Ensure connection is closed if not already
        try:
            await websocket.close(code=1011)
        except RuntimeError:  # Handle cases where connection might already be closed
            pass

# Define request model for better validation (BaseModel import moved to top)

class TaskRequest(BaseModel):
    prompt: str

@app.post("/start_task")
async def start_task(task_request: TaskRequest):
    """Endpoint to start a new CrewAI task."""
    user_prompt = task_request.prompt
    print(f"Received task request via POST: {user_prompt}")

    # Instantiate orchestrator with the WebSocket manager
    orchestrator = TaskOrchestrator(websocket_manager=manager)

    # Run the crew - NOTE: This is currently BLOCKING
    # TODO: Run this in a background thread/task to not block the HTTP response
    # For now, the client will wait until the crew finishes.
    result = orchestrator.run_crew(user_prompt)

    # Return the final result (or an initial task ID if running in background)
    return {"message": "Task execution finished (sync).", "result": result}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)