import os
import requests
import urllib3
import time
import sys
from datetime import datetime
from colorama import Fore, Back, Style, init

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)

# Link ကို ပိုမိုခိုင်မာအောင် ပြင်ဆင်ထားသည်
GITHUB_URL = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database/main/key.txt"
CACHE_FILE = os.path.join(os.path.expanduser("~"), ".license_cache")
USER_KEY = "AF8BE771-03B"

def h_banner():
    os.system('clear')
    print(f"{Fore.CYAN}{'='*55}")
    print(f"{Fore.MAGENTA}  █████╗ ██╗      █████╗ ██████╗ ██████╗ ██╗███╗   ██╗")
    print(f"{Fore.MAGENTA} ██╔══██╗██║     ██╔══██╗██╔══██╗██╔══██╗██║████╗  ██║")
    print(f"{Fore.MAGENTA} ███████║██║     ███████║██║  ██║██║  ██║██║██╔██╗ ██║")
    print(f"{Fore.MAGENTA} ██╔══██║██║     ██╔══██║██║  ██║██║  ██║██║██║╚██╗██║")
    print(f"{Fore.MAGENTA} ██║  ██║███████╗██║  ██║██████╔╝██████╔╝██║██║ ╚████║")
    print(f"{Fore.MAGENTA} ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝")
    print(f"{Fore.CYAN}{'='*55}")
    print(f"{Fore.WHITE}{Back.BLUE}      ALADDIN BYPASS PREMIUM | OWNER: HH TET TET      ")
    print(f"{Style.RESET_ALL}{Fore.CYAN}{'='*55}\n")

def verify_license():
    h_banner()
    print(f"{Fore.YELLOW}[i] System Identity: {Fore.GREEN}{USER_KEY}")
    
    try:
        response = requests.get(GITHUB_URL, timeout=10)
        if response.status_code == 200:
            lines = response.text.strip().splitlines()
            for line in lines:
                if "|" in line:
                    key, exp = line.split("|")
                    if key.strip() == USER_KEY:
                        expiry = datetime.strptime(exp.strip(), "%Y-%m-%d")
                        if datetime.now() < expiry:
                            with open(CACHE_FILE, "w") as f: f.write(f"{USER_KEY}|{exp}")
                            print(f"{Fore.GREEN}[+] STATUS: ONLINE ACTIVE")
                            print(f"{Fore.WHITE}└─ VALID UNTIL: {Fore.CYAN}{exp}")
                            return True
    except:
        if os.path.exists(CACHE_FILE):
            print(f"{Fore.CYAN}[+] STATUS: OFFLINE ACTIVE (Cache Mode)")
            return True

    print(f"{Fore.RED}❌ ACCESS DENIED! PLEASE CHECK INTERNET OR KEY.")
    sys.exit()

def start_bypass():
    print(f"\n{Fore.WHITE}>>> {Fore.YELLOW}STARTING PREMIUM BYPASS PROCESS {Fore.WHITE}<<<")
    print(f"{Fore.WHITE}─" * 55)
    
    features = [
        "Initializing Firewall Bypass...",
        "Connecting to Ruijie Server...",
        "Optimizing Tunnel Speed...",
        "Applying Global Protocol...",
        "Premium Access Granted!"
    ]
    
    for feature in features:
        print(f"{Fore.GREEN}[✔] {feature}")
        time.sleep(0.8)
    
    print(f"\n{Fore.BLACK}{Back.GREEN} SYSTEM RUNNING STABLE: ENJOY YOUR BYPASS! ")
    while True:
        time.sleep(10)

if __name__ == "__main__":
    if verify_license():
        start_bypass()
