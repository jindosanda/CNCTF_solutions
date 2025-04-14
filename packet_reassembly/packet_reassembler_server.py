import socket
import threading
import random
import time
import os
from dotenv import load_dotenv

load_dotenv()

HOST = "0.0.0.0"
PORT = 31204
FLAG = os.getenv("FLAG", "CTF{default_flag}")
MESSAGE = os.getenv("MESSAGE", "DEFAULT_MESSAGE")

# def handle_client(conn, addr):
#     print(f"[+] Connection from {addr}")
#     conn.settimeout(5)
#     received_acks = set()
#     to_send = list(enumerate(MESSAGE))
#     random.shuffle(to_send)
#     alive = True  # flag condiviso

#     def sender():
#         nonlocal alive
#         try:
#             while alive:
#                 for seq, char in to_send:
#                     if not alive:
#                         break
#                     if seq in received_acks:
#                         continue
#                     if random.random() < 0.2:
#                         continue  # simulate packet loss
#                     try:
#                         if random.random() < 0.3:
#                             # simulate duplicate packets
#                             for _ in range(2):
#                                 conn.sendall(f"SEQ: {seq} | DATA: {char}\n".encode())
#                                 time.sleep(0.05)
#                         else:
#                             conn.sendall(f"SEQ: {seq} | DATA: {char}\n".encode())
#                             time.sleep(0.05)
#                     except (BrokenPipeError, OSError):
#                         alive = False
#                         break
#                 time.sleep(1)
#         except Exception as e:
#             print(f"[!] Sender error for {addr}: {e}")

#     thread = threading.Thread(target=sender, daemon=True)
#     thread.start()

#     try:
#         while True:
#             data = conn.recv(1024)
#             if not data:
#                 break
#             lines = data.decode().splitlines()
#             for line in lines:
#                 if line.startswith("ACK:"):
#                     try:
#                         ack = int(line.split(":")[1].strip())
#                         received_acks.add(ack)
#                     except:
#                         pass
#                 elif line.startswith("COMPLETE:"):
#                     msg = line.split(":", 1)[1].strip()
#                     if msg == MESSAGE:
#                         conn.sendall(f"FLAG: {FLAG}\n".encode())
#                     else:
#                         conn.sendall(b"WRONG MESSAGE\n")
#                     return
#     except Exception as e:
#         print(f"[!] Error with {addr}: {e}")
#     finally:
#         alive = False
#         conn.close()

# def start_server():
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.bind((HOST, PORT))
#         s.listen()
#         print(f"[+] Listening on {HOST}:{PORT}")
#         while True:
#             conn, addr = s.accept()
#             threading.Thread(target=handle_client, args=(conn, addr)).start()

# if __name__ == "__main__":
#     start_server()


def handle_client(conn, addr):
    print(f"[+] Connection from {addr}")
    conn.settimeout(5)

    received_acks = set()  # shared between receiver and sender
    alive = True           # shared flag

    def sender():
        window_size = 5
        base = 0
        total_packets = len(MESSAGE)

        while alive and base < total_packets:
            # Determine the boundaries of our sliding window
            window_end = min(base + window_size, total_packets)

            # Build a list of unacknowledged packets in the current window
            unacked_in_window = [
                seq for seq in range(base, window_end)
                if seq not in received_acks
            ]
            random.shuffle(unacked_in_window)

            # Send (or re-send) each unacked packet in random order
            for seq in unacked_in_window:
                # If the connection is dead, stop sending
                if not alive:
                    return

                # Simulate packet loss
                if random.random() < 0.2:
                    continue

                # Prepare data
                data_str = f"SEQ: {seq} | DATA: {MESSAGE[seq]}\n"
                try:
                    # Simulate random duplication
                    if random.random() < 0.3:
                        for _ in range(2):
                            conn.sendall(data_str.encode())
                            time.sleep(0.05)
                    else:
                        conn.sendall(data_str.encode())
                        time.sleep(0.05)
                except (BrokenPipeError, OSError):
                    return  # connection lost, exit sender

            # Small delay between rounds
            time.sleep(1)

            # Slide the window forward past any newly ACKed packets at the front
            while base < total_packets and base in received_acks:
                base += 1

    # Start the sender thread
    send_thread = threading.Thread(target=sender, daemon=True)
    send_thread.start()

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            lines = data.decode().splitlines()
            for line in lines:
                if line.startswith("ACK:"):
                    try:
                        ack = int(line.split(":")[1].strip())
                        received_acks.add(ack)
                    except:
                        pass

                elif line.startswith("COMPLETE:"):
                    msg = line.split(":", 1)[1].strip()
                    if msg == MESSAGE:
                        conn.sendall(f"FLAG: {FLAG}\n".encode())
                    else:
                        conn.sendall(b"WRONG MESSAGE\n")
                    return

    except Exception as e:
        print(f"[!] Error with {addr}: {e}")
    finally:
        alive = False
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