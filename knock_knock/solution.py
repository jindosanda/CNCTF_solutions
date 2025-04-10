import socket
import base64
import re

HOST = "ctf.computernetworking.usi.ch"
PORT = 31200

def decode_b64(msg):
    return base64.b64decode(msg.encode()).decode()

def encode_b64(msg):
    return base64.b64encode(msg.encode()).decode()

with socket.create_connection((HOST, PORT)) as s:
    s.sendall(b"knock knock\n")
    challenge = s.recv(1024).decode().strip()
    print("[SERVER]", challenge)

    b64_expr = re.search(r"Solve this: ([A-Za-z0-9+/=]+)", challenge).group(1)
    expr = decode_b64(b64_expr)

    try:
        result = str(eval(expr))
        b64_result = encode_b64(result)
        s.sendall(f"{b64_result}\n".encode())
        flag = s.recv(1024).decode().strip()
        print("[SERVER]", flag)
    except Exception as e:
        print("[!] Error:", e)