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
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
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