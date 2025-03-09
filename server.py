import http.server
import socketserver
import json
import os

PORT = 8000
CHAT_FILE = 'chats.json'

# Initialize empty chats file if it doesn't exist
if not os.path.exists(CHAT_FILE):
    with open(CHAT_FILE, 'w') as file:
        json.dump([], file)

class ChatHandler(http.server.SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        # Handle preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', 'https://beingrkn.github.io')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def send_header(self, keyword, value):
        # Prevent duplicate headers
        if keyword.lower() == 'access-control-allow-origin':
            return  # Skip adding the header if it already exists
        super().send_header(keyword, value)

    def end_headers(self):
        # Add CORS headers to all responses
        self.send_header('Access-Control-Allow-Origin', 'https://beingrkn.github.io')
        super().end_headers()

    def do_GET(self):
        if self.path == '/get-chats':
            with open(CHAT_FILE, 'r') as file:
                chats = json.load(file)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(chats).encode())
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/add-chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            new_chat = json.loads(post_data)

            with open(CHAT_FILE, 'r') as file:
                chats = json.load(file)

            chats.append(new_chat)

            with open(CHAT_FILE, 'w') as file:
                json.dump(chats, file, indent=4)

            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'success'}).encode())

# Run the server
with socketserver.TCPServer(('', PORT), ChatHandler) as httpd:
    print(f'Serving at http://localhost:{PORT}')
    httpd.serve_forever()
