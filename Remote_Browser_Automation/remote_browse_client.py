import socket

SERVER_IP = '192.168.1.100'  # Replace with your server IP
SERVER_PORT = 9999

def send_search(term):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER_IP, SERVER_PORT))
            s.sendall(f"SEARCH:{term}\n".encode())
            print(f"[+] Sent search: {term}")
    except Exception as e:
        print(f"[!] Failed to send: {e}")

if __name__ == "__main__":
    while True:
        search = input("Enter YouTube search (or 'exit'): ").strip()
        if search.lower() == "exit":
            break
        if search:
            send_search(search)
