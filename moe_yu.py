import os
import sys
import json
import time
import asyncio
import aiohttp
import hashlib
import platform
import subprocess
from datetime import datetime

# --- Configuration ---
# GitHub Raw Link အမှန်ဖြစ်ရပါမယ်
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
        try:
            cmd = subprocess.check_output("getprop ro.serialno", shell=True).decode().strip()
            if not cmd:
                cmd = subprocess.check_output("getprop ro.build.id", shell=True).decode().strip()
            hwid = hashlib.sha256(cmd.encode()).hexdigest().upper()
            return hwid[:20]
        except:
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
 >> VERSION : 1.0.6 (EXPIRY SYSTEM)
 >> HWID    : {my_id}
{self.white}---------------------------------------------""")

    async def check_key(self, session, my_hwid):
        try:
            async with session.get(DB_URL) as response:
                if response.status == 200:
                    raw_data = await response.text()
                    lines = raw_data.strip().split('\n')
                    
                    for line in lines:
                        if "|" in line:
                            db_hwid, exp_date_str = line.split("|")
                            db_hwid = db_hwid.strip()
                            exp_date_str = exp_date_str.strip()

                            if my_hwid == db_hwid:
                                # ရက်စွဲကို စစ်ဆေးခြင်း
                                try:
                                    exp_date = datetime.strptime(exp_date_str, "%Y-%m-%d")
                                    current_date = datetime.now()

                                    if current_date < exp_date:
                                        return True, f"Access Granted! Exp: {exp_date_str}"
                                    else:
                                        return False, f"Key Expired on {exp_date_str}"
                                except ValueError:
                                    return False, "Invalid Date Format in Database (Use YYYY-MM-DD)"
                    
                    return False, "Your ID is not registered."
                else:
                    return False, "Server Connection Failed."
        except Exception as e:
            return False, "Check your internet connection."

    async def main_logic(self):
        my_hwid = self.get_hwid()
        self.banner(my_hwid)
        
        async with aiohttp.ClientSession() as session:
            print(f"{self.blue}[*] Checking License and Expiry...{self.reset}")
            await asyncio.sleep(1)
            
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
        print(f"[0] Exit")
        choice = input(f"\n{self.green}Select > {self.reset}")
        if choice == "1":
            print(f"{self.yellow}[*] Running main script...{self.reset}")
        else:
            sys.exit()

if __name__ == "__main__":
    app = Star()
    try:
        asyncio.run(app.main_logic())
    except KeyboardInterrupt:
        print(f"\n{self.red}[!] Program Closed.{self.reset}")
