import socket
import struct

host = "ctf.computernetworking.usi.ch"
port = 31101

payload = b"pingme"
payload_len = len(payload)
header = struct.pack("!BBHHH", 0x01, 0x08, 0xdead, payload_len, 0)
packet = header + payload

assert len(packet) == 8 + payload_len, "Invalid packet size"

with socket.create_connection((host, port), timeout=3) as s:
    s.sendall(packet)
    response = s.recv(1024)
    print(response.decode())
