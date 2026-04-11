import os
import requests
import urllib3
import time
import sys
from datetime import datetime
from colorama import Fore, Back, Style, init

# SSL warning များပိတ်ရန် နှင့် Colorama initialize လုပ်ရန်
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)

# သင့်ရဲ့ Repository လမ်းကြောင်းအတိအကျ
GITHUB_URL = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/main/key.txt"
CACHE_FILE = os.path.join(os.path.expanduser("~"), ".license_cache")
USER_KEY = "AF8BE771-03B"

def h_banner():
    os.system('clear')
    print(f"{Fore.CYAN}{'='*55}")
    print(f"{Fore.YELLOW}  █████╗ ██╗      █████╗ ██████╗ ██████╗ ██╗███╗   ██╗")
    print(f"{Fore.YELLOW} ██╔══██╗██║     ██╔══██╗██╔══██╗██╔══██╗██║████╗  ██║")
    print(f"{Fore.YELLOW} ███████║██║     ███████║██║  ██║██║  ██║██║██╔██╗ ██║")
    print(f"{Fore.YELLOW} ██╔══██║██║     ██╔══██║██║  ██║██║  ██║██║██║╚██╗██║")
    print(f"{Fore.YELLOW} ██║  ██║███████╗██║  ██║██████╔╝██████╔╝██║██║ ╚████║")
    print(f"{Fore.YELLOW} ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝")
    print(f"{Fore.CYAN}{'='*55}")
    print(f"{Fore.WHITE}{Back.BLUE}      ALADDIN PREMIUM BYPASS | OWNER: HH TET TET      ")
    print(f"{Style.RESET_ALL}{Fore.CYAN}{'='*55}\n")

def verify_license():
    h_banner()
    print(f"{Fore.WHITE}[i] Checking Device: {Fore.GREEN}{USER_KEY}")
    
    try:
        # GitHub ကနေ Key ကို တိုက်ရိုက်ဖတ်မယ်
        response = requests.get(GITHUB_URL, timeout=15, verify=False)
        if response.status_code == 200:
            # စာသားထဲမှာ Space တွေပါနေရင် ဖယ်ထုတ်ပစ်မယ်
            raw_data = response.text.strip()
            
            if "|" in raw_data:
                github_key, expiry_str = raw_data.split("|")
                # ID နှင့် ရက်စွဲကို သန့်စင်ပြီးမှ စစ်ဆေးမယ်
                if github_key.strip() == USER_KEY:
                    expiry_date = datetime.strptime(expiry_str.strip(), "%Y-%m-%d")
                    if datetime.now() < expiry_date:
                        # Offline သုံးလို့ရအောင် Cache သိမ်းမယ်
                        with open(CACHE_FILE, "w") as f:
                            f.write(f"{USER_KEY}|{expiry_str.strip()}")
                        print(f"{Fore.GREEN}[+] STATUS: ONLINE ACTIVE")
                        print(f"{Fore.WHITE}└─ VALID UNTIL: {Fore.CYAN}{expiry_str.strip()}")
                        return True
            
            print(f"{Fore.RED}❌ ERROR: KEY NOT MATCHED IN GITHUB!")
            print(f"{Fore.YELLOW}Expected: {USER_KEY}")
            print(f"{Fore.YELLOW}Got from GitHub: {raw_data}")
            
    except Exception as e:
        # အင်တာနက်မရှိရင် Cache ကနေ စစ်မယ်
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r") as f:
                c_key, c_exp = f.read().split("|")
                if c_key == USER_KEY:
                    print(f"{Fore.CYAN}[+] STATUS: OFFLINE ACTIVE (Cached)")
                    return True
        print(f"{Fore.RED}❌ CONNECTION ERROR OR NO INTERNET")
        
    return False

def start_bypass():
    print(f"\n{Fore.GREEN}[✓] Access Granted! Starting Engine...")
    time.sleep(1)
    # ဒီနေရာမှာ သင့်ရဲ့ Bypass လုပ်ဆောင်ချက်တွေ ထည့်ပါ
    print(f"{Fore.MAGENTA}>>> BYPASS RUNNING STABLE <<<")
    while True:
        time.sleep(10)

if __name__ == "__main__":
    if verify_license():
        start_bypass()
    else:
        print(f"{Fore.RED}\n[!] Please contact HH TET TET for activation.")
        sys.exit()
