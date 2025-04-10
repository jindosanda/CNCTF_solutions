import socket
import threading
import struct
import random
import os
from dotenv import load_dotenv

# Carica variabili da .env
load_dotenv()

HOST = "0.0.0.0"
PORT = 31211
FLAG = os.getenv("FLAG").encode()

def generate_packet(version, ptype, payload):
    length = len(payload)
    header = struct.pack(">BBH", version, ptype, length)
    return header + payload

def handle_client(conn, addr):
    print(f"[+] Connection from {addr}")
    try:
        conn.settimeout(10)
        packets = []

        # Inserisce il pacchetto contenente la flag in una posizione casuale
        flag_packet = generate_packet(0x01, 0xFF, FLAG)
        flag_position = random.randint(0, 29)

        for i in range(30):
            if i == flag_position:
                packets.append(flag_packet)
            else:
                dummy_payload = bytes([random.randint(65, 90) for _ in range(random.randint(5, 20))])
                pkt = generate_packet(0x01, random.randint(0x00, 0xFE), dummy_payload)
                packets.append(pkt)

        # Invia tutti i pacchetti
        for pkt in packets:
            conn.sendall(pkt)

    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        conn.close()
        print(f"[-] Connection closed from {addr}")

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[+] Header Hunter Server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start_server()
