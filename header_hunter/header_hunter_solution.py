import socket
import struct

HOST = "ctf.computernetworking.usi.ch"
PORT = 31211
TARGET_TYPE = 0x42
ACK_TYPE = 0xAA

def parse_packet(data):
    if len(data) < 4:
        return None, None, None
    version, ptype, length = struct.unpack(">BBH", data[:4])
    payload = data[4:4+length]
    return version, ptype, payload

def build_ack(payload):
    length = len(payload)
    header = struct.pack(">BBH", 0x01, ACK_TYPE, length)
    return header + payload

with socket.create_connection((HOST, PORT)) as s:
    buffer = b""
    target_payload = None

    while True:
        chunk = s.recv(1024)
        if not chunk:
            break
        buffer += chunk

        while len(buffer) >= 4:
            version, ptype, length = struct.unpack(">BBH", buffer[:4])
            if len(buffer) < 4 + length:
                break  # aspetta altri dati

            payload = buffer[4:4+length]
            print(f"[DEBUG] Received packet type=0x{ptype:02X}, length={length}, payload={payload}")

            if ptype == TARGET_TYPE:
                target_payload = payload

            buffer = buffer[4+length:]

    if target_payload:
        print(f"[✓] Sending ACK for target payload: {target_payload}")
        ack_packet = build_ack(target_payload)
        s.sendall(ack_packet)

        try:
            flag = s.recv(1024).decode(errors="ignore")
            print(f"[🎉] Flag: {flag.strip()}")
        except Exception as e:
            print(f"[!] Error receiving flag: {e}")
    else:
        print("[✗] Target packet not found")
