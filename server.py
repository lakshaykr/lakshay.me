import http.server
import socketserver
import json
import os
from datetime import datetime
import pytz  # Use pytz for timezone handling
import psycopg2

# Define the port
PORT = int(os.getenv('PORT', 8000))  # Use PORT environment variable or default to 8000

# Database connection details
DATABASE_URL = os.getenv('DATABASE_URL')  # Set this in Render's environment variables

# Connect to the database
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# Create chats table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS chats (
        id SERIAL PRIMARY KEY,
        username TEXT NOT NULL,
        message TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()

class ChatHandler(http.server.SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        # Handle preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', 'https://beingrkn.github.io')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        if self.path == '/get-chats':
            cursor.execute('SELECT username, message, timestamp FROM chats ORDER BY timestamp DESC')
            chats = cursor.fetchall()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', 'https://beingrkn.github.io')
            self.end_headers()
            self.wfile.write(json.dumps([{
                'username': row[0],
                'message': row[1],
                'timestamp': row[2].strftime('%d %b %Y, %I:%M %p IST')
            } for row in chats]).encode())
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/add-chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            new_chat = json.loads(post_data)

            # Add timestamp in IST
            ist = pytz.timezone('Asia/Kolkata')
            new_chat['timestamp'] = datetime.now(ist).strftime('%d %b %Y, %I:%M %p IST')

            # Insert new chat into the database
            cursor.execute('''
                INSERT INTO chats (username, message) VALUES (%s, %s)
            ''', (new_chat['username'], new_chat['message']))
            conn.commit()

            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', 'https://beingrkn.github.io')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'success'}).encode())

# Run the server
with socketserver.TCPServer(('', PORT), ChatHandler) as httpd:
    print(f'Serving at http://localhost:{PORT}')
    httpd.serve_forever()
