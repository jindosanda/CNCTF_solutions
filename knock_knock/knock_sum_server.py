import socket
import threading
import base64
import random
import os
from dotenv import load_dotenv

load_dotenv()

HOST = "0.0.0.0"
PORT = 31200
FLAG = os.getenv("FLAG")
TIMEOUT_SECONDS = 3

def encode_b64(msg):
    return base64.b64encode(msg.encode()).decode()

def decode_b64(msg):
    return base64.b64decode(msg.encode()).decode()

def handle_client(conn, addr):
    print(f"[+] Connection from {addr}")
    try:
        conn.settimeout(TIMEOUT_SECONDS)
        greeting = conn.recv(1024).decode().strip()
        if greeting.lower() != "knock knock":
            conn.sendall(b"Wrong greeting!\n")
            return

        a, b = random.randint(10, 99), random.randint(10, 99)
        challenge = f"{a} + {b}"
        encoded_challenge = encode_b64(challenge)
        conn.sendall(f"Solve this: {encoded_challenge}\n".encode())

        answer = conn.recv(1024).decode().strip()
        try:
            decoded = decode_b64(answer)
            if int(decoded) == a + b:
                conn.sendall(f"{FLAG}\n".encode())
            else:
                conn.sendall(b"Wrong answer!\n")
        except Exception:
            conn.sendall(b"Invalid response!\n")

    except socket.timeout:
        conn.sendall(b"Too slow!\n")
    except Exception as e:
        print(f"[!] Error with {addr}: {e}")
    finally:
        conn.close()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[+] Listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start_server()