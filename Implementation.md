# TCP Chat Server Assignment

## Overview

This document provides a comprehensive, step-by-step guide for an AI agent to complete the Backend Assignment for building a Simple Socket Chat Server from scratch.

---

## Phase 1: Planning & Analysis (5-10 minutes)

### Step 1.1: Understand Requirements

- Read and parse the assignment document thoroughly
- Extract all core requirements:
  - Port 4000 (configurable)
  - Handle 5-10 concurrent clients
  - LOGIN flow with username validation
  - Message broadcasting (MSG)
  - Disconnect notifications (INFO)
  - Optional features: WHO, DM, PING/PONG, idle timeout

### Step 1.2: Choose Technology Stack

- **Recommended**: Python (simple, clean, good standard library support)
- **Alternative options**: Node.js, Go, Java
- **Decision criteria**:
  - Standard library socket support
  - Threading/async capabilities
  - Ease of demonstration
  - Agent's proficiency

### Step 1.3: Design Architecture

- Identify key components:
  1. **Server class**: Main socket listener
  2. **Client handler**: Per-client thread/coroutine
  3. **User registry**: Track active users (username → connection mapping)
  4. **Message parser**: Parse LOGIN, MSG, WHO, DM, PING commands
  5. **Broadcast mechanism**: Send to all/specific users

---

## Phase 2: Implementation (30-45 minutes)

### Step 2.1: Set Up Project Structure

Create the following files:

```
chat-server/
├── server.py (or server.js, server.go, etc.)
├── README.md
├── .gitignore (optional)
└── requirements.txt (if needed)
```

### Step 2.2: Implement Core Server Setup

**Task**: Create basic TCP server that listens on port 4000

```python
# Pseudocode structure
import socket
import threading

class ChatServer:
    def __init__(self, host='0.0.0.0', port=4000):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = {}  # {username: socket}
        self.lock = threading.Lock()

    def start(self):
        # Create socket
        # Bind to host:port
        # Listen for connections
        # Accept loop
```

**Checklist**:

- [ ] Socket creation with `socket.socket()`
- [ ] Bind to configurable port (env var or CLI arg)
- [ ] Listen with appropriate backlog
- [ ] Accept connections in loop
- [ ] Handle KeyboardInterrupt for graceful shutdown

### Step 2.3: Implement Client Handler

**Task**: Create threaded handler for each client connection

```python
# Pseudocode
def handle_client(self, client_socket, client_address):
    username = None
    try:
        # Wait for LOGIN command
        # Validate username (not taken)
        # Add to clients dict
        # Enter message loop
        # Parse and route commands
    except:
        # Handle disconnection
    finally:
        # Cleanup and notify others
```

**Checklist**:

- [ ] Spawn new thread for each client
- [ ] Receive data in chunks (handle partial messages)
- [ ] Parse newline-delimited commands
- [ ] Handle socket errors and disconnections
- [ ] Thread-safe access to shared `clients` dictionary

### Step 2.4: Implement LOGIN Flow

**Task**: Handle user authentication and username validation

**Protocol**:

- Receive: `LOGIN <username>`
- Check if username exists in `self.clients`
- Respond: `ERR username-taken` or `OK`

**Checklist**:

- [ ] Parse LOGIN command (split by space)
- [ ] Validate username (no spaces, reasonable length)
- [ ] Thread-safe check and insert into clients dict
- [ ] Send appropriate response with newline
- [ ] Block further commands until successful login

### Step 2.5: Implement Message Broadcasting

**Task**: Broadcast messages to all connected users

**Protocol**:

- Receive: `MSG <text>`
- Broadcast: `MSG <username> <text>` to all clients

```python
# Pseudocode
def broadcast(self, message, exclude_user=None):
    with self.lock:
        for username, socket in self.clients.items():
            if username != exclude_user:
                try:
                    socket.sendall(message.encode() + b'\n')
                except:
                    # Mark for removal if send fails
```

**Checklist**:

- [ ] Parse MSG command
- [ ] Extract message text (handle spaces)
- [ ] Format broadcast message
- [ ] Send to all clients (thread-safe)
- [ ] Handle failed sends (broken connections)

### Step 2.6: Implement Disconnect Handling

**Task**: Clean up when users disconnect

**Checklist**:

- [ ] Detect disconnection (empty recv or exception)
- [ ] Remove user from `self.clients`
- [ ] Broadcast `INFO <username> disconnected`
- [ ] Close socket properly

### Step 2.7: Implement Optional Features (Bonus)

#### WHO Command

- Receive: `WHO`
- Respond with: `USER <username>` for each connected user

#### DM (Direct Message)

- Receive: `DM <target_username> <text>`
- Send to specific user: `DM <sender_username> <text>`
- Handle non-existent users

#### PING/PONG

- Receive: `PING`
- Respond: `PONG`

#### Idle Timeout

- Track last activity timestamp per client
- Background thread to check timeouts
- Disconnect after 60 seconds of inactivity

**Checklist**:

- [ ] Implement WHO command
- [ ] Implement DM command
- [ ] Implement PING/PONG
- [ ] Implement idle timeout (optional)

### Step 2.8: Add Configuration Options

**Task**: Make port and host configurable

```python
# Example
import os
import sys

port = int(os.getenv('CHAT_PORT', 4000))
# OR
port = int(sys.argv[1]) if len(sys.argv) > 1 else 4000
```

**Checklist**:

- [ ] Support environment variable (e.g., `CHAT_PORT`)
- [ ] Support command-line argument
- [ ] Document in README

---

## Phase 3: Testing (15-20 minutes)

### Step 3.1: Unit Testing

**Test each component**:

1. **Server startup**: Can it bind to port 4000?
2. **Connection handling**: Can multiple clients connect?
3. **LOGIN flow**:
   - Accept valid username
   - Reject duplicate username
4. **Message broadcasting**: Do all clients receive messages?
5. **Disconnect handling**: Is INFO sent correctly?

### Step 3.2: Integration Testing

**Test scenarios**:

#### Scenario 1: Two Users Chatting

```bash
# Terminal 1
$ nc localhost 4000
LOGIN Alice
# Expect: OK
MSG Hello everyone!

# Terminal 2
$ nc localhost 4000
LOGIN Bob
# Expect: OK
MSG Hi Alice!

# Terminal 1 should see:
# MSG Bob Hi Alice!
```

#### Scenario 2: Username Collision

```bash
# Terminal 1
$ nc localhost 4000
LOGIN Alice
# Expect: OK

# Terminal 2
$ nc localhost 4000
LOGIN Alice
# Expect: ERR username-taken
```

#### Scenario 3: Disconnection

```bash
# Terminal 1
LOGIN Alice
# Disconnect (Ctrl+C or close)

# Terminal 2 should see:
# INFO Alice disconnected
```

**Checklist**:

- [ ] Test with 2 clients
- [ ] Test with 5+ clients
- [ ] Test username collision
- [ ] Test message broadcasting
- [ ] Test disconnect notification
- [ ] Test WHO command (if implemented)
- [ ] Test DM command (if implemented)

### Step 3.3: Edge Case Testing

**Test edge cases**:

- Empty messages
- Very long messages (>1000 chars)
- Special characters in messages
- Rapid connect/disconnect
- Messages sent before login
- Malformed commands

**Checklist**:

- [ ] Handle empty input gracefully
- [ ] Handle long messages
- [ ] Handle special characters
- [ ] Handle commands before login
- [ ] Handle malformed commands

---

## Phase 4: Documentation (10-15 minutes)

### Step 4.1: Create README.md

**Required sections**:

````markdown
# TCP Chat Server

## Description

A simple TCP-based chat server built with [language] using only standard library.

## Features

- Multi-client support (5-10 concurrent users)
- Username-based login
- Real-time message broadcasting
- Disconnect notifications
- [Optional features implemented]

## Requirements

- [Language] [version]
- Standard library only (no external dependencies)

## Installation

[Installation steps if any]

## Running the Server

```bash
# Default (port 4000)
python server.py

# Custom port
python server.py 5000
# OR
CHAT_PORT=5000 python server.py
```
````

## Connecting as a Client

```bash
# Using netcat
nc localhost 4000

# Using telnet
telnet localhost 4000
```

## Commands

- `LOGIN <username>` - Log in with a username
- `MSG <text>` - Send a message to all users
- `WHO` - List all connected users (if implemented)
- `DM <username> <text>` - Send private message (if implemented)
- `PING` - Heartbeat check (if implemented)

## Example Usage

[Include the example from assignment]

## Screen Recording

[Link to video demonstration]

## Architecture

[Brief explanation of design]

## Author

[Your name]

```

**Checklist**:
- [ ] Clear description
- [ ] Installation instructions
- [ ] Running instructions (with examples)
- [ ] Client connection examples
- [ ] Command documentation
- [ ] Example interaction (copy from assignment)
- [ ] Screen recording link placeholder

### Step 4.2: Add Code Comments

**Add comments for**:
- Complex logic
- Protocol explanations
- Thread safety considerations
- Error handling reasoning

**Checklist**:
- [ ] Function/method docstrings
- [ ] Inline comments for complex sections
- [ ] Protocol format comments

---

## Phase 5: Screen Recording (5-10 minutes)

### Step 5.1: Prepare Recording Environment

**Setup**:
1. Open terminal for server
2. Open 2-3 terminals for clients
3. Clear terminals for clean recording
4. Test run once before recording

### Step 5.2: Record Demonstration

**Recording script** (1-2 minutes):

```

[0:00-0:10] Show code structure

- Briefly show server.py file
- Show README.md

[0:10-0:20] Start server

- Run: python server.py
- Show "Server listening on port 4000" message

[0:20-0:40] Connect Client 1

- Run: nc localhost 4000
- Type: LOGIN Alice
- Show: OK response
- Type: MSG Hello everyone!

[0:40-1:00] Connect Client 2

- Run: nc localhost 4000
- Type: LOGIN Bob
- Show: OK response
- Show Client 1 receiving: MSG Bob [message]
- Type: MSG Hi Alice!

[1:00-1:20] Show features

- Type WHO (if implemented)
- Show user list
- Type DM Alice <message> (if implemented)

[1:20-1:30] Demonstrate disconnect

- Close Client 1
- Show Client 2 receiving: INFO Alice disconnected

[1:30-2:00] Show bonus features (if implemented)

- PING/PONG
- Explain briefly

````

**Checklist**:
- [ ] Use screen recorder (Loom, OBS, QuickTime, etc.)
- [ ] Record clear terminal output
- [ ] Demonstrate all core features
- [ ] Show at least 2 clients chatting
- [ ] Show disconnect notification
- [ ] Keep recording under 2 minutes
- [ ] Upload to YouTube/Loom/Google Drive
- [ ] Add link to README

---

## Phase 6: Final Review & Submission (5-10 minutes)

### Step 6.1: Code Review Checklist

- [ ] Code follows language conventions
- [ ] No external libraries (only standard lib)
- [ ] Proper error handling
- [ ] Thread-safe operations
- [ ] Clean, readable code
- [ ] Comments where needed
- [ ] No hardcoded values (use config)

### Step 6.2: Feature Completeness Checklist

**Core Requirements**:
- [ ] Server listens on port 4000
- [ ] Handles 5-10 concurrent clients
- [ ] LOGIN with username validation
- [ ] MSG broadcasting
- [ ] Disconnect notifications (INFO)
- [ ] Configurable port

**Optional Features**:
- [ ] WHO command
- [ ] DM (private messaging)
- [ ] PING/PONG
- [ ] Idle timeout

### Step 6.3: Documentation Checklist

- [ ] README.md complete
- [ ] Installation instructions clear
- [ ] Running instructions with examples
- [ ] Command documentation
- [ ] Example interactions included
- [ ] Screen recording linked

### Step 6.4: Testing Checklist

- [ ] Tested with multiple clients
- [ ] Tested username collision
- [ ] Tested message broadcasting
- [ ] Tested disconnect handling
- [ ] Tested all implemented features
- [ ] Tested edge cases

### Step 6.5: Prepare Submission

**Deliverables**:
1. **Source Code**: `server.py` (or equivalent)
2. **README.md**: Complete documentation
3. **Screen Recording**: Video link in README
4. **Optional**: Deployment details (if hosted)

**Submission format**:
- ZIP file or GitHub repository
- Clear file structure
- All files included

---

## Common Pitfalls & Solutions

### Pitfall 1: Race Conditions
**Problem**: Multiple threads accessing `clients` dict simultaneously
**Solution**: Use `threading.Lock()` for all dict operations

### Pitfall 2: Partial Message Receives
**Problem**: `recv()` doesn't guarantee complete message
**Solution**: Buffer data and split on newlines

### Pitfall 3: Broken Pipe Errors
**Problem**: Sending to disconnected client
**Solution**: Catch exceptions, remove dead clients

### Pitfall 4: Blocking on Recv
**Problem**: Thread hangs waiting for data
**Solution**: Use timeout or non-blocking sockets

### Pitfall 5: Not Handling SIGINT
**Problem**: Server doesn't shut down cleanly
**Solution**: Catch `KeyboardInterrupt` and close sockets

---

## Example Implementation Skeleton (Python)

```python
#!/usr/bin/env python3
import socket
import threading
import sys
import os

class ChatServer:
    def __init__(self, host='0.0.0.0', port=4000):
        self.host = host
        self.port = port
        self.clients = {}  # {username: socket}
        self.lock = threading.Lock()

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(10)

        print(f"Server listening on {self.host}:{self.port}")

        try:
            while True:
                client_socket, address = self.server_socket.accept()
                thread = threading.Thread(target=self.handle_client,
                                         args=(client_socket, address))
                thread.daemon = True
                thread.start()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            self.server_socket.close()

    def handle_client(self, client_socket, address):
        username = None
        try:
            # LOGIN flow
            # Message loop
            # Command parsing
            pass
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            if username:
                with self.lock:
                    if username in self.clients:
                        del self.clients[username]
                self.broadcast(f"INFO {username} disconnected")
            client_socket.close()

    def broadcast(self, message, exclude=None):
        with self.lock:
            dead_clients = []
            for username, sock in self.clients.items():
                if username != exclude:
                    try:
                        sock.sendall(message.encode() + b'\n')
                    except:
                        dead_clients.append(username)

            for username in dead_clients:
                del self.clients[username]

if __name__ == "__main__":
    port = int(os.getenv('CHAT_PORT', 4000))
    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    server = ChatServer(port=port)
    server.start()
````

---

## Time Estimation

| Phase               | Estimated Time     |
| ------------------- | ------------------ |
| Planning & Analysis | 5-10 minutes       |
| Implementation      | 30-45 minutes      |
| Testing             | 15-20 minutes      |
| Documentation       | 10-15 minutes      |
| Screen Recording    | 5-10 minutes       |
| Final Review        | 5-10 minutes       |
| **Total**           | **70-110 minutes** |

---

## Success Criteria

The assignment is complete when:

1. ✅ Server runs and listens on port 4000
2. ✅ Multiple clients can connect simultaneously
3. ✅ LOGIN flow works with username validation
4. ✅ Messages broadcast to all users correctly
5. ✅ Disconnect notifications appear
6. ✅ README.md is complete and clear
7. ✅ Screen recording demonstrates all features
8. ✅ Code uses only standard library
9. ✅ All edge cases handled gracefully
10. ✅ Bonus features implemented (optional)

---

## Quick Start Command Summary

```bash
# 1. Create project
mkdir chat-server && cd chat-server

# 2. Create server file
touch server.py

# 3. Implement (follow Phase 2 steps)

# 4. Test server
python server.py

# 5. Connect clients (new terminals)
nc localhost 4000

# 6. Create documentation
touch README.md

# 7. Record demonstration

# 8. Submit
```

---

## Additional Resources

- **Socket Programming**: [Python socket docs](https://docs.python.org/3/library/socket.html)
- **Threading**: [Python threading docs](https://docs.python.org/3/library/threading.html)
- **netcat**: Testing tool for TCP connections
- **Screen Recording**: OBS Studio, Loom, QuickTime

---

**End of Guidelines**

Good luck with the implementation! 🚀
