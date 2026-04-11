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
# CONFIGURATION (FIXED LINK)
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
    
    try:
        # GitHub ကနေ Data လှမ်းယူမယ်
        response = requests.get(GITHUB_URL, timeout=10)
        if response.status_code == 200:
            lines = response.text.splitlines()
            for line in lines:
                if "|" in line:
                    parts = line.split("|")
                    key = parts[0].strip()
                    exp_date_str = parts[1].strip()
                    
                    if key == user_key:
                        expiry_date = datetime.strptime(exp_date_str, "%Y-%m-%d")
                        if datetime.now() < expiry_date:
                            # အောင်မြင်ရင် Cache သိမ်းမယ်
                            with open(CACHE_FILE, "w") as f: f.write(f"{user_key}|{exp_date_str}")
                            print(f"\n{Fore.GREEN}[+] Status: ONLINE ACTIVE")
                            print(f"{Fore.WHITE}└─ Expire Date: {Fore.YELLOW}{exp_date_str}")
                            return True
    except:
        # အင်တာနက်မရှိရင် Cache ကို စစ်မယ်
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r") as f:
                c_data = f.read().strip().split("|")
                if c_data[0] == user_key:
                    if datetime.now() < datetime.strptime(c_data[1], "%Y-%m-%d"):
                        print(f"\n{Fore.CYAN}[+] Status: OFFLINE ACTIVE")
                        return True

    print(f"\n{Fore.RED}❌ ERROR: ACCESS DENIED!")
    print(f"{Fore.YELLOW}[!] GitHub Link သို့မဟုတ် ID/Date မှားယွင်းနေပါသည်။")
    sys.exit()

if __name__ == "__main__":
    if verify_license():
        print(f"\n{Fore.GREEN}[✓] Bypass Engine Started Successfully!")
        while True:
            time.sleep(10)
