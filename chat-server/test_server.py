import socket
import time
import threading
import sys

def receive_messages(sock, messages):
    buffer = ""
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            buffer += data.decode()
            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)
                messages.append(line)
        except:
            break

def test_server():
    host = 'localhost'
    port = 4000
    
    # Client 1
    c1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c1.connect((host, port))
    c1_msgs = []
    t1 = threading.Thread(target=receive_messages, args=(c1, c1_msgs))
    t1.start()
    
    # Client 2
    c2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c2.connect((host, port))
    c2_msgs = []
    t2 = threading.Thread(target=receive_messages, args=(c2, c2_msgs))
    t2.start()

    time.sleep(0.5)
    
    # Test LOGIN
    print("Testing LOGIN...")
    c1.sendall(b"LOGIN Alice\n")
    c2.sendall(b"LOGIN Bob\n")
    time.sleep(0.5)
    
    assert "OK" in c1_msgs
    assert "OK" in c2_msgs
    print("LOGIN passed")
    
    # Test MSG (Broadcast)
    print("Testing Broadcast...")
    c1.sendall(b"MSG Hello World\n")
    time.sleep(0.5)
    
    # Check if Bob received Alice's message
    found = False
    for msg in c2_msgs:
        if "MSG Alice Hello World" in msg:
            found = True
            break
    if not found:
        print(f"Broadcast failed. Bob's messages: {c2_msgs}")
        return
    print("Broadcast passed")
    
    # Test DM
    print("Testing DM...")
    c2.sendall(b"DM Alice SecretMsg\n")
    time.sleep(0.5)
    
    found_dm = False
    for msg in c1_msgs:
        if "DM Bob SecretMsg" in msg:
            found_dm = True
            break
    if not found_dm:
        print(f"DM failed. Alice's messages: {c1_msgs}")
        return
    print("DM passed")
    
    # Test WHO
    print("Testing WHO...")
    c1.sendall(b"WHO\n")
    time.sleep(0.5)
    
    found_who = False
    for msg in c1_msgs:
        if "USERS" in msg and "Alice" in msg and "Bob" in msg:
            found_who = True
            break
    if not found_who:
        print(f"WHO failed. Alice's messages: {c1_msgs}")
        return
    print("WHO passed")
    
    # Test Disconnect
    print("Testing Disconnect...")
    c1.close()
    time.sleep(0.5)
    
    found_disco = False
    for msg in c2_msgs:
        if "INFO Alice disconnected" in msg:
            found_disco = True
            break
    if not found_disco:
        print(f"Disconnect notification failed. Bob's messages: {c2_msgs}")
        return
    print("Disconnect notification passed")
    
    c2.close()
    print("All tests passed!")

if __name__ == "__main__":
    try:
        test_server()
    except Exception as e:
        print(f"Test failed with exception: {e}")
        sys.exit(1)
