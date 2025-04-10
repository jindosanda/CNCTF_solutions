import socket
import struct

HOST = "ctf.computernetworking.usi.ch"
PORT = 31211

def recv_all(s, expected_total_bytes=1024):
    buffer = b""
    while True:
        part = s.recv(1024)
        if not part:
            break
        buffer += part
        if len(buffer) >= expected_total_bytes:
            break
    return buffer

def parse_packets(data):
    i = 0
    packets = []
    while i + 4 <= len(data):
        header = data[i:i+4]
        version, ptype, length = struct.unpack(">BBH", header)
        if i + 4 + length > len(data):
            break
        payload = data[i+4:i+4+length]
        packets.append((version, ptype, length, payload))
        i += 4 + length
    return packets

def build_ack(payload):
    version = 0x01
    ptype = 0xAA
    length = len(payload)
    header = struct.pack(">BBH", version, ptype, length)
    return header + payload

with socket.create_connection((HOST, PORT)) as s:
    print("[+] Connected to server")

    # Step 1: riceve pacchetti
    data = recv_all(s)
    packets = parse_packets(data)

    # Step 2: cerca il pacchetto target
    for version, ptype, length, payload in packets:
        if ptype == 0x42:
            print("[✓] Found target packet with type 0x42")
            ack_pkt = build_ack(payload)
            s.sendall(ack_pkt)
            break
    else:
        print("[!] Target packet not found")
        exit()

    # Step 3: riceve la flag
    response = s.recv(1024)
    if len(response) >= 4:
        v, t, l = struct.unpack(">BBH", response[:4])
        payload = response[4:]
        if t == 0xFF:
            print("🎉 Flag:", payload.decode())
        else:
            print("[!] Unexpected response:", payload.decode(errors='ignore'))
    else:
        print("[!] No response
