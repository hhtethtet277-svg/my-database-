import requests
import re
import urllib3
import time
import threading
import random
import sys
import datetime
import os
from urllib.parse import urlparse, parse_qs
from rich.console import Console
from rich.panel import Panel
from rich.align import Align

# --- Configuration ---
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
console = Console()
stop_event = threading.Event()

# Colors
GREEN = "\033[1;32m"
CYAN = "\033[1;36m"
WHITE = "\033[1;37m"
RED = "\033[1;31m"
YELLOW = "\033[1;33m"
RESET = "\033[0m"

# GitHub Key database
KEY_URL = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/main/key.txt"

# --- UI Design ---
AI_BANNER = """
[bold cyan]
  █████  ██     ██████  ██████  ██████  ███████ 
 ██   ██ ██     ██   ██ ██   ██ ██   ██ ██      
 ███████ ██     ██████  ██████  ██████  ███████ 
 ██   ██ ██     ██   ██ ██      ██           ██ 
 ██   ██ ██     ██████  ██      ██      ███████ 
[/bold cyan]
[bold white] >>> GAMING MODE VOUCHER BYPASS SYSTEM <<< [/bold white]
"""

def get_hwid():
    # ပုံထဲကအတိုင်း Device ID ထုတ်ပေးခြင်း
    return "KEY-2B6F4CE00A"

def display_activation_screen(hwid):
    console.clear()
    console.print(Align.center(AI_BANNER))
    info = f"""
[bold yellow]╔══════════════════════════════════════════╗[/bold yellow]
[bold yellow]║[/bold yellow] [cyan]DEVICE ID[/cyan]   : [green]{hwid}[/green]          [bold yellow]║[/bold yellow]
[bold yellow]║[/bold yellow] [cyan]STATUS[/cyan]      : [red]PENDING ACTIVATION[/red]    [bold yellow]║[/bold yellow]
[bold yellow]╚══════════════════════════════════════════╝[/bold yellow]
"""
    console.print(Align.center(info))

# --- Core Logic ---
def get_sid_automatically():
    # Ruijie/Starlink portal ကို ရှာဖွေခြင်း
    try:
        res = requests.get("http://connectivitycheck.gstatic.com/generate_204", timeout=5, allow_redirects=True)
        portal_url = res.url
        params = parse_qs(urlparse(portal_url).query)
        sid = params.get('sessionId', [None])[0]
        return sid, portal_url
    except:
        return None, None

def pulse_log(sid):
    # Bypass လုပ်ဆောင်ချက်ပြသခြင်း (Video ထဲကအတိုင်း)
    while not stop_event.is_set():
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        core_id = random.randint(100000, 999999)
        sys.stdout.write(f"{WHITE}[{ts}]{RESET} {GREEN}AI_CORE: THR=30 INT=0.01s SID={sid}{RESET}\n{GREEN}ODE={core_id}...{RESET}\n")
        sys.stdout.flush()
        time.sleep(0.04)

def start_bypass_engine():
    console.clear()
    console.print(Align.center(AI_BANNER))
    print(f"{CYAN}[*] SEARCHING FOR VOUCHER PORTAL...{RESET}")
    
    sid, portal_url = get_sid_automatically()
    
    if sid:
        print(f"{GREEN}[+] PORTAL FOUND! SID: {sid}{RESET}")
        # Auth request ပို့ခြင်း
        try:
            p = parse_qs(urlparse(portal_url).query)
            auth_url = f"http://{p.get('gw_address',['192.168.110.1'])[0]}:{p.get('gw_port',['2060'])[0]}/wifidog/auth?token={sid}"
            requests.get(auth_url, timeout=5)
        except: pass

        threading.Thread(target=pulse_log, args=(sid,), daemon=True).start()
        while True: time.sleep(1)
    else:
        print(f"{RED}[!] PORTAL NOT FOUND. PLEASE CONNECT TO WIFI FIRST!{RESET}")

# --- Activation & Main ---
def main():
    hwid = get_hwid()
    display_activation_screen(hwid)
    
    key_input = console.input(f"\n{CYAN}[?] Activation Key: {RESET}")
    
    # Key စစ်ဆေးခြင်း
    try:
        response = requests.get(KEY_URL, timeout=10)
        valid_keys = response.text.splitlines()
        
        if key_input in valid_keys:
            console.print(f"\n{GREEN}[+] ACTIVATION SUCCESSFUL!{RESET}")
            time.sleep(1.5)
            start_bypass_engine()
        else:
            console.print(f"\n{RED}[!] INVALID ACTIVATION KEY!{RESET}")
    except:
        console.print(f"\n{RED}[!] SERVER ERROR. CHECK INTERNET!{RESET}")

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: sys.exit()
