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
        self.server_socket = None

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(10)
            print(f"Server listening on {self.host}:{self.port}")
        except Exception as e:
            print(f"Failed to bind/listen: {e}")
            return

        try:
            while True:
                client_socket, address = self.server_socket.accept()
                print(f"Accepted connection from {address}")
                thread = threading.Thread(target=self.handle_client,
                                         args=(client_socket, address))
                thread.daemon = True
                thread.start()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            self.server_socket.close()
        except Exception as e:
            print(f"Server error: {e}")
            if self.server_socket:
                self.server_socket.close()

    def handle_client(self, client_socket, address):
        username = None
        buffer = ""
        try:
            client_socket.sendall(b"Welcome! Please login with: LOGIN <username>\n")
            
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                
                try:
                    buffer += data.decode('utf-8')
                except UnicodeDecodeError:
                    continue # Skip invalid bytes

                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    command = line.strip()
                    if not command:
                        continue

                    parts = command.split(' ', 1)
                    cmd = parts[0].upper()
                    arg = parts[1] if len(parts) > 1 else ""

                    if not username:
                        if cmd == "LOGIN":
                            if not arg:
                                client_socket.sendall(b"ERR invalid-username\n")
                                continue
                            
                            new_username = arg.strip()
                            if " " in new_username or len(new_username) < 1:
                                client_socket.sendall(b"ERR invalid-username\n")
                                continue

                            with self.lock:
                                if new_username in self.clients:
                                    client_socket.sendall(b"ERR username-taken\n")
                                else:
                                    username = new_username
                                    self.clients[username] = client_socket
                                    client_socket.sendall(b"OK\n")
                        else:
                            client_socket.sendall(b"ERR login-required\n")
                    else:
                        if cmd == "MSG":
                            if not arg:
                                continue 
                            self.broadcast(f"MSG {username} {arg}", exclude_user=username)
                        elif cmd == "WHO":
                             with self.lock:
                                users = ", ".join(self.clients.keys())
                                client_socket.sendall(f"USERS {users}\n".encode('utf-8'))
                        elif cmd == "PING":
                             client_socket.sendall(b"PONG\n")
                        elif cmd == "DM":
                            self.handle_dm(username, arg, client_socket)
                        else:
                            client_socket.sendall(b"ERR unknown-command\n")

        except Exception as e:
            print(f"Error handling client {address}: {e}")
        finally:
            if username:
                self.disconnect_user(username)
            try:
                client_socket.close()
            except:
                pass

    def handle_dm(self, sender, args, sender_socket):
        parts = args.split(' ', 1)
        if len(parts) < 2:
            sender_socket.sendall(b"ERR usage: DM <username> <message>\n")
            return
        
        target_username = parts[0]
        message = parts[1]
        
        with self.lock:
            target_socket = self.clients.get(target_username)
            if target_socket:
                try:
                    target_socket.sendall(f"DM {sender} {message}\n".encode('utf-8'))
                except:
                    pass # Handle broken pipe in broadcast/disconnect
            else:
                 sender_socket.sendall(b"ERR user-not-found\n")

    def disconnect_user(self, username):
        with self.lock:
            if username in self.clients:
                del self.clients[username]
        self.broadcast(f"INFO {username} disconnected")

    def broadcast(self, message, exclude_user=None):
        with self.lock:
            dead_clients = []
            for user, socket in self.clients.items():
                if user != exclude_user:
                    try:
                        socket.sendall(f"{message}\n".encode('utf-8'))
                    except:
                        dead_clients.append(user)
            
            # Clean up broken connections
            for user in dead_clients:
                del self.clients[user]

if __name__ == "__main__":
    # Configuration
    port = int(os.getenv('CHAT_PORT', 4000))
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port number")
            sys.exit(1)

    server = ChatServer(port=port)
    server.start()
