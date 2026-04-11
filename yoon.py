import os
import requests
import urllib3
import time
import sys
from datetime import datetime
from colorama import Fore, Back, Style, init

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)

# Link ကို အမှားကင်းအောင် raw link တိုက်ရိုက် သုံးထားပါတယ်
GITHUB_URL = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/main/key.txt"
CACHE_FILE = os.path.join(os.path.expanduser("~"), ".license_cache")
USER_KEY = "AF8BE771-03B"

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
    print(f"{Fore.YELLOW}[i] Device ID: {Fore.GREEN}{USER_KEY}")
    
    try:
        # GitHub ကနေ key နဲ့ date ကို လှမ်းဖတ်မယ်
        response = requests.get(GITHUB_URL, timeout=15)
        if response.status_code == 200:
            raw_text = response.text.strip()
            # key.txt ထဲမှာ AF8BE771-03B|2027-01-01 လို့ ရှိရမယ်
            if "|" in raw_text:
                file_key, exp_date = raw_text.split("|")
                if file_key.strip() == USER_KEY:
                    expiry = datetime.strptime(exp_date.strip(), "%Y-%m-%d")
                    if datetime.now() < expiry:
                        with open(CACHE_FILE, "w") as f: f.write(f"{USER_KEY}|{exp_date}")
                        print(f"{Fore.GREEN}[+] STATUS: ONLINE ACTIVE")
                        print(f"{Fore.YELLOW}└─ VALID UNTIL: {exp_date}")
                        return True
        print(f"{Fore.RED}❌ ERROR: KEY NOT MATCHED IN GITHUB")
    except Exception as e:
        if os.path.exists(CACHE_FILE):
            print(f"{Fore.CYAN}[+] STATUS: OFFLINE ACTIVE")
            return True
        print(f"{Fore.RED}❌ CONNECTION ERROR: {e}")

    sys.exit()

if __name__ == "__main__":
    if verify_license():
        print(f"\n{Fore.GREEN}[✓] Bypass Engine Started!")
        while True: time.sleep(10)
