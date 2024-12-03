import requests
import json
import data
from game_functions import *



PARENT_URL = "http://localhost:8080"

# Function to send messages to the parent
def send_message(endpoint, message):
    try:
        response = requests.post(f"{PARENT_URL}{endpoint}", data=json.dumps(message))
        print(f"[Child] Sent message to {endpoint}: {response.status_code}")
    except Exception as e:
        print(f"[Child] Failed to send message: {e}")

# Custom code execution function
def execute_user_code(user_code):
    def send_message_to_parent(endpoint, message):
        """Safe function exposed to user code to send messages to the parent."""
        if not isinstance(endpoint, str) or not isinstance(message, dict):
            raise ValueError("Invalid arguments: 'endpoint' must be a string, 'message' must be a dictionary.")
        send_message(endpoint, message)

    # Restricted globals for user code
    safe_globals = {
        "__builtins__": {
            "range": range,
            "sum": sum,
            "print": print,
        },
        "send_message_to_parent": send_message_to_parent,
        "door_close" : door_close,
        "door_open" : door_open,
        "blinds_close" : blinds_close,
        "blinds_open" : blinds_open # Expose the function
    }
    safe_locals = {}
    
    try:
        exec(user_code, safe_globals, safe_locals)
        return {"status": "success", "result": safe_locals.get("result", "No result")}
    except Exception as e:
        return {"status": "error", "error": str(e)}

if __name__ == "__main__":
    # Step 1: Send handshake to parent
    send_message("/handshake", {"status": "started"})

    # Step 2: Execute user code (replace this with actual input)
    user_code = """
# User-defined code
door_close()
door_open()
"""
    result = execute_user_code(user_code)

    # Step 3: Send result to parent
    send_message("/result", result)
