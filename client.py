import socket
import threading
import json
import customtkinter as ctk
from datetime import datetime

class ChatClient:
    def __init__(self, host='localhost', port=5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        
        # GUI setup
        self.window = ctk.CTk()
        self.window.title("Chat Application")
        self.window.geometry("800x600")
        
        # Configure grid
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(0, weight=1)
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Create chat display
        self.chat_display = ctk.CTkTextbox(self.main_frame, wrap="word")
        self.chat_display.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="nsew")
        
        # Create input frame
        self.input_frame = ctk.CTkFrame(self.main_frame)
        self.input_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)
        
        # Create message input
        self.message_input = ctk.CTkEntry(self.input_frame, placeholder_text="Type your message...")
        self.message_input.grid(row=0, column=0, padx=(0, 5), sticky="ew")
        
        # Create send button
        self.send_button = ctk.CTkButton(self.input_frame, text="Send", command=self.send_message)
        self.send_button.grid(row=0, column=1, padx=(5, 0))
        
        # Bind Enter key to send message
        self.message_input.bind("<Return>", lambda event: self.send_message())
        
        # Username setup
        self.username = None
        self.setup_username()
        
    def setup_username(self):
        """Setup username dialog"""
        self.username_window = ctk.CTkToplevel(self.window)
        self.username_window.title("Enter Username")
        self.username_window.geometry("300x150")
        
        # Center the window
        self.username_window.transient(self.window)
        self.username_window.grab_set()
        
        # Create username input
        ctk.CTkLabel(self.username_window, text="Enter your username:").pack(pady=10)
        username_entry = ctk.CTkEntry(self.username_window)
        username_entry.pack(pady=10)
        
        def submit_username():
            username = username_entry.get().strip()
            if username:
                self.username = username
                self.username_window.destroy()
                self.connect_to_server()
        
        ctk.CTkButton(self.username_window, text="Join Chat", command=submit_username).pack(pady=10)
        
    def connect_to_server(self):
        """Connect to the server"""
        try:
            self.client.connect((self.host, self.port))
            
            # Start receiving thread
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.start()
            
        except Exception as e:
            self.display_message("System", f"Error connecting to server: {str(e)}")
            
    def send_message(self):
        """Send message to server"""
        message = self.message_input.get().strip()
        if message:
            try:
                message_data = {
                    'type': 'message',
                    'username': self.username,
                    'content': message,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                self.client.send(json.dumps(message_data).encode('utf-8'))
                self.message_input.delete(0, 'end')
            except Exception as e:
                self.display_message("System", f"Error sending message: {str(e)}")
                
    def receive_messages(self):
        """Receive messages from server"""
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message == 'USERNAME':
                    self.client.send(self.username.encode('utf-8'))
                else:
                    message_data = json.loads(message)
                    self.display_message(
                        message_data.get('username', 'System'),
                        message_data.get('content', ''),
                        message_data.get('timestamp', '')
                    )
            except:
                self.display_message("System", "Lost connection to server")
                self.client.close()
                break
                
    def display_message(self, username, content, timestamp=''):
        """Display message in chat window"""
        if timestamp:
            message = f"[{timestamp}] {username}: {content}\n"
        else:
            message = f"{username}: {content}\n"
            
        self.chat_display.insert('end', message)
        self.chat_display.see('end')
        
    def run(self):
        """Start the client application"""
        self.window.mainloop()

if __name__ == "__main__":
    client = ChatClient()
    client.run() 