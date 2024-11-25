import http.server
import socketserver
import subprocess
import threading
import json
import os
import data



file_path = os.getcwd() 
PORT = 8080

class ChildMessageHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        # Read the JSON message from the child process
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        message = json.loads(post_data.decode())
        
        if self.path == "/handshake":
            print(f"[Parent] Handshake received: {message}")
        elif self.path == "/result":
            print(f"[Parent] Result received: {message}")
        elif self.path == "/custom":
            print(f"[Parent] Custom message received: {message}")
        elif self.path == "/door/close":
            if data.state["closed"] == False:
                print(f"[Parent] Door closed")
                data.state["closed"] = True
                
            else:
                print(f"[Parent] Door is already closed")
        elif self.path == "/door/open":
            if data.state["closed"] == True:
                print(f"[Parent] Door opened")
                data.state["closed"] = False
                
            else:
                print(f"[Parent] Door is already open")

        elif "/blinds/close/" in self.path :
            blind = self.path.replace("/blinds/close/", "")
            if data.state["blinds"][f"{blind}_closed"] == False:
                print(f"[Parent] {blind} closed")
                data.state["blinds"][f"{blind}_closed"] = True
            else:
                print(f"[Parent] {blind} is already closed")
        elif "/blinds/open/" in self.path :
            blind = self.path.replace("/blinds/open/", "")
            if data.state["blinds"][f"{blind}_closed"] == True:
                print(f"[Parent] {blind} opened")
                data.state["blinds"][f"{blind}_closed"] = False
            else:
                print(f"[Parent] {blind} is already open")
        else:
            print(f"[Parent] Unknown endpoint: {self.path}, message: {message}")

        # Respond with a 200 OK
        self.send_response(200)
        self.end_headers()

# Start the HTTP server in a separate thread
def start_server():
    with socketserver.TCPServer(("", PORT), ChildMessageHandler) as httpd:
        print(f"[Parent] HTTP server running on port {PORT}")
        httpd.serve_forever()

# Launch the child process
def start_child_process():
    try:
        if os.name == "nt":
            subprocess.Popen(["python", os.path.join(file_path,"safe_run/child.py")], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elif os.name == "posix":
            subprocess.Popen(["python3", "safe_run/child.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            print(f"[Parent] Failed to start child process: Unknown OS")
            return
        print("[Parent] Child process started.")
    except Exception as e:
        print(f"[Parent] Failed to start child process: {e}")

# Main program
if __name__ == "__main__":
    # Start the HTTP server in a thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # Start the child process
    start_child_process()

    # Keep the parent running
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("[Parent] Shutting down.")
