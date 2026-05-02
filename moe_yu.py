import os
import sys
import json
import time
import base64
import asyncio
import aiohttp
import requests
import urllib3
import hashlib
import platform
import subprocess
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# SSL Warning များ မပေါ်အောင် ပိတ်ခြင်း
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- Configuration ---
# GitHub Screenshot အတိုင်း URL ကို ပြင်ဆင်ထားသည်
DB_URL = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/main/key.txt"

class Star:
    def __init__(self):
        self.red = "\033[1;31m"
        self.green = "\033[1;32m"
        self.yellow = "\033[1;33m"
        self.blue = "\033[1;34m"
        self.white = "\033[1;37m"
        self.reset = "\033[0m"

    def clear(self):
        os.system('clear')

    def get_hwid(self):
        """
        Device ရဲ့ Serial Number နဲ့ Model ကိုယူပြီး 
        HWID တစ်ခု ထုတ်ပေးတဲ့ မူရင်း Logic ဖြစ်ပါတယ်။
        """
        try:
            # Android Device ID သို့မဟုတ် Serial ကို ယူခြင်း
            cmd = subprocess.check_output("getprop ro.serialno", shell=True).decode().strip()
            if not cmd:
                cmd = subprocess.check_output("getprop ro.build.id", shell=True).decode().strip()
            
            # SHA256 နဲ့ Hash လုပ်ပြီး အရှည် ၂၀ ယူခြင်း
            hwid = hashlib.sha256(cmd.encode()).hexdigest().upper()
            return hwid[:20]
        except:
            # Error တက်လျှင် Platform info ကို သုံးခြင်း
            alt_info = f"{platform.machine()}{platform.node()}"
            return hashlib.md5(alt_info.encode()).hexdigest().upper()[:20]

    def banner(self, my_id):
        self.clear()
        print(f"""{self.green}
  ██████  ████████  █████  ██████  
 ██       ──██──  ██   ██ ██   ██ 
  ██████    ██    ███████ ██████  
       ██   ██    ██   ██ ██   ██ 
  ██████    ██    ██   ██ ██   ██ 
{self.white}---------------------------------------------
{self.yellow} >> OWNER   : MOE YU
 >> VERSION : 1.0.5 (STABLE)
 >> HWID    : {my_id}
{self.white}---------------------------------------------""")

    async def check_key(self, session, hwid):
        """Database (key.txt) မှာ HWID ရှိမရှိ စစ်ဆေးခြင်း"""
        try:
            async with session.get(DB_URL) as response:
                if response.status == 200:
                    raw_data = await response.text()
                    
                    # key.txt ထဲမှာ HWID ပါသလားဆိုတာ တစ်ကြောင်းချင်းစစ်တာဖြစ်ပါတယ်
                    allowed_hwids = raw_data.strip().split('\n')
                    
                    if hwid in [h.strip() for h in allowed_hwids]:
                        return True, "Access Success!"
                    else:
                        return False, "Your ID is not registered."
                else:
                    return False, "Server Connection Failed."
        except Exception as e:
            return False, f"Error: Check your internet connection."

    async def main_logic(self):
        my_hwid = self.get_hwid()
        self.banner(my_hwid)
        
        async with aiohttp.ClientSession() as session:
            print(f"{self.blue}[*] Connecting to Database...{self.reset}")
            await asyncio.sleep(1.5)
            
            status, msg = await self.check_key(session, my_hwid)
            
            if status:
                print(f"{self.green}[+] {msg}{self.reset}")
                await self.menu()
            else:
                print(f"{self.red}[!] {msg}{self.reset}")
                print(f"{self.yellow}[!] Contact Admin: Moe Yu{self.reset}")
                sys.exit()

    async def menu(self):
        print(f"\n{self.white}[1] Start Automation Script")
        print(f"[2] Update Database Link")
        print(f"[3] Clean Termux Cache")
        print(f"[0] Exit")
        
        choice = input(f"\n{self.green}Select > {self.reset}")
        
        if choice == "1":
            print(f"{self.yellow}[*] Running main script...{self.reset}")
            # ဒီနေရာမှာ သင့်ရဲ့ အဓိက code တွေကို ဆက်ရေးနိုင်ပါတယ်
        elif choice == "2":
            os.system("git pull")
            print(f"{self.green}[+] Updated!{self.reset}")
        elif choice == "3":
            os.system("rm -rf $HOME/.cache/*")
            print(f"{self.green}[+] Cache Cleaned!{self.reset}")
            await self.menu()
        elif choice == "0":
            sys.exit()
        else:
            print(f"{self.red}Invalid Option{self.reset}")
            await self.menu()

if __name__ == "__main__":
    app = Star()
    try:
        asyncio.run(app.main_logic())
    except KeyboardInterrupt:
        print(f"\n{self.red}[!] Program Closed.{self.reset}")
