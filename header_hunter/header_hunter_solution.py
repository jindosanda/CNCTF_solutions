import socket
import struct

HOST = "0.0.0.0"  # oppure "ctf.computernetworking.usi.ch"
PORT = 31211
TARGET_TYPE = 0x42
ACK_TYPE = 0xAA

def build_ack(payload):
    length = len(payload)
    header = struct.pack(">BBH", 0x01, ACK_TYPE, length)
    return header + payload

with socket.create_connection((HOST, PORT)) as s:
    s.settimeout(2)  # timeout di ricezione
    buffer = b""
    target_payload = None

    try:
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
    except socket.timeout:
        print("[✓] Packet stream ended (timeout)")

    if target_payload:
        print(f"[✓] Sending ACK for target payload: {target_payload}")
        ack_packet = build_ack(target_payload)
        s.sendall(ack_packet)

        try:
            flag = s.recv(1024).decode(errors="ignore")
            print(f"[🎉] Flag: {flag.strip()}")
        except socket.timeout:
            print("[!] Server did not respond in time.")
    else:
        print("[✗] Target packet not found")
