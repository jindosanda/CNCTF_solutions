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
    target_payload = b"seek_and_ack"
    target_type = 0x42
    ack_type = 0xAA
    ack_timeout = 15
    
    try:
        conn.settimeout(ack_timeout)
        
        # Prepara i pacchetti
        packets = []
        target_packet = generate_packet(0x01, target_type, target_payload)
        flag_packet = generate_packet(0x01, 0xFF, FLAG)
        target_pos = random.randint(0, 29)

        for i in range(30):
            if i == target_pos:
                packets.append(target_packet)
            else:
                dummy_payload = bytes([random.randint(65, 90) for _ in range(random.randint(5, 20))])
                packets.append(generate_packet(0x01, random.randint(0x00, 0x41), dummy_payload))

        # Invia pacchetti in ordine casuale
        for pkt in packets:
            try:
                time.sleep(random.uniform(0.05, 0.15))
                conn.sendall(pkt)
            except BrokenPipeError:
                print(f"[!] Broken pipe when sending to {addr}")
                return

        # Aspetta ACK dal client
        try:
            data = conn.recv(1024)
            if len(data) < 4:
                return

            version, ptype, length = struct.unpack(">BBH", data[:4])
            payload = data[4:4+length]

            if ptype == ack_type and payload == target_payload:
                print(f"[✓] Correct ACK received from {addr}")
                conn.sendall(flag_packet)
            else:
                print(f"[✗] Invalid ACK from {addr}")
                conn.sendall(b"Wrong ACK\n")

        except socket.timeout:
            print(f"[!] Timeout waiting for ACK from {addr}")
        except Exception as e:
            print(f"[!] Error receiving ACK from {addr}: {e}")

    except (socket.timeout, ConnectionResetError) as e:
        print(f"[!] Connection error with {addr}: {e}")
    finally:
        conn.close()
        print(f"[-] Connection closed from {addr}")

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[+] Header Hunter Server running on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()