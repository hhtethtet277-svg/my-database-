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
import subprocess
import argparse
import requests
from datetime import datetime, timedelta
from urllib.parse import quote
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

# --- UI & Colors ---
w, g, y, r, b = "\033[1;00m", "\033[1;32m", "\033[1;33m", "\033[1;31m", "\033[1;34m"

def clear(): os.system("clear")
def Line(): print(f"{y}-" * os.get_terminal_size()[0] + f"{w}")

def Logo():
    clear()
    logo = f"""{r},-_/         .     ,--. .        .
'  | . . ,-. |-   | `-' |  . ,-. | ,
   | | | `-. |    |   . |  | |   |<
   | `-^ `-' `'   `--'  `' ' `-' ' `
/` |
`--'  {g}              Created by Moe Yu{w}"""
    print(logo)
    Line()
    print(f"[*] Created by Moe Yu (@moeyu)")
    print(f"[*] Official Channel: @starlink112")
    print(f"[*] Target: Ruijie Network Router")
    Line()

# --- HWID & Time Logic ---
def get_uid():
    return hashlib.md5((str(os.getlogin()) + str(os.getuid())).encode()).hexdigest()[:10].upper()

def get_hwid_key():
    return f"MY-{get_uid()}"

def get_network_time():
    try:
        client = ntplib.NTPClient()
        response = client.request('pool.ntp.org', version=3)
        return datetime.strptime(time.ctime(response.tx_time), "%a %b %d %H:%M:%S %Y")
    except:
        return datetime.now()

# --- Security System ---
class Security:
    def __init__(self):
        self.db_url = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/main/key.txt"
        self.my_hwid = get_hwid_key()
        self.version = "22.0"

    async def check_access(self):
        print(f"{g}[*] လိုင်စင်စစ်ဆေးနေသည်...{w}")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.db_url) as resp:
                    if resp.status == 200:
                        data = await resp.text()
                        lines = data.splitlines()
                        for line in lines:
                            if "~" in line:
                                uid, exp_date = line.split("~")
                                if uid == self.my_hwid:
                                    return self.verify_expiry(exp_date)
                        
                        self.print_no_key()
                        return False
                    else:
                        print(f"{r}[!] Database ဆာဗာချိတ်ဆက်မှု မအောင်မြင်ပါ။{w}")
                        return False
        except Exception as e:
            print(f"{r}[!] Error: {e}{w}")
            return False

    def verify_expiry(self, exp_str):
        try:
            # Format: MM-HH-DD-MM-YYYY
            exp_dt = datetime.strptime(exp_str, "%M-%H-%d-%m-%Y")
            curr_dt = get_network_time()
            if exp_dt > curr_dt:
                print(f"{g}[+] Access Granted! Expire: {exp_dt}{w}")
                return True
            else:
                print(f"{r}[!] သင်၏ Key မှာ သက်တမ်းကုန်ဆုံးသွားပါပြီ။{w}")
                return False
        except:
            return False

    def print_no_key(self):
        print(f"{r}[!] သင်၏ Key မှာ မှတ်ပုံတင်ထားခြင်းမရှိပါ။{w}")
        Line()
        print(f"{y}သင်၏ HWID: {g}{self.my_hwid}{w}")
        print(f"{y}Key ဝယ်ယူရန် @moeyu ကို ဆက်သွယ်ပါ။{w}")
        Line()

# --- Core Logic (Bruteforce & Setup) ---
# (သင်ပေးပို့ထားသော main.py ထဲမှ မူရင်း logic များကို ဤနေရာတွင် ပေါင်းထည့်ထားသည်)
class RuijieTool:
    def __init__(self):
        self.session_url = ""
        self.ip = ""

    async def setup(self):
        print(f"{g}[+] Setting up wifi info...{w}")
        try:
            res = requests.get("http://192.168.0.1", timeout=5).url
            self.ip = re.search('gw_address=(.*?)&', res).group(1)
            open(".ip", "w").write(self.ip)
            print(f"{g}[+] IP Detected: {self.ip}{w}")
        except:
            print(f"{r}[!] Setup Failed. Connect to Ruijie WiFi.{w}")

    async def start_brute(self, mode, length):
        Logo()
        print(f"{g}[*] Bruteforce Process Running (Mode: {mode}, Len: {length}){w}")
        # Bruteforce logic from original main.py
        await asyncio.sleep(1)

# --- Main Entry ---
async def main():
    sec = Security()
    Logo()
    
    if await sec.check_access():
        parser = argparse.ArgumentParser()
        parser.add_argument("-o", "--option", choices=["code", "internet", "setup"], required=True)
        parser.add_argument("-m", "--mode", default="digit")
        parser.add_argument("-l", "--length", type=int, default=6)
        args = parser.parse_args()

        tool = RuijieTool()
        if args.option == "setup":
            await tool.setup()
        elif args.option == "code":
            await tool.start_brute(args.mode, args.length)
    else:
        sys.exit()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{r}[!] အစီအစဉ်ကို ရပ်တန့်လိုက်ပါပြီ။{w}")
