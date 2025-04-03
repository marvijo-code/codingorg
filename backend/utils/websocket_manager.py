# backend/utils/websocket_manager.py
from fastapi import WebSocket
from typing import List, Dict, Any
import json
import asyncio

class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Accepts a new WebSocket connection."""
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"New WebSocket connection: {websocket.client}")
        # Optionally send a welcome message or initial state
        # await websocket.send_json({"type": "status", "message": "Connected"})

    def disconnect(self, websocket: WebSocket):
        """Removes a WebSocket connection."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            print(f"WebSocket connection closed: {websocket.client}")

    async def broadcast_message(self, message: Dict[str, Any]):
        """Sends a JSON message to all active connections."""
        print(f"Broadcasting message: {message}")
        message_json = json.dumps(message)
        # Create a list of tasks for sending messages concurrently
        send_tasks = [conn.send_text(message_json) for conn in self.active_connections]
        # Wait for all messages to be sent (or handle exceptions)
        results = await asyncio.gather(*send_tasks, return_exceptions=True)
        for result, conn in zip(results, self.active_connections):
            if isinstance(result, Exception):
                print(f"Error sending message to {conn.client}: {result}")
                # Optionally remove problematic connections
                # self.disconnect(conn) # Be careful with modifying list during iteration

    async def send_personal_message(self, message: Dict[str, Any], websocket: WebSocket):
        """Sends a JSON message to a specific WebSocket connection."""
        if websocket in self.active_connections:
            print(f"Sending personal message to {websocket.client}: {message}")
            try:
                await websocket.send_json(message)
            except Exception as e:
                print(f"Error sending personal message to {websocket.client}: {e}")
                # Optionally disconnect on error
                # self.disconnect(websocket)

# --- Example Usage (Conceptual) ---
# This manager would typically be instantiated once in your FastAPI app
# and passed to components that need to send updates (like the TaskOrchestrator).

# Example in main.py:
# from backend.utils.websocket_manager import WebSocketManager
# manager = WebSocketManager()
#
# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await manager.connect(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             # Handle incoming messages if needed
#             await manager.broadcast_message({"type": "echo", "data": data}) # Example broadcast
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)
#     except Exception as e:
#         print(f"WebSocket error in endpoint: {e}")
#         manager.disconnect(websocket)
#         await websocket.close(code=1011)

# Example in TaskOrchestrator:
# class TaskOrchestrator:
#     def __init__(self, websocket_manager: WebSocketManager):
#         self.websocket_manager = websocket_manager
#
#     def some_method_generating_update(self, update_data):
#         if self.websocket_manager:
#             # Use asyncio.create_task or similar if calling from sync code
#             # to avoid blocking, or ensure the calling context is async.
#             asyncio.create_task(
#                 self.websocket_manager.broadcast_message({"type": "update", "data": update_data})
#             )

# Need to import asyncio for the broadcast_message method