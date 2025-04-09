import socket
import threading
import random

HOST = "0.0.0.0"
PORT = 31203
MESSAGE = "C0mput3r N3work1ng 1s C00l"
FLAG = "CTF{ordered_delivery_wins}"

def handle_client(conn, addr):
    print(f"[+] Connection from {addr}")
    try:
        conn.settimeout(10)

        # Crea pacchetti (seq_num, char)
        packets = [(i, c) for i, c in enumerate(MESSAGE)]
        random.shuffle(packets)

        # Invia pacchetti fuori ordine
        for seq, char in packets:
            conn.sendall(f"SEQ: {seq} | DATA: {char}\n".encode())

        # Riceve gli ACK
        acked = set()
        while len(acked) < len(MESSAGE):
            ack_line = conn.recv(1024).decode().strip()
            if ack_line.startswith("ACK:"):
                try:
                    ack_num = int(ack_line.split(":")[1].strip())
                    acked.add(ack_num)
                except ValueError:
                    continue

        # Riceve il messaggio completo
        final_line = conn.recv(1024).decode().strip()
        if final_line.startswith("COMPLETE:"):
            submitted = final_line.split(":", 1)[1].strip()
            if submitted == MESSAGE:
                conn.sendall(f"FLAG: {FLAG}\n".encode())
            else:
                conn.sendall(b"Wrong message!\n")
    except Exception as e:
        print(f"[!] Error with {addr}: {e}")
    finally:
        conn.close()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[+] Listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start_server()
