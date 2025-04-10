import socket
import threading
import struct
import os
import random
import string
import hashlib
from dotenv import load_dotenv

load_dotenv()
HOST = "0.0.0.0"
PORT = 31221
FLAG = os.getenv("FLAG", "CTF{not_the_real_flag}").encode()

def generate_nonce(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def build_packet(ptype, payload):
    return struct.pack(">BBH", 1, ptype, len(payload)) + payload

def parse_packet(data):
    if len(data) < 4:
        return None, None, None
    version, ptype, length = struct.unpack(">BBH", data[:4])
    payload = data[4:4+length]
    return version, ptype, payload

def handle_client(conn, addr):
    print(f"[+] Connection from {addr}")
    try:
        conn.settimeout(10)
        buffer = b""
        step = 0
        nonce = generate_nonce()

        while True:
            chunk = conn.recv(1024)
            if not chunk:
                break
            buffer += chunk
            while len(buffer) >= 4:
                version, ptype, length = struct.unpack(">BBH", buffer[:4])
                if len(buffer) < 4 + length:
                    break
                payload = buffer[4:4+length]
                buffer = buffer[4+length:]

                print(f"[Step {step}] Received packet type=0x{ptype:02X}, payload={payload}")

                if step == 0 and ptype == 0x01 and payload.lower() == b"hello":
                    conn.sendall(build_packet(0x10, nonce.encode()))
                    step += 1
                elif step == 1 and ptype == 0x02:
                    expected = hashlib.sha256(("CTF2025" + nonce).encode()).hexdigest()[:8].encode()
                    if payload == expected:
                        conn.sendall(build_packet(0x11, b"OK"))
                        step += 1
                    else:
                        conn.sendall(build_packet(0x11, b"FAIL"))
                        return
                elif step == 2 and ptype == 0x03:
                    services = b"DNS,HTTP,FLAG"
                    conn.sendall(build_packet(0x12, services))
                    step += 1
                elif step == 3 and ptype == 0x04 and payload == b"flag":
                    conn.sendall(build_packet(0xFF, FLAG))
                    return
                else:
                    conn.sendall(build_packet(0xEE, b"INVALID"))
                    return
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        conn.close()
        print(f"[-] Connection closed from {addr}")

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[+] State Secrets v2 Server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start_server()
