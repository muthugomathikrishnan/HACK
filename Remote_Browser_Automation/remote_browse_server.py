import socket
import threading
import urllib.parse
import webbrowser

HOST = '0.0.0.0'
PORT = 9999

stop_flag = False

def handle_client(conn, addr):
    global stop_flag
    print(f"[+] Connection from {addr}")

    with conn:
        while not stop_flag:
            try:
                data = conn.recv(1024).decode().strip()
                if not data:
                    break

                if data.startswith("SEARCH:"):
                    search_term = data.replace("SEARCH:", "")
                    print(f"[>] Search received: {search_term}")
                    encoded = urllib.parse.quote_plus(search_term)
                    url = f"https://www.youtube.com/results?search_query={encoded}"
                    webbrowser.open(url)
            except Exception as e:
                print(f"[!] Error: {e}")
                break

def input_listener():
    global stop_flag
    while True:
        command = input("[Server] Type 'stop' to end: ").strip().lower()
        if command == "stop":
            stop_flag = True
            print("[*] Stopping server...")
            break

def main():
    threading.Thread(target=input_listener, daemon=True).start()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[*] Server listening on port {PORT}...")

        while not stop_flag:
            try:
                s.settimeout(1.0)
                conn, addr = s.accept()
                threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
            except socket.timeout:
                continue
            except Exception as e:
                print(f"[!] Server error: {e}")

if __name__ == "__main__":
    main()
