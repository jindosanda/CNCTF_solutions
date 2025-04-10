import socket
import threading
import struct
import random
import os
from dotenv import load_dotenv
import time

# Carica variabili da .env
load_dotenv()

HOST = "0.0.0.0"
PORT = 31211
FLAG = os.getenv("FLAG", "CTF{not_the_real_flag}").encode()

def generate_packet(version, ptype, payload):
    length = len(payload)
    header = struct.pack(">BBH", version, ptype, length)
    return header + payload

def handle_client(conn, addr):
    print(f"[+] Connection from {addr}")
    try:
        conn.settimeout(10)
        packets = []

        # Crea il pacchetto speciale da riconoscere
        target_payload = b"seek_and_ack"
        target_packet = generate_packet(0x01, 0x42, target_payload)
        target_position = random.randint(0, 29)

        for i in range(30):
            if i == target_position:
                packets.append(target_packet)
            else:
                dummy_payload = bytes([random.randint(65, 90) for _ in range(random.randint(5, 20))])
                pkt = generate_packet(0x01, random.randint(0x00, 0x41), dummy_payload)
                packets.append(pkt)

        # Invia i pacchetti uno per volta con ritardo
        for pkt in packets:
            time.sleep(random.uniform(0.05, 0.15))
            conn.sendall(pkt)

        # Attende la risposta del client
        ack_data = conn.recv(1024)
        if len(ack_data) < 4:
            conn.sendall(b"Invalid ACK\n")
            return

        version, ptype, length = struct.unpack(">BBH", ack_data[:4])
        payload = ack_data[4:]

        if ptype == 0xAA and payload == target_payload:
            print("[✓] Valid ACK received, sending flag")
            time.sleep(0.2)
            flag_packet = generate_packet(0x01, 0xFF, FLAG)
            conn.sendall(flag_packet)
        else:
            print("[✗] Invalid ACK or wrong payload")
            conn.sendall(b"Wrong ACK or payload\n")

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
