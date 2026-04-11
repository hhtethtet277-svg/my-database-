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

# SSL Warning များနှင့် Certificate စစ်ဆေးခြင်းကို ပိတ်ထားရန်
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)

# ===============================
# CONFIGURATION
# ===============================
GITHUB_URL = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/main/key.txt"
USER_KEY = "AF8BE771-03B"  # သင့်ဖုန်းရဲ့ ID အမှန်
PING_THREADS = 5
stop_event = threading.Event()

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
# LICENSE & EXPIRY SYSTEM
# ===============================
def verify_license():
    h_banner()
    print(f"{Fore.YELLOW}[i] Checking security clearance...")
    print(f"{Fore.WHITE}└─ Device ID: {Fore.GREEN}{USER_KEY}")
    print(f"{Fore.CYAN}{'─'*55}")

    try:
        # SSL Verification ကို False လုပ်ပြီး Server ချိတ်ဆက်မှု အမှားကို ကျော်မယ်
        response = requests.get(GITHUB_URL, timeout=15, verify=False)
        
        if response.status_code == 200:
            raw_text = response.text.strip()
            # GitHub ထဲမှာ ID|YYYY-MM-DD ပုံစံရှိရမယ်
            if "|" in raw_text:
                key_from_server, exp_date_str = raw_text.split("|")
                
                if key_from_server.strip() == USER_KEY:
                    expiry_date = datetime.strptime(exp_date_str.strip(), "%Y-%m-%d")
                    
                    if datetime.now() < expiry_date:
                        print(f"{Fore.CYAN}[+] Status: {Fore.BLACK}{Back.GREEN} ACTIVE ")
                        print(f"{Fore.WHITE}└─ Expire Date: {Fore.YELLOW}{exp_date_str.strip()}")
                        print(f"{Fore.GREEN}✅ Access Granted! Launching...")
                        time.sleep(1)
                        return True
                    else:
                        print(f"{Fore.RED}[!] Status: {Fore.BLACK}{Back.RED} EXPIRED ")
                        print(f"{Fore.RED}❌ သက်တမ်းကုန်ဆုံးသွားပါပြီ။")
                        sys.exit()
            
            print(f"{Fore.RED}❌ ERROR: KEY NOT REGISTERED IN GITHUB")
            sys.exit()
            
    except Exception as e:
        print(f"{Fore.RED}❌ ERROR: SERVER UNREACHABLE")
        print(f"{Fore.YELLOW}Reason: {e}")
        sys.exit()

# ===============================
# CORE ENGINE
# ===============================
def start_bypass_process():
    print(f"{Fore.CYAN}[*] Initializing Turbo Engine...{Fore.RESET}")
    # ဒီနေရာမှာ သင့်ရဲ့ မူလ bypass logic တွေ ဆက်သွားပါမယ်
    while not stop_event.is_set():
        print(f"{Fore.YELLOW}[•] Bypass Engine Running...               ", end="\r")
        time.sleep(5)

if __name__ == "__main__":
    try:
        if verify_license():
            start_bypass_process()
    except KeyboardInterrupt:
        stop_event.set()
        print(f"\n{Fore.RED}Turbo Engine Shutdown...{Fore.RESET}")
