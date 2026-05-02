import requests
import re
import urllib3
import time
import threading
import random
import sys
import datetime
import os
from urllib.parse import urlparse, parse_qs, urljoin
from rich.console import Console
from rich.align import Align

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
console = Console()
stop_event = threading.Event()

GREEN = "\033[1;32m"
CYAN = "\033[1;36m"
WHITE = "\033[1;37m"
RED = "\033[1;31m"
RESET = "\033[0m"

AI_BANNER = """
[bold cyan]
  █████  ██     ██████  ██████  ██████  ███████ 
 ██   ██ ██     ██   ██ ██   ██ ██   ██ ██      
 ███████ ██     ██████  ██████  ██████  ███████ 
 ██   ██ ██     ██   ██ ██      ██           ██ 
 ██   ██ ██     ██████  ██      ██      ███████ 
[/bold cyan]
[bold white] >>> STARLINK & RUIJIE AUTO-BYPASS PRO <<< [/bold white]
"""

def get_sid_automatically():
    """Voucher Page ကနေ SID ကို Auto နှိုက်ယူတဲ့စနစ်"""
    try:
        session = requests.Session()
        # Google ဆီကို အရင်သွားပြီး Portal Link ကို ဖမ်းယူခြင်း
        res = session.get("http://connectivitycheck.gstatic.com/generate_204", timeout=5, allow_redirects=True)
        portal_url = res.url
        
        # URL ထဲက sessionId ကို ရှာခြင်း
        parsed_url = urlparse(portal_url)
        params = parse_qs(parsed_url.query)
        sid = params.get('sessionId', [None])[0]
        
        if not sid:
            # URL ထဲမှာ မပါရင် Page ထဲက Code ထဲမှာ ထပ်ရှာခြင်း
            res_page = session.get(portal_url, timeout=5, verify=False)
            sid_match = re.search(r'sessionId=([a-zA-Z0-9\-]+)', res_page.text)
            sid = sid_match.group(1) if sid_match else None
            
        return sid, portal_url
    except:
        return None, None

def pulse_log(sid):
    while not stop_event.is_set():
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        core_id = random.randint(100000, 999999)
        sys.stdout.write(f"{WHITE}[{ts}]{RESET} {GREEN}AI_CORE: THR=30 SID={sid}{RESET}\n{GREEN}BYPASSING_PORTAL... ODE={core_id}{RESET}\n")
        sys.stdout.flush()
        time.sleep(0.05)

def start_engine():
    console.clear()
    console.print(Align.center(AI_BANNER))
    print(f"{CYAN}[*] SEARCHING FOR VOUCHER PORTAL...{RESET}")
    
    sid, portal_url = get_sid_automatically()
    
    if sid:
        print(f"{GREEN}[+] PORTAL FOUND! SID: {sid}{RESET}")
        print(f"{GREEN}[+] STARLINK/RUIJIE DETECTED. STARTING ENGINE...{RESET}\n")
        
        # Bypass Request ပို့ခြင်း (Ruijie Auth Logic)
        try:
            p = parse_qs(urlparse(portal_url).query)
            gw_addr = p.get('gw_address', ['192.168.110.1'])[0]
            gw_port = p.get('gw_port', ['2060'])[0]
            auth_url = f"http://{gw_addr}:{gw_port}/wifidog/auth?token={sid}"
            requests.get(auth_url, timeout=5)
        except: pass

        threading.Thread(target=pulse_log, args=(sid,), daemon=True).start()
        
        while True:
            try:
                # ၅ စက္ကန့်တစ်ခါ အင်တာနက်စစ်ပြီး အလိုအလျောက် Refresh လုပ်ပေးခြင်း
                if requests.get("http://www.google.com", timeout=3).status_code == 200:
                    time.sleep(10)
                else:
                    # အင်တာနက် ပြန်ပြတ်သွားရင် SID အသစ်ပြန်ယူ
                    sid, _ = get_sid_automatically()
            except: time.sleep(2)
    else:
        print(f"{RED}[!] PORTAL NOT FOUND. PLEASE CONNECT TO WIFI FIRST!{RESET}")

if __name__ == "__main__":
    try: start_engine()
    except KeyboardInterrupt: sys.exit()
