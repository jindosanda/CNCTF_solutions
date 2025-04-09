import socket
import re

HOST = "ctf.computernetworking.usi.ch"
PORT = 31200

with socket.create_connection((HOST, PORT), timeout=2) as s:
    # Step 1: invia il saluto
    s.sendall(b"knock knock\n")
    
    # Step 2: riceve la domanda
    challenge = s.recv(1024).decode().strip()
    print(f"[SERVER] {challenge}")
    
    # Step 3: estrai i numeri dalla stringa
    match = re.search(r"What is (\d+)\s*\+\s*(\d+)", challenge)
    if not match:
        print("Unexpected challenge format")
        exit(1)
    
    a, b = int(match.group(1)), int(match.group(2))
    result = str(a + b)

    # Step 4: invia la risposta
    s.sendall((result + "\n").encode())

    # Step 5: riceve la flag o errore
    response = s.recv(1024).decode().strip()
    print(f"[SERVER] {response}")
