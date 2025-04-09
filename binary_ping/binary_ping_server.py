import socket
import threading
import struct

HOST = "0.0.0.0"
PORT = 31101
FLAG = "CTF{custom_icmp_sim}"
MAX_PACKET_SIZE = 1024

def handle_client(conn, addr):
    try:
        data = conn.recv(MAX_PACKET_SIZE)
        if len(data) < 6:
            conn.sendall("01 FF ERROR: Malformed Packet\n".encode())
            return

        version, ptype, ident, payload_len, reserved = struct.unpack("!BBHHH", data[:8])
        payload = data[8:]
        
        if version != 0x01 or ptype != 0x08 or len(payload) != payload_len:
            conn.sendall("01 FF ERROR: Malformed Packet\n".encode())
            return

        response = f"01 00 FLAG: {FLAG}\n"
        conn.sendall(response.encode())

    except Exception as e:
        print(f"[!] Error: {e}")
        try:
            conn.sendall("01 FF ERROR: Internal Server Error\n".encode())
        except:
            pass
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
