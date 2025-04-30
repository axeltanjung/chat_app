import socket
import threading
import json
from datetime import datetime

class ChatServer:
    def __init__(self, host='localhost', port=5555):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        
        self.clients = []
        self.usernames = []
        self.messages = []
        
        print(f"Server is running on {host}:{port}")
        
    def broadcast(self, message):
        """Send message to all connected clients"""
        for client in self.clients:
            client.send(message)
            
    def handle_client(self, client):
        """Handle individual client connections"""
        while True:
            try:
                message = client.recv(1024)
                if message:
                    # Decode and process the message
                    message_data = json.loads(message.decode('utf-8'))
                    
                    # Add timestamp to message
                    message_data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    
                    # Store message in history
                    self.messages.append(message_data)
                    
                    # Broadcast to all clients
                    self.broadcast(json.dumps(message_data).encode('utf-8'))
                    
            except:
                # Remove and close client
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                username = self.usernames[index]
                self.broadcast(json.dumps({
                    'type': 'system',
                    'content': f'{username} left the chat!',
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }).encode('utf-8'))
                self.usernames.remove(username)
                break
                
    def start(self):
        """Start the server and accept connections"""
        while True:
            client, address = self.server.accept()
            print(f"Connected with {str(address)}")
            
            # Request and store username
            client.send('USERNAME'.encode('utf-8'))
            username = client.recv(1024).decode('utf-8')
            self.usernames.append(username)
            self.clients.append(client)
            
            # Send welcome message
            welcome_message = {
                'type': 'system',
                'content': f'{username} joined the chat!',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            self.broadcast(json.dumps(welcome_message).encode('utf-8'))
            
            # Send message history to new client
            for message in self.messages[-50:]:  # Send last 50 messages
                client.send(json.dumps(message).encode('utf-8'))
            
            # Start handling thread for client
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()

if __name__ == "__main__":
    server = ChatServer()
    server.start() 