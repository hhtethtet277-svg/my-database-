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
from datetime import datetime
from urllib.parse import urlparse, parse_qs, urljoin
from colorama import Fore, Back, Style, init

# SSL Warning ပိတ်ခြင်း
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)

# ===============================
# ကိုယ်ပိုင် LICENSE CONFIG (ဒီနေရာကို သင့် Link နဲ့ အစားထိုးပါ)
# ===============================
GITHUB_URL = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/main/key.txt"
USER_KEY = "AF8BE771-03B"  # သင့်ဖုန်းရဲ့ ID အမှန်

# ===============================
# BYPASS CONFIG
# ===============================
PING_THREADS = 5
MIN_INTERVAL = 0.05
MAX_INTERVAL = 0.2
DEBUG = False

stop_event = threading.Event()

def check_real_internet():
    try:
        return requests.get("http://www.google.com", timeout=3).status_code == 200
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
    print(f"{Fore.CYAN} ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝ ╚═════╝ ╚═╝╚═╝  ╚════╝")
    print(f"{Fore.MAGENTA}{'='*55}")
    print(f"{Fore.WHITE}{Back.BLUE}      ALADDIN TURBO BYPASS | OWNER: HH TET TET      ")
    print(f"{Style.RESET_ALL}{Fore.MAGENTA}{'='*55}\n")

# ===============================
# BYPASS CORE LOGIC
# ===============================
def high_speed_ping(auth_link, sid):
    session = requests.Session()
    while not stop_event.is_set():
        try:
            session.get(auth_link, timeout=5)
            print(f"{Fore.GREEN}[✓]{Fore.RESET} SID {sid} | Turbo Pulse Active     ", end="\r")
        except:
            break
        time.sleep(random.uniform(MIN_INTERVAL, MAX_INTERVAL))

def start_bypass_process():
    print(f"{Fore.CYAN}[*] Initializing Turbo Engine...{Fore.RESET}")
    # သင့်ရဲ့ မူလ Bypass လုပ်ဆောင်ချက်များ ဒီနေရာမှာ ဆက်သွားပါမယ်
    while not stop_event.is_set():
        # ... (မူလ bypass logic များ) ...
        time.sleep(5)
        print(f"{Fore.YELLOW}[•] Bypass Engine Running...               ", end="\r")

# ===============================
# EXPIRY VERIFICATION (သက်တမ်းစစ်ဆေးခြင်း)
# ===============================
def verify_license():
    h_banner()
    print(f"{Fore.YELLOW}[i] Checking security clearance...")
    print(f"{Fore.WHITE}└─ Device ID: {Fore.GREEN}{USER_KEY}")
    print(f"{Fore.CYAN}{'─'*55}")

    try:
        response = requests.get(GITHUB_URL, timeout=10)
        if response.status_code == 200:
            raw_text = response.text.strip()
            # GitHub ထဲမှာ ID|YYYY-MM-DD ပုံစံရှိရမယ်
            if "|" in raw_text:
                key, exp_date = raw_text.split("|")
                if key.strip() == USER_KEY:
                    expiry = datetime.strptime(exp_date.strip(), "%Y-%m-%d")
                    if datetime.now() < expiry:
                        print(f"{Fore.CYAN}[+] Status: {Fore.BLACK}{Back.GREEN} ACTIVE ")
                        print(f"{Fore.WHITE}└─ Expire Date: {Fore.YELLOW}{exp_date}")
                        print(f"{Fore.GREEN}✅ Access Granted! Launching...")
                        time.sleep(1)
                        return True
                    else:
                        print(f"{Fore.RED}[!] Status: {Fore.BLACK}{Back.RED} EXPIRED ")
                        print(f"{Fore.RED}❌ သက်တမ်းကုန်ဆုံးသွားပါပြီ။")
                        sys.exit()
            
            print(f"{Fore.RED}❌ ERROR: KEY NOT REGISTERED")
            sys.exit()
    except Exception as e:
        print(f"{Fore.RED}❌ ERROR: SERVER UNREACHABLE ({e})")
        sys.exit()

if __name__ == "__main__":
    try:
        if verify_license():
            start_bypass_process()
    except KeyboardInterrupt:
        stop_event.set()
        print(f"\n{Fore.RED}Turbo Engine Shutdown...{Fore.RESET}")
