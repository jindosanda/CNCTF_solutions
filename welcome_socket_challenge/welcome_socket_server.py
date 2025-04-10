import socket

HOST = "0.0.0.0"
PORT = 31000
FLAG = "CTF{hello_from_the_socket}"

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[+] Welcome Socket Server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"[+] Connection from {addr}")
                conn.sendall(f"Hello challenger! Your flag is: {FLAG}\n".encode())

if __name__ == "__main__":
    start_server()
