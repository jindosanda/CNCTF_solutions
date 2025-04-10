import socket
import struct
import hashlib

HOST = "ctf.computernetworking.usi.ch"
PORT = 31221

def recv_packet(s):
    header = s.recv(4)
    if len(header) < 4:
        return None, None, None
    version, ptype, length = struct.unpack(">BBH", header)
    payload = s.recv(length)
    return version, ptype, payload

def send_packet(s, ptype, payload):
    header = struct.pack(">BBH", 1, ptype, len(payload))
    s.sendall(header + payload)

with socket.create_connection((HOST, PORT)) as s:
    print("[1] Sending hello...")
    send_packet(s, 0x01, b"hello")

    version, ptype, nonce = recv_packet(s)
    print(f"[2] Received nonce: {nonce.decode()}")

    h = hashlib.sha256(("CTF2025" + nonce.decode()).encode()).hexdigest()[:8].encode()
    print(f"[3] Sending hash: {h.decode()}")
    send_packet(s, 0x02, h)

    version, ptype, response = recv_packet(s)
    if response != b"OK":
        print("[!] Auth failed!")
        exit()

    print("[4] Auth success. Requesting services...")
    send_packet(s, 0x03, b"services?")

    version, ptype, services = recv_packet(s)
    print(f"[5] Received services list: {services.decode()}")

    print("[6] Requesting flag...")
    send_packet(s, 0x04, b"flag")

    version, ptype, flag = recv_packet(s)
    print(f"[🎉] FLAG: {flag.decode()}")
