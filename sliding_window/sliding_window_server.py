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
        packets = [(i, c) for i, c in enumerate(MESSAGE)]
        random.shuffle(packets)

        print("[*] Sending packets...")
        for seq, char in packets:
            conn.sendall(f"SEQ: {seq} | DATA: {char}\n".encode())

        acked = set()
        buffer = ""
        message_received = False

        while not message_received:
            try:
                data = conn.recv(1024).decode()
                if not data:
                    break
                buffer += data
            except socket.timeout:
                print("[!] Timeout while receiving data.")
                break

            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                line = line.strip()
                if line.startswith("ACK:"):
                    try:
                        ack_num = int(line.split(":")[1].strip())
                        acked.add(ack_num)
                        print(f"[✓] ACK received: {ack_num}")
                    except ValueError:
                        print("[!] Invalid ACK format.")
                elif line.startswith("COMPLETE:"):
                    submitted = line.split(":", 1)[1].strip()
                    print(f"[↪] COMPLETE received: {submitted}")
                    if submitted == MESSAGE:
                        conn.sendall(f"FLAG: {FLAG}\n".encode())
                        print("[🏁] Flag sent.")
                    else:
                        conn.sendall(b"Wrong message!\n")
                        print("[✘] Wrong message submitted.")
                    message_received = True
                else:
                    print(f"[?] Unknown line: {line}")

        if len(acked) == len(MESSAGE):
            print("[✓] All ACKs received.")
        else:
            print(f"[!] Only {len(acked)}/{len(MESSAGE)} ACKs received.")

    except Exception as e:
        print(f"[!] Error with {addr}: {e}")
    finally:
        conn.close()
        print(f"[-] Connection closed from {addr}")


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[+] Sliding Window Server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start_server()
