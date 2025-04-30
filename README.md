# Python Chat Application

A modern chat application built with Python using socket programming and customtkinter for the GUI.

## Features

- Real-time messaging
- Modern GUI interface
- User authentication
- Message history
- System notifications
- Timestamp for messages

## Requirements

- Python 3.7+
- Required packages (install using `pip install -r requirements.txt`):
  - customtkinter
  - socket
  - threading
  - json
  - datetime

## Installation

1. Clone the repository or download the files
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the server:
   ```bash
   python server.py
   ```

2. Start the client(s):
   ```bash
   python client.py
   ```

3. Enter your username when prompted
4. Start chatting!

## How it Works

- The server handles multiple client connections using threading
- Messages are broadcasted to all connected clients
- The client application provides a modern GUI interface
- Messages are stored with timestamps
- System notifications for user join/leave events

## Security Note

This is a basic implementation for educational purposes. For production use, consider adding:
- Encryption
- User authentication
- Message validation
- Error handling
- Connection security

## License

MIT License 