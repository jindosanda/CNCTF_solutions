import socket
import re
import time

HOST = "0.0.0.0"
PORT = 31203
MESSAGE_LENGTH = 26  # Lunghezza nota del messaggio

def main():
    with socket.create_connection((HOST, PORT)) as s:
        s.settimeout(10)

        received = {}
        buffer = ""

        print("[*] Connecting to server...")

        try:
            while len(received) < MESSAGE_LENGTH:
                data = s.recv(1024).decode()
                if not data:
                    break
                buffer += data

                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    line = line.strip('\r\n')
                    if line.startswith("SEQ:"):
                        match = re.match(r"SEQ: (\d+)\s+\|\s+DATA: (.)", line)
                        if match:
                            seq = int(match.group(1))
                            char = match.group(2)
                            if seq not in received:
                                received[seq] = char
                                print(f"[✓] Received SEQ {seq}: {repr(char)}")
                                s.sendall(f"ACK: {seq}\n".encode())
                    else:
                        print(f"[?] Ignoring unknown line: {line}")
        except socket.timeout:
            print("[!] Timeout while receiving packets.")

        if len(received) < MESSAGE_LENGTH:
            print(f"[✘] Incomplete message ({len(received)}/{MESSAGE_LENGTH} characters).")
            return

        # Ricostruzione e invio
        message = ''.join(received[i] for i in sorted(received))
        print("[DEBUG] Reassembled message:", message)

        # time.sleep(0.3)  # Lascia respirare il server
        s.sendall(f"COMPLETE: {message}\n".encode())

        try:
            response = s.recv(1024).decode(errors="ignore").strip()
            print(f"[SERVER] {response}")
        except socket.timeout:
            print("[!] Timeout while waiting for response.")

if __name__ == "__main__":
    main()
