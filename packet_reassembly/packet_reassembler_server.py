import socket
import threading
import random
import time
import os
from dotenv import load_dotenv

load_dotenv()

HOST = "0.0.0.0"
PORT = 31204
FLAG = os.getenv("FLAG", "CTF{default_flag}")
MESSAGE = os.getenv("MESSAGE", "DEFAULT_MESSAGE")

def handle_client(conn, addr):
    print(f"[+] Connection from {addr}")
    conn.settimeout(5)
    received_acks = set()
    to_send = list(enumerate(MESSAGE))
    random.shuffle(to_send)
    alive = True  # flag condiviso

    def sender():
        nonlocal alive
        try:
            while alive:
                for seq, char in to_send:
                    if not alive:
                        break
                    if seq in received_acks:
                        continue
                    if random.random() < 0.2:
                        continue  # simulate packet loss
                    try:
                        if random.random() < 0.3:
                            # simulate duplicate packets
                            for _ in range(2):
                                conn.sendall(f"SEQ: {seq} | DATA: {char}\n".encode())
                                time.sleep(0.05)
                        else:
                            conn.sendall(f"SEQ: {seq} | DATA: {char}\n".encode())
                            time.sleep(0.05)
                    except (BrokenPipeError, OSError):
                        alive = False
                        break
                time.sleep(1)
        except Exception as e:
            print(f"[!] Sender error for {addr}: {e}")

    thread = threading.Thread(target=sender, daemon=True)
    thread.start()

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            lines = data.decode().splitlines()
            for line in lines:
                if line.startswith("ACK:"):
                    try:
                        ack = int(line.split(":")[1].strip())
                        received_acks.add(ack)
                    except:
                        pass
                elif line.startswith("COMPLETE:"):
                    msg = line.split(":", 1)[1].strip()
                    if msg == MESSAGE:
                        conn.sendall(f"FLAG: {FLAG}\n".encode())
                    else:
                        conn.sendall(b"WRONG MESSAGE\n")
                    return
    except Exception as e:
        print(f"[!] Error with {addr}: {e}")
    finally:
        alive = False
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
