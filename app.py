# Auto-install required packages if not present
import subprocess
import sys

def install_if_missing(package):
    try:
        __import__(package)
    except ImportError:
        print(f"[+] Installing missing package: {package}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Check and install dependencies
install_if_missing("flask")
install_if_missing("pyautogui")
install_if_missing("qrcode_terminal")

# Now import after install check
from flask import Flask, render_template, request
import pyautogui
import qrcode_terminal
import socket

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('control.html')

@app.route('/action', methods=['POST'])
def action():
    data = request.get_json()
    action = data.get('action')

    try:
        if action == 'move_up':
            pyautogui.moveRel(0, -25)
        elif action == 'move_down':
            pyautogui.moveRel(0, 25)
        elif action == 'move_left':
            pyautogui.moveRel(-25, 0)
        elif action == 'move_right':
            pyautogui.moveRel(25, 0)
        elif action == 'click_left':
            pyautogui.click(button='left')
        elif action == 'click_right':
            pyautogui.click(button='right')
    except Exception as e:
        print("Mouse error:", e)

    return '', 204

@app.route('/keypress', methods=['POST'])
def keypress():
    data = request.get_json()
    key = data.get('key')

    try:
        pyautogui.press(key)
    except Exception as e:
        print("Keypress error:", e)

    return '', 204

# Get local LAN IP to show QR
def get_lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

if __name__ == '__main__':
    lan_ip = get_lan_ip()
    url = f'http://{lan_ip}:5000'
    print(f"\n[+] Flask server running at {url}")
    qrcode_terminal.draw(url)

    app.run(host='0.0.0.0', port=5000, debug=True)
