# TCP Chat Server

A simple, multi-threaded TCP chat server built with Python using only the standard library.

## Features

- **Multi-client support**: Handles multiple concurrent connections using threading.
- **Username-based login**: Use `LOGIN <username>` to join.
- **Real-time broadcasting**: Messages sent with `MSG` are broadcast to all other users.
- **Direct Messaging**: Private messages supported via `DM`.
- **User Discovery**: List connected users with `WHO`.
- **Disconnect notifications**: Notifies active users when someone leaves.

## Requirements

- Python 3.x
- Standard library (socket, threading)

## Usage

### Starting the Server

```bash
# Default port 4000
python3 server.py

# Custom port
python3 server.py 5000
# OR
CHAT_PORT=5000 python3 server.py
```

### Connecting as a Client

You can use `nc` (netcat) or `telnet` to connect to the server.

```bash
nc localhost 4000
```

### Commands Protocol

| Command   | Usage              | Description                                    |
| :-------- | :----------------- | :--------------------------------------------- |
| **LOGIN** | `LOGIN <username>` | Log in with a unique username.                 |
| **MSG**   | `MSG <text>`       | Broadcast a message to all connected users.    |
| **DM**    | `DM <user> <text>` | Send a private message to a specific user.     |
| **WHO**   | `WHO`              | List all currently connected usernames.        |
| **PING**  | `PING`             | Check if server is alive (responds with PONG). |

### Example Session

**Terminal 1 (Server)**

```text
$ python3 server.py
Server listening on 0.0.0.0:4000
Accepted connection from ('127.0.0.1', 54321)
```

**Terminal 2 (Client 1)**

```text
$ nc localhost 4000
Welcome! Please login with: LOGIN <username>
LOGIN Alice
OK
MSG Hello world!
```

**Terminal 3 (Client 2)**

```text
$ nc localhost 4000
Welcome! Please login with: LOGIN <username>
LOGIN Bob
OK
MSG Alice Hello world!
MSG Hi Alice!
```

## Testing

A `test_server.py` script is included to run automated verification of all features.

```bash
python3 test_server.py
```

## Architecture

The server uses a thread-per-client model.

- **Main Thread**: Listens for incoming TCP connections on the specified port.
- **Client Threads**: A new thread is spawned for each connected client to handle the `recv` loop.
- **Synchronization**: A `threading.Lock` is used to ensure thread-safe access to the shared `clients` dictionary.
