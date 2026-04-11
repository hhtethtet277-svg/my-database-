import os
import requests
import re
import urllib3
import time
import threading
import random
import sys
from datetime import datetime
from urllib.parse import urlparse, parse_qs, urljoin
from colorama import Fore, Back, Style, init

# SSL Warning များနှင့် Certificate စစ်ဆေးခြင်းကို ပိတ်ထားရန် (SSL Error ကင်းဝေးစေရန်)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)

# ===============================
# CONFIGURATION
# ===============================
GITHUB_URL = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/main/key.txt"
USER_KEY = "AF8BE771-03B"  # သင့်ဖုန်းရဲ့ ID

# Bypass Settings
PING_THREADS = 5
MIN_INTERVAL = 0.05
MAX_INTERVAL = 0.2
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
    print(f"{Fore.WHITE}{Back.BLUE}      ALADDIN TURBO BYPASS | OWNER: MOE YU      ")
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
        # SSL Verification ကို False လုပ်ထားခြင်းက Server Unreachable Error ကို ပြေလည်စေပါတယ်
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
                        print(f"{Fore.GREEN}✅ Access Granted! Launching Engine...")
                        time.sleep(1)
                        return True
                    else:
                        print(f"{Fore.RED}[!] Status: {Fore.BLACK}{Back.RED} EXPIRED ")
                        print(f"{Fore.RED}❌ သက်တမ်းကုန်ဆုံးသွားပါပြီ။")
                        return False
            
            print(f"{Fore.RED}\n❌ ERROR: KEY NOT REGISTERED IN GITHUB")
            print(f"{Fore.YELLOW}Received Data: {raw_text}")
            return False
            
    except Exception as e:
        print(f"{Fore.RED}\n❌ ERROR: CONNECTION FAILED")
        print(f"{Fore.YELLOW}Reason: {e}")
        return False

# ===============================
# BYPASS CORE LOGIC
# ===============================
def high_speed_ping(auth_link, sid):
    session = requests.Session()
    while not stop_event.is_set():
        try:
            session.get(auth_link, timeout=5, verify=False)
            print(f"{Fore.GREEN}[✓]{Fore.RESET} SID {sid} | Turbo Pulse Active     ", end="\r")
        except:
            break
        time.sleep(random.uniform(MIN_INTERVAL, MAX_INTERVAL))

def start_bypass_process():
    print(f"{Fore.CYAN}[*] Initializing Turbo Engine...{Fore.RESET}")
    
    # ဤနေရာတွင် Captive Portal များကို ရှာဖွေပြီး Bypass လုပ်မည့် Logic များဖြစ်သည်
    while not stop_event.is_set():
        # စမ်းသပ်ရန်အတွက် Engine အလုပ်လုပ်ပုံကို ပြသခြင်းဖြစ်သည်
        # သင့်တွင် Captive Portal link ရှိပါက ဤနေရာတွင် high_speed_ping ကို run ပေးရပါမည်
        time.sleep(5)
        print(f"{Fore.YELLOW}[•] Bypass Engine Running Optimized...         ", end="\r")

# ===============================
# ENTRY POINT
# ===============================
if __name__ == "__main__":
    try:
        if verify_license():
            start_bypass_process()
    except KeyboardInterrupt:
        stop_event.set()
        print(f"\n{Fore.RED}Turbo Engine Shutdown...{Fore.RESET}")
