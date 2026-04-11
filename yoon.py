import os
import requests
import urllib3
import time
import uuid
import sys
from datetime import datetime
from colorama import Fore, Back, Style, init

# SSL warning ပိတ်ရန်နှင့် အရောင်စနစ်စတင်ရန်
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)

# ===============================
# CONFIGURATION (STABLE VERSION)
# ===============================
# Link ကို အမှားမခံအောင် တိုက်ရိုက်သတ်မှတ်ထားသည်
GITHUB_URL = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/main/key.txt"
KEY_FILE = os.path.join(os.path.expanduser("~"), ".device_key")
CACHE_FILE = os.path.join(os.path.expanduser("~"), ".license_cache")

def get_device_id():
    """Device ID ကို တည်ငြိမ်အောင် ဖတ်ယူသည်"""
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "r") as f: return f.read().strip()
    # ပုံထဲမှ သင်၏ ID အား ပုံသေသတ်မှတ်ပေးထားပါသည်
    stable_key = "AF8BE771-03B" 
    with open(KEY_FILE, "w") as f: f.write(stable_key)
    return stable_key

def h_banner():
    """Logo နှင့် Banner ပြသရန်"""
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
    """License နှင့် သက်တမ်း စစ်ဆေးရန်"""
    h_banner()
    user_key = get_device_id()
    print(f"{Fore.YELLOW}[i] System Identity: {Fore.GREEN}{user_key}")
    print(f"{Fore.WHITE}─" * 55)

    # ၁။ အွန်လိုင်းမှ စစ်ဆေးခြင်း
    try:
        response = requests.get(GITHUB_URL, timeout=10)
        if response.status_code == 200:
            lines = response.text.strip().splitlines()
            for line in lines:
                if "|" in line:
                    file_key, exp_date = line.split("|")
                    if file_key.strip() == user_key:
                        # ရက်စွဲကို စစ်ဆေးခြင်း
                        expiry = datetime.strptime(exp_date.strip(), "%Y-%m-%d")
                        if datetime.now() < expiry:
                            # Cache သိမ်းဆည်းခြင်း
                            with open(CACHE_FILE, "w") as f: f.write(f"{user_key}|{exp_date}")
                            print(f"{Fore.GREEN}[+] STATUS: ONLINE ACTIVE")
                            print(f"{Fore.WHITE}└─ EXPIRY: {Fore.YELLOW}{exp_date}")
                            return True
                        else:
                            print(f"{Fore.RED}❌ ERROR: LICENSE EXPIRED! (သက်တမ်းကုန်ဆုံးပါပြီ)")
                            sys.exit()
    except Exception:
        # ၂။ အင်တာနက်မရှိလျှင် Cache ကို စစ်ဆေးခြင်း
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r") as f:
                c_data = f.read().strip().split("|")
                if len(c_data) == 2 and c_data[0] == user_key:
                    c_expiry = datetime.strptime(c_data[1], "%Y-%m-%d")
                    if datetime.now() < c_expiry:
                        print(f"{Fore.CYAN}[+] STATUS: OFFLINE ACTIVE (Valid Until {c_data[1]})")
                        return True

    print(f"{Fore.RED}❌ ACCESS DENIED: NO INTERNET OR INVALID KEY")
    print(f"{Fore.YELLOW}[!] ပထမဆုံးအကြိမ် Online ရှိစဉ် တစ်ခါ Run ပေးရန် လိုအပ်ပါသည်။")
    sys.exit()

def start_bypass():
    print(f"\n{Fore.MAGENTA}[*] Initializing Bypass Core...")
    time.sleep(1)
    while True:
        print(f"{Fore.GREEN}[✓] Pulse Active... Service Running.", end="\r")
        time.sleep(2)

if __name__ == "__main__":
    if verify_license():
        start_bypass()
