import socket
import re

HOST = "ctf.computernetworking.usi.ch"
PORT = 31337

with socket.create_connection((HOST, PORT), timeout=1) as s:
    data = s.recv(1024).decode().strip()
    print(f"[SERVER] {data}")

    # Estrai il numero dal messaggio SYN
    match = re.match(r"SYN: (\d+)", data)
    if not match:
        print("Invalid SYN format")
        exit(1)

    seq = int(match.group(1))
    ack = f"ACK: {seq + 1}"
    print(f"[CLIENT] {ack}")
    s.sendall((ack + "\n").encode())

    # Ricevi la flag
    response = s.recv(1024).decode().strip()
    print(f"[SERVER] {response}")
