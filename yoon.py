import os
import requests
import urllib3
import time
import threading
import sys
import base64
from datetime import datetime
from colorama import Fore, Back, Style, init

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
# V2RAY CONFIG GENERATOR
# ===============================
def generate_v2ray_link():
    # v2rayNG အတွက် SOCKS5 Link ထုတ်ပေးခြင်း
    # ပုံစံ - socks://[base64(host:port)]#Remarks
    config_info = f"127.0.0.1:{PROXY_PORT}"
    encoded_info = base64.b64encode(config_info.encode()).decode()
    v2ray_link = f"socks://{encoded_info}#Moe_Yu_Bypass_🚀"
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
    try:
        response = requests.get(GITHUB_URL, timeout=15, verify=False)
        if response.status_code == 200:
            raw_text = response.text.strip()
            if "|" in raw_text:
                key_from_server, exp_date_str = raw_text.split("|")
                if key_from_server.strip() == USER_KEY:
                    print(f"{Fore.CYAN}[+] Status: {Fore.GREEN}ACTIVE")
                    print(f"{Fore.WHITE}└─ Expire Date: {Fore.YELLOW}{exp_date_str.strip()}")
                    return True
            print(f"{Fore.RED}\n❌ ERROR: KEY NOT REGISTERED")
            return False
    except Exception:
        print(f"{Fore.RED}\n❌ ERROR: SERVER UNREACHABLE")
        return False

def start_bypass_process():
    print(f"{Fore.CYAN}[*] Initializing Turbo Engine...")
    
    # Config Link ထုတ်ပေးခြင်း
    link = generate_v2ray_link()
    
    print(f"\n{Fore.WHITE}{Back.MAGENTA}  V2RAYNG CONFIG LINK (COPY THIS):  ")
    print(f"{Fore.YELLOW}{link}")
    print(f"{Fore.WHITE}{Back.MAGENTA}{' '*36}\n")
    
    print(f"{Fore.GREEN}💡 နည်းလမ်း: အပေါ်က Link ကို Copy ကူးပြီး v2rayNG ထဲမှာ")
    print(f"{Fore.GREEN}   'Import config from clipboard' ကို နှိပ်ပါဗျ။\n")
    
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
