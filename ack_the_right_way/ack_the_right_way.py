import socket
import threading
import random

HOST = "0.0.0.0"
PORT = 31337
FLAG = "CTF{ACK_numb3r_is_correct}"
TIMEOUT_SECONDS = 2  # Impedisce l’interazione manuale

def handle_client(conn, addr):
    print(f"[+] Connection from {addr}")
    seq = random.randint(1000, 9999)

    try:
        conn.settimeout(TIMEOUT_SECONDS)
        conn.sendall(f"SYN: {seq}\n".encode())

        ack_msg = conn.recv(1024).decode().strip()
        expected_ack = f"ACK: {seq + 1}"

        if ack_msg == expected_ack:
            conn.sendall(f"{FLAG}\n".encode())
        else:
            conn.sendall(b"Wrong ACK!\n")
            conn.close()

    except socket.timeout:
        print(f"[!] Timeout from {addr}")
        conn.sendall(b"Too slow my friend!\n")
        conn.close()

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
