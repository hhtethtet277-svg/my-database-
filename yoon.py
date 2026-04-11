import os
import requests
import re
import urllib3
import time
import threading
import random
import uuid
import sys
from datetime import datetime
from urllib.parse import urlparse, parse_qs, urljoin
from colorama import Fore, Back, Style, init

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)

# ===============================
# CONFIGURATION
# ===============================
GITHUB_URL = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/main/key.txt"
KEY_FILE = os.path.join(os.path.expanduser("~"), ".device_key")
CACHE_FILE = os.path.join(os.path.expanduser("~"), ".license_cache")

def get_or_create_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "r") as f: return f.read().strip()
    new_key = str(uuid.uuid4())[:12].upper()
    with open(KEY_FILE, "w") as f: f.write(new_key)
    return new_key

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

def verify_license():
    h_banner()
    user_key = get_or_create_key()
    print(f"{Fore.YELLOW}[i] Checking Security Clearance...")
    print(f"{Fore.WHITE}└─ Your Device ID: {Fore.GREEN}{user_key}")
    
    # ၁။ GitHub ကို ချိတ်ဆက်ရန် ကြိုးစားခြင်း (Online Check)
    try:
        response = requests.get(GITHUB_URL, timeout=10)
        if response.status_code == 200:
            lines = response.text.splitlines()
            for line in lines:
                if "|" in line:
                    parts = line.split("|")
                    key = parts[0].strip()
                    exp_date_str = parts[1].strip()
                    
                    if key == user_key:
                        # ရက်စွဲ စစ်ဆေးခြင်း
                        expiry_date = datetime.strptime(exp_date_str, "%Y-%m-%d")
                        if datetime.now() < expiry_date:
                            # Cache သိမ်းဆည်းခြင်း
                            with open(CACHE_FILE, "w") as f: f.write(f"{user_key}|{exp_date_str}")
                            print(f"{Fore.GREEN}[+] Status: ONLINE ACTIVE")
                            print(f"{Fore.WHITE}└─ Expire Date: {Fore.YELLOW}{exp_date_str}")
                            return True
                        else:
                            print(f"{Fore.RED}❌ LICENSE EXPIRED (သက်တမ်းကုန်ဆုံးပါပြီ)")
                            sys.exit()
    except:
        # ၂။ အင်တာနက်မရှိလျှင် Cache ကို စစ်ဆေးခြင်း (Offline Check)
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r") as f:
                cached_data = f.read().strip().split("|")
                if cached_data[0] == user_key:
                    expiry_date = datetime.strptime(cached_data[1], "%Y-%m-%d")
                    if datetime.now() < expiry_date:
                        print(f"{Fore.CYAN}[+] Status: OFFLINE ACTIVE (No Internet)")
                        print(f"{Fore.WHITE}└─ Expire Date: {Fore.YELLOW}{cached_data[1]}")
                        return True

    print(f"\n{Fore.RED}❌ ERROR: ACCESS DENIED!")
    print(f"{Fore.YELLOW}[!] Voucher မရှိလျှင် ပထမဆုံးတစ်ကြိမ် Online ရှိစဉ် Run ထားရန်လိုသည်။")
    print(f"{Fore.WHITE}└─ လိုအပ်ပါက Owner ထံသို့ ID ပေး၍ သက်တမ်းတိုးပါ။")
    sys.exit()

def start_bypass_process():
    print(f"\n{Fore.MAGENTA}[*] Initializing Bypass Engine...")
    time.sleep(1)
    # ဤနေရာတွင် သင်၏ Bypass Logic များကို ဆက်လက်ထည့်သွင်းနိုင်သည်
    while True:
        print(f"{Fore.GREEN}[✓] Pulse Active... Check your browser.", end="\r")
        time.sleep(2)

if __name__ == "__main__":
    if verify_license():
        start_bypass_process()
