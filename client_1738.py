# client_1738.py
# IE2102 - Network Programming Assignment
# Registration: IT24101738
# Usage: python3 client_1738.py

import socket

HOST = "127.0.0.1"
PORT = 50738

def send_framed(sock, message):
    """Send framed message: LEN:<n>\n<payload>"""
    payload = message.encode()
    header = f"LEN:{len(payload)}\n".encode()
    sock.sendall(header + payload)

def recv_response(sock):
    """Receive one response line from server"""
    data = b""
    while True:
        chunk = sock.recv(1024)
        if not chunk:
            break
        data += chunk
        if b"\n" in data:
            break
    return data.decode().strip()

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    print(f"Connected to server at {HOST}:{PORT}")
    print("Commands: REGISTER <user> <pass> | LOGIN <user> <pass> | LOGOUT | quit")
    print("-" * 60)

    while True:
        try:
            cmd = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nDisconnected.")
            break

        if not cmd:
            continue

        if cmd.lower() == "quit":
            break

        send_framed(sock, cmd)
        response = recv_response(sock)
        print(f"<- {response}")

    sock.close()

if __name__ == "__main__":
    main()
