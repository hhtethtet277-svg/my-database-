import os
import requests
import urllib3
import time
import threading
import socketserver
import http.server
import base64
from datetime import datetime
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
stop_event = threading.Event()

# ===============================
# PROXY SERVER LOGIC (အခြား App များအတွက်)
# ===============================
class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Moe Yu Bypass Engine Active")

def start_proxy():
    try:
        # 0.0.0.0 သုံးထား၍ ဖုန်းထဲက App အားလုံး ဝင်ချိတ်နိုင်ပါသည်
        with socketserver.TCPServer(("0.0.0.0", PROXY_PORT), ProxyHandler) as httpd:
            print(f"{Fore.GREEN}[✔] Proxy Engine ready on Port: {PROXY_PORT}")
            httpd.serve_forever()
    except Exception as e:
        print(f"{Fore.RED}[!] Proxy Error: {e}")

# ===============================
# V2RAY CONFIG GENERATOR
# ===============================
def generate_v2ray_link():
    # v2rayNG အတွက် SOCKS5 Link ထုတ်ပေးခြင်း (Format အမှန်)
    config_info = f"127.0.0.1:{PROXY_PORT}"
    encoded_info = base64.b64encode(config_info.encode()).decode()
    v2ray_link = f"socks://{encoded_info}#Moe_Yu_Bypass"
    return v2ray_link

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

def verify_license():
    h_banner()
    print(f"{Fore.YELLOW}[i] Checking security clearance...")
    try:
        response = requests.get(GITHUB_URL, timeout=15, verify=False)
        if response.status_code == 200:
            raw_text = response.text.strip()
            if "|" in raw_text:
                key_from_server, exp_date_str = raw_text.split("|")
                if key_from_server.strip() == USER_KEY:
                    print(f"{Fore.CYAN}[+] Status: {Fore.BLACK}{Back.GREEN} ACTIVE ")
                    print(f"{Fore.WHITE}└─ Expire Date: {Fore.YELLOW}{exp_date_str.strip()}")
                    return True
        print(f"{Fore.RED}\n❌ ERROR: KEY NOT REGISTERED")
        return False
    except:
        print(f"{Fore.RED}\n❌ ERROR: CONNECTION FAILED")
        return False

def start_bypass_process():
    print(f"{Fore.CYAN}[*] Launching Turbo Engine...")
    
    # Proxy ကို background မှာ run ရန်
    proxy_thread = threading.Thread(target=start_proxy, daemon=True)
    proxy_thread.start()
    
    # Config Link ထုတ်ပေးရန်
    link = generate_v2ray_link()
    
    print(f"\n{Fore.WHITE}{Back.MAGENTA}  V2RAYNG CONFIG LINK (COPY THIS):  ")
    print(f"{Fore.YELLOW}{link}")
    print(f"{Fore.WHITE}{Back.MAGENTA}{' '*36}\n")
    
    print(f"{Fore.GREEN}✅ Access Granted! Everything is ready.")
    
    while not stop_event.is_set():
        print(f"{Fore.YELLOW}[•] Bypass Engine Running Optimized...         ", end="\r")
        time.sleep(5)

if __name__ == "__main__":
    try:
        if verify_license():
            start_bypass_process()
    except KeyboardInterrupt:
        stop_event.set()
        print(f"\n{Fore.RED}Turbo Engine Shutdown...{Fore.RESET}")
