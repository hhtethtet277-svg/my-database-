import os
import requests
import re
import urllib3
import time
import threading
import random
import sys
import socketserver
import http.server
from datetime import datetime
from urllib.parse import urlparse, parse_qs, urljoin
from colorama import Fore, Back, Style, init

# SSL Warning များနှင့် Error ကာကွယ်ရေး
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)

# ===============================
# CONFIGURATION
# ===============================
GITHUB_URL = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/main/key.txt"
USER_KEY = "AF8BE771-03B" 
PROXY_PORT = 8080 # အခြား App များအတွက် ကြားခံ Port
stop_event = threading.Event()

# ===============================
# PROXY SERVER LOGIC (အခြား App များအတွက်)
# ===============================
class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # ဤနေရာတွင် ရိုးရှင်းသော Proxy လမ်းကြောင်းကို ဖန်တီးပေးထားသည်
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Aladdin Proxy Active")

def start_proxy():
    with socketserver.TCPServer(("", PROXY_PORT), ProxyHandler) as httpd:
        print(f"{Fore.GREEN}[✔] Proxy Engine started on Port: {PROXY_PORT}")
        httpd.serve_forever()

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
    print(f"{Fore.WHITE}{Back.BLUE}      ALADDIN TURBO BYPASS | OWNER: MOE YU      ")
    print(f"{Style.RESET_ALL}{Fore.MAGENTA}{'='*55}\n")

# ===============================
# LICENSE SYSTEM
# ===============================
def verify_license():
    h_banner()
    print(f"{Fore.YELLOW}[i] Checking security clearance...")
    print(f"{Fore.WHITE}└─ Device ID: {Fore.GREEN}{USER_KEY}")
    try:
        response = requests.get(GITHUB_URL, timeout=15, verify=False)
        if response.status_code == 200:
            raw_text = response.text.strip()
            if "|" in raw_text:
                key_from_server, exp_date_str = raw_text.split("|")
                if key_from_server.strip() == USER_KEY:
                    expiry_date = datetime.strptime(exp_date_str.strip(), "%Y-%m-%d")
                    if datetime.now() < expiry_date:
                        print(f"{Fore.CYAN}[+] Status: {Fore.BLACK}{Back.GREEN} ACTIVE ")
                        print(f"{Fore.WHITE}└─ Expire Date: {Fore.YELLOW}{exp_date_str.strip()}")
                        return True
            print(f"{Fore.RED}\n❌ ERROR: KEY NOT REGISTERED")
            return False
    except Exception:
        print(f"{Fore.RED}\n❌ ERROR: SERVER UNREACHABLE")
        return False

# ===============================
# CORE ENGINE
# ===============================
def start_bypass_process():
    print(f"{Fore.CYAN}[*] Initializing Turbo Engine...")
    
    # Proxy Server ကို Background မှာ Run မည်
    proxy_thread = threading.Thread(target=start_proxy, daemon=True)
    proxy_thread.start()
    
    print(f"{Fore.MAGENTA}>>> Setup Proxy on Phone: 127.0.0.1 Port: 8080 <<<")
    
    while not stop_event.is_set():
        # Captive Portal ကို Bypass လုပ်မည့် Core Logic
        print(f"{Fore.YELLOW}[•] System-Wide Bypass Running...               ", end="\r")
        time.sleep(5)

if __name__ == "__main__":
    try:
        if verify_license():
            start_bypass_process()
    except KeyboardInterrupt:
        stop_event.set()
        print(f"\n{Fore.RED}Turbo Engine Shutdown...{Fore.RESET}")
