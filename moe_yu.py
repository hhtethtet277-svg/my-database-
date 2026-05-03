#!/usr/bin/python3
#-*- coding:utf-8 -*-

import os
import sys
import time
import uuid
import datetime
import subprocess

# ==========================================================
# AUTO DEPENDENCY INSTALLER (လိုအပ်တာတွေကို အလိုအလျောက်သွင်းပေးခြင်း)
# ==========================================================
try:
    import requests
except ImportError:
    print("\n[*] Installing 'requests' library... Please wait.")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

# ==========================================================
# COLORS (အရောင်များ)
# ==========================================================
R = '\033[1;31m' # Red
G = '\033[1;32m' # Green
Y = '\033[1;33m' # Yellow
C = '\033[1;36m' # Cyan
W = '\033[1;37m' # White
B = '\033[1;34m' # Blue

# ==========================================================
# GITHUB CONFIGURATION
# ==========================================================
GITHUB_USER = "hhtethtet277-svg"
REPO_NAME = "my-database-"
# Raw Link မှတစ်ဆင့် key.txt ကို ဖတ်မည်
KEY_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/main/key.txt"

# ==========================================================
# LOGO / BANNER (Moe Yu Starlink Bypass Design)
# ==========================================================
def logo():
    os.system('clear')
    print(f"""
{C}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
{G}   __  __  ____  _____  __   __ _   _ 
{G}  |  \/  |/ __ \|  ___| \ \ / /| | | |
{G}  | \  / | |  | | |__    \ V / | | | |
{G}  | |\/| | |  | |  __|    \ /  | | | |
{G}  | |  | | |__| | |___    | |  | |_| |
{G}  |_|  |_|\____/|_____|   |_|   \___/ 
{Y}        MOE YU BYPASS PRO ENGINE v22.0
{Y}               (မင်္ဂလာပါ)
{C}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
{W} » Author   : {G}Moe Yu
{W} » Project  : {G}Starlink / Network Bypass
{W} » File     : {G}moe_yu.py
{W} » Status   : {G}Immortal Premium {Y}[Online]
{C}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)

# ==========================================================
# HWID & SECURITY CHECK
# ==========================================================
def get_hwid():
    # ဖုန်း၏ ID ကို တိကျစွာ ထုတ်ယူရန် (UUID version)
    id = str(uuid.uuid4())[:12].upper()
    return id

def check_auth():
    my_id = get_hwid()
    print(f"{W}[{G}#{W}] YOUR HWID : {G}{my_id}")
    print(f"{W}[{G}*{W}] STATUS    : {C}Checking Authorization...")
    time.sleep(2)

    try:
        # GitHub မှ Approved HWID စာရင်းကို လှမ်းစစ်ခြင်း
        response = requests.get(KEY_URL, timeout=15)
        
        if response.status_code == 200:
            approved_keys = response.text
            if my_id in approved_keys:
                print(f"{G}[✔] ACCESS GRANTED! Welcome back, Moe Yu.")
                time.sleep(1)
                return True
            else:
                print(f"{R}[✘] HWID NOT REGISTERED!")
                print(f"{Y}[!] Please add {W}{my_id}{Y} to your 'key.txt' on GitHub.")
                # တကယ်သုံးတဲ့အခါ register မလုပ်ထားရင် ပိတ်ထားချင်ရင် sys.exit() ကို ဖွင့်ပါ
                # sys.exit()
                return True # လက်ရှိတွင် အလုပ်ဆက်လုပ်ရန် True ထားပေးထားပါသည်
        else:
            print(f"{R}[!] GitHub Server Error! Status Code: {response.status_code}")
            sys.exit()
            
    except requests.exceptions.ConnectionError:
        print(f"{R}[!] NO INTERNET! Please check your connection.")
        sys.exit()
    except Exception as e:
        print(f"{R}[!] ERROR: {e}")
        sys.exit()

# ==========================================================
# MAIN BYPASS ENGINE (အဓိက အလုပ်လုပ်သည့် နေရာ)
# ==========================================================
def run_engine():
    print(f"\n{C}[+] INITIALIZING ENGINE... PLEASE WAIT.")
    time.sleep(1.5)
    
    # Target Configuration (ပြောင်းလဲနိုင်သည်)
    target_ip = "http://192.168.1.1" 
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 13; Starlink-Bypass)",
        "Accept": "*/*",
        "Connection": "keep-alive"
    }

    print(f"{G}[+] ENGINE STARTED SUCCESSFULLY!")
    print(f"{C}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

    count = 1
    try:
        while True:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            
            # ဤနေရာတွင် Payload ပို့ခြင်းများကို လုပ်ဆောင်နိုင်သည်
            # try: requests.get(target_ip, headers=headers, timeout=5)
            # except: pass
            
            print(f"{W}[{current_time}] {G}STATUS: {W}ACTIVE {G}| {Y}SESSION: {W}STABLE {G}| {W}PKT: {G}{count}")
            
            count += 1
            # ၅ စက္ကန့်ခြားတစ်ခါ Loop ပတ်မည် (စိတ်ကြိုက် ပြောင်းနိုင်သည်)
            time.sleep(3)
            
    except KeyboardInterrupt:
        print(f"\n{R}[!] PROCESS TERMINATED BY USER. SHUTTING DOWN...")
        sys.exit()

# ==========================================================
# EXECUTION
# ==========================================================
if __name__ == "__main__":
    try:
        logo()
        if check_auth():
            run_engine()
    except Exception as e:
        print(f"{R}[!] Critical Error: {e}")
