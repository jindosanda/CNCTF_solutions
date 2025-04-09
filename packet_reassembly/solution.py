import socket
import time

host = "ctf.computernetworking.usi.ch"
port = 31204

buffer = {}
received = set()
expected_len = 36  # known length of message

with socket.create_connection((host, port), timeout=2) as s:
    s.settimeout(1)
    start = time.time()
    while len(buffer) < expected_len and time.time() - start < 20:
        try:
            data = s.recv(1024).decode().splitlines()
            for line in data:
                if line.startswith("SEQ:"):
                    try:
                        parts = line.split("|")
                        seq = int(parts[0].split(":")[1].strip())
                        char = parts[1].split(":")[1].strip()
                        if seq not in buffer:
                            buffer[seq] = char
                        s.sendall(f"ACK: {seq}\n".encode())
                    except:
                        continue
        except socket.timeout:
            continue

    if len(buffer) == expected_len:
        message = "".join(buffer[i] for i in sorted(buffer))
        s.sendall(f"COMPLETE: {message}\n".encode())
        print("Message reconstructed:", message)
        try:
            print(s.recv(1024).decode())
        except:
            pass
    else:
        print("Failed to reconstruct the message in time.")
