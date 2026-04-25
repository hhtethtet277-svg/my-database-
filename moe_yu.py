import requests, re, urllib3, time, threading, logging, random, sys, datetime, os, uuid
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
URL = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/refs/heads/main/key.txt"
stop_event = threading.Event()

# LOGO & BANNER
BABY_LOGO = "\n[bold cyan]      _ \n    _(_)_ \n   (_)@(_) \n     (_)\  / \n      /  || \n  ___/___||___\n |____________|[/bold cyan]"
BANNER = "[bold #00FF00]\n ╔╦╗╔═╗╔═╗  ╦ ╦╦ ╦\n ║║║║ ║║╣   ╚╦╝║ ║\n ╩ ╩╚═╝╚═╝   ╩ ╚═╝\n      [#00FF00]M O E   Y U   H A C K E R[/#00FF00][/bold #00FF00]"

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

def check_license_hacker_style():
    my_hwid = get_hwid()
    console.clear()
    console.print(Align.center(BABY_LOGO))
    console.print(Align.center(BANNER))
    console.print(Align.center(Panel(f"[bold white]YOUR HWID: [yellow]{my_hwid}[/yellow][/bold white]", title="[bold red]DEVICE INFO[/bold red]", border_style="bold cyan", expand=False)))
    
    user_key = input("\n  [SECURITY_ACCESS] @MoeYu_").strip()
    if not user_key: sys.exit()
    
    try:
        res = requests.get(URL, timeout=10)
        lines = [l.strip() for l in res.text.splitlines() if l.strip()]
        for entry in lines:
            parts = entry.split("|") # Format: Key | Expiry | HWID
            if len(parts) >= 1 and user_key == parts[0].strip():
                # HWID Check
                db_hwid = parts[2].strip() if len(parts) > 2 else "FREE"
                if db_hwid != "FREE" and db_hwid != my_hwid:
                    console.print("\n[bold red]❌ HWID MISMATCH![/bold red]"); sys.exit()
                # Expiry Check
                is_active, date_label = check_expiry(parts[1].strip() if len(parts) > 1 else "None")
                if is_active:
                    console.print(f"\n[bold green]✅ ACCESS GRANTED | EXPIRY: {date_label}[/bold green]\n")
                    return True
                else:
                    console.print(f"\n[bold red]❌ KEY EXPIRED (Date: {date_label})![/bold red]"); sys.exit()
        console.print("\n[bold red]❌ INVALID KEY![/bold red]"); sys.exit()
    except:
        console.print("\n[bold red]📡 CONNECTION ERROR![/bold red]"); sys.exit()

def start_bypass_process():
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36'})
    
    while not stop_event.is_set():
        try:
            r = session.get("http://connectivitycheck.gstatic.com/generate_204", timeout=5, allow_redirects=True)
            if r.status_code == 204:
                time.sleep(5)
                continue
            
            portal_url = r.url
            page = session.get(portal_url, timeout=10, verify=False)
            
            # --- DETECT PORTAL ---
            form = re.search(r'<form.*?action=["\'](.*?)["\'].*?>', page.text, re.DOTALL)
            auth_link = None
            
            if form:
                action = form.group(1)
                auth_url = action if action.startswith('http') else urljoin(portal_url, action)
                inputs = re.findall(r'<input.*?name=["\'](.*?)["\'].*?value=["\'](.*?)["\']', page.text)
                data = {name: val for name, val in inputs}
                session.post(auth_url, data=data)
                auth_link = auth_url
            else:
                sid = re.search(r'sessionId=([a-zA-Z0-9]+)', page.text)
                if sid:
                    p = parse_qs(urlparse(portal_url).query)
                    gw = p.get('gw_address',['192.168.60.1'])[0]
                    pt = p.get('gw_port',['2060'])[0]
                    auth_link = f"http://{gw}:{pt}/wifidog/auth?token={sid.group(1)}"

            if auth_link:
                def pulse_ping():
                    while not stop_event.is_set():
                        try:
                            session.get(auth_link, timeout=5)
                            sys.stdout.write(f"\r[✓] SID Active | Turbo Pulse Running...")
                            sys.stdout.flush()
                        except: pass
                        time.sleep(2)

                for _ in range(PING_THREADS):
                    threading.Thread(target=pulse_ping, daemon=True).start()
                
                while True:
                    if session.get("http://www.google.com", timeout=3).status_code != 200: break
                    time.sleep(10)
        except: time.sleep(5)

if __name__ == "__main__":
    if check_license_hacker_style():
        console.print(Panel(Align.center("[bold white]🔥 MOE YU BYPASS ACTIVATED 🔥[/bold white]"), border_style="bold red", expand=False))
        try: start_bypass_process()
        except KeyboardInterrupt: sys.exit()
