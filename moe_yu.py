import requests, re, urllib3, time, threading, logging, sys, os, uuid, signal, datetime
from urllib.parse import urlparse, parse_qs, urljoin
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text

# ==========================================
# CONFIGURATION
# ==========================================
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
console = Console()
stop_event = threading.Event()
LICENSE_URL = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/refs/heads/main/key.txt"

logging.basicConfig(filename='bypass_engine.log', level=logging.INFO, format="%(asctime)s | %(message)s")

# UI Elements
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
BANNER = "[bold #00FF00]M O E   Y U   B Y P A S S   P R O   V 5 . 4 (HYBRID)[/bold #00FF00]"

# ==========================================
# LICENSE & HWID SYSTEM
# ==========================================
def get_hwid():
    id_file = os.path.expanduser("~/.moe_yu_id")
    if os.path.exists(id_file):
        with open(id_file, "r") as f: return f.read().strip()
    new_id = f"MOE-{str(uuid.uuid4()).split('-')[0].upper()}"
    with open(id_file, "w") as f: f.write(new_id)
    return new_id

def check_expiry(expiry_str):
    if expiry_str.upper() in ["NONE", "LIFETIME", "FREE"]: return True, "Lifetime"
    try:
        expiry_date = datetime.datetime.strptime(expiry_str, '%Y-%m-%d')
        if datetime.datetime.now() > expiry_date: return False, expiry_date.strftime('%d-%b-%Y')
        return True, expiry_date.strftime('%d-%b-%Y')
    except: return True, "Lifetime"

def verify_license():
    console.clear()
    console.print(Align.center(BABY_LOGO))
    console.print(Align.center(BANNER))
    my_hwid = get_hwid()
    console.print(Panel(f"[bold white]YOUR HWID: [yellow]{my_hwid}[/yellow][/bold white]", expand=False))
    
    user_key = console.input("\n[bold green]>>> Enter Access Key:[/bold green] ").strip()
    if not user_key: sys.exit()

    try:
        res = requests.get(LICENSE_URL, timeout=10)
        for line in res.text.splitlines():
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 1 and user_key == parts[0]:
                db_hwid = parts[2] if len(parts) > 2 else "FREE"
                if db_hwid != "FREE" and db_hwid != my_hwid:
                    console.print("[bold red]❌ HWID MISMATCH![/bold red]"); sys.exit()
                is_active, date_label = check_expiry(parts[1] if len(parts) > 1 else "None")
                if is_active:
                    console.print(f"[bold green]✅ ACCESS GRANTED | Status: {date_label}[/bold green]\n")
                    return True
                else:
                    console.print(f"[bold red]❌ KEY EXPIRED![/bold red]"); sys.exit()
        console.print("[bold red]❌ INVALID KEY![/bold red]"); sys.exit()
    except Exception as e:
        console.print(f"[bold red]📡 Connection Error: {e}[/bold red]"); sys.exit()

# ==========================================
# HYBRID ENGINE LOGIC
# ==========================================
def pulse_ping(auth_link):
    session = requests.Session()
    while not stop_event.is_set():
        try: session.get(auth_link, timeout=5)
        except: pass
        time.sleep(2)

def start_engine():
    console.print("[bold cyan]>> Engine Started. Monitoring Network...[/bold cyan]")
    session = requests.Session()
    while not stop_event.is_set():
        try:
            r = session.get("http://connectivitycheck.gstatic.com/generate_204", timeout=5)
            if r.status_code == 204:
                time.sleep(10)
                continue
            
            # Detect Portal
            r1 = session.get("http://neverssl.com", timeout=10, verify=False)
            portal_url = r1.url
            
            # HYBRID DETECTION: ရှာဖွေပုံနည်းလမ်းနှစ်မျိုး
            # 1. Standard sessionId
            # 2. Old-style token/nas_id
            sid_match = re.search(r'(?:sessionId|token|nas_id)=([a-zA-Z0-9]+)', r1.text)
            sid = sid_match.group(1) if sid_match else None
            
            # URL ထဲမှာပါမပါ ထပ်စစ်
            if not sid:
                p = parse_qs(urlparse(portal_url).query)
                sid = p.get('sessionId', [None])[0] or p.get('token', [None])[0]

            if sid:
                p = parse_qs(urlparse(portal_url).query)
                gw = p.get('gw_address', ['192.168.60.1'])[0]
                port = p.get('gw_port', ['2060'])[0]
                
                # အဟောင်း/အသစ် ကြိုက်တာဖြစ်ဖြစ် Auth Link တည်ဆောက်ခြင်း
                auth_link = f"http://{gw}:{port}/wifidog/auth?token={sid}"
                
                console.print(f"[bold yellow]>> Portal Detected! SID/Token: {sid[:10]}... Activating Pulse[/bold yellow]")
                threading.Thread(target=pulse_ping, args=(auth_link,), daemon=True).start()
            
            time.sleep(5)
        except Exception as e:
            logging.error(f"Loop Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda s, f: (stop_event.set(), sys.exit(0)))
    if verify_license():
        start_engine()
