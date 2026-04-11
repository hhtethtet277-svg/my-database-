import os
import socket
import threading
import requests
import urllib3
from colorama import Fore, Back, Style, init

# SSL Warning ပိတ်ရန်နှင့် Colorama စတင်ရန်
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)

# ===============================
# CONFIGURATION
# ===============================
GITHUB_URL = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/main/key.txt"
USER_KEY = "AF8BE771-03B" 
PROXY_PORT = 8080

def h_banner():
    os.system('clear')
    print(f"{Fore.MAGENTA}{'='*55}")
    print(f"{Fore.CYAN}  █████╗ ██╗      █████╗ ██████╗ ██████╗ ██╗███╗   ██╗")
    print(f"{Fore.CYAN} ██╔══██╗██║     ██╔══██╗██╔══██╗██╔══██╗██║████╗  ██║")
    print(f"{Fore.CYAN} ███████║██║     ███████║██║  ██║██║  ██║██║██╔██╗ ██║")
    print(f"{Fore.CYAN} ██╔══██║██║     ██╔══██║██║  ██║██║  ██║██║██║╚██╗██║")
    print(f"{Fore.CYAN} ██║  ██║███████╗██║  ██║██████╔╝██████╔╝██║██║ ╚████║")
    print(f"{Fore.CYAN} ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝ ╚═════╝ ╚═╝╚═╝  ╚════╝")
    print(f"{Fore.MAGENTA}{'='*55}")
    print(f"{Fore.WHITE}{Back.BLUE}      ALADDIN HTTPS BYPASS | OWNER: MOE YU      ")
    print(f"{Style.RESET_ALL}{Fore.MAGENTA}{'='*55}\n")

# ===============================
# HTTPS PROXY ENGINE (For Wi-Fi Settings)
# ===============================
def handle_client(client_socket):
    try:
        # Request ကို လက်ခံခြင်း
        request = client_socket.recv(4096).decode('latin-1')
        if not request: return
        
        first_line = request.split('\n')[0]
        method = first_line.split(' ')[0]
        
        # HTTPS လမ်းကြောင်းများကို တိုက်ရိုက်ချိတ်ပေးခြင်း
        if method == "CONNECT":
            host_port = first_line.split(' ')[1]
            host, port = host_port.split(':')
            
            # Target Server သို့ ချိတ်ဆက်ခြင်း
            remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote_socket.connect((host, int(port)))
            client_socket.send(b"HTTP/1.1 200 Connection Established\r\n\r\n")
            
            # Data Bridge လုပ်ခြင်း
            def bridge(src, dest):
                try:
                    while True:
                        data = src.recv(4096)
                        if not data: break
                        dest.sendall(data)
                except: pass

            threading.Thread(target=bridge, args=(client_socket, remote_socket), daemon=True).start()
            bridge(remote_socket, client_socket)
        else:
            # ရိုးရိုး HTTP Requests များအတွက်
            client_socket.send(b"HTTP/1.1 501 Unsupported Method\r\n\r\n")
    except: pass
    finally: client_socket.close()

def start_engine():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('0.0.0.0', PROXY_PORT))
        server.listen(10)
        print(f"{Fore.GREEN}[✔] Aladdin Engine is Live on Port: {PROXY_PORT}")
        print(f"{Fore.YELLOW}[i] Wi-Fi Proxy: 127.0.0.1 | Port: {PROXY_PORT}")
        
        while True:
            client, addr = server.accept()
            # print(f"{Fore.BLACK}{Back.WHITE} [LOG] Connection from: {addr[0]} ") # Log ကြည့်ချင်လျှင် ဖွင့်ပါ
            threading.Thread(target=handle_client, args=(client,), daemon=True).start()
    except Exception as e:
        print(f"{Fore.RED}[!] Server Error: {e}")

# ===============================
# LICENSE VERIFICATION
# ===============================
def verify_license():
    h_banner()
    print(f"{Fore.YELLOW}[i] Validating Access...")
    try:
        response = requests.get(GITHUB_URL, timeout=15, verify=False)
        if response.status_code == 200:
            raw_text = response.text.strip()
            if "|" in raw_text:
                key_from_server, exp_date_str = raw_text.split("|")
                if key_from_server.strip() == USER_KEY:
                    print(f"{Fore.CYAN}[+] Status: {Fore.BLACK}{Back.GREEN} ACTIVE ")
                    print(f"{Fore.WHITE}└─ Security Date: {Fore.YELLOW}{exp_date_str.strip()}")
                    return True
        return False
    except:
        return False

if __name__ == "__main__":
    if verify_license():
        start_engine()
    else:
        print(f"{Fore.RED}\n❌ ACCESS DENIED: INVALID KEY")
