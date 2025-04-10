import socket
import struct

HOST = "ctf.computernetworking.usi.ch"
PORT = 31211

def read_exact(sock, size):
    buf = b""
    while len(buf) < size:
        chunk = sock.recv(size - len(buf))
        if not chunk:
            raise ConnectionError("Connection closed prematurely")
        buf += chunk
    return buf

def main():
    with socket.create_connection((HOST, PORT)) as s:
        try:
            while True:
                header = read_exact(s, 4)
                version, ptype, length = struct.unpack(">BBH", header)

                payload = read_exact(s, length)

                if version != 0x01:
                    continue

                if ptype == 0xFF:
                    print("[✓] Found flag packet!")
                    print("🎉 Flag:", payload.decode())
                    break

        except Exception as e:
            print("[!] Error:", e)

if __name__ == "__main__":
    main()