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
from rich.align import Align

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
console = Console()
stop_event = threading.Event()

GREEN = "\033[1;32m"
CYAN = "\033[1;36m"
WHITE = "\033[1;37m"
RED = "\033[1;31m"
YELLOW = "\033[1;33m"
RESET = "\033[0m"

KEY_URL = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/main/key.txt"

AI_BANNER = """
[bold cyan]
  █████  ██     ██████  ██████  ██████  ███████ 
 ██   ██ ██     ██   ██ ██   ██ ██   ██ ██      
 ███████ ██     ██████  ██████  ██████  ███████ 
 ██   ██ ██     ██   ██ ██      ██           ██ 
 ██   ██ ██     ██████  ██████  ██████  ███████ 
[/bold cyan]
[bold white] >>> GAMING MODE VOUCHER BYPASS SYSTEM <<< [/bold white]
"""

def get_hwid():
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

def get_sid_automatically():
    try:
        res = requests.get("http://connectivitycheck.gstatic.com/generate_204", timeout=5, allow_redirects=True)
        portal_url = res.url
        params = parse_qs(urlparse(portal_url).query)
        sid = params.get('sessionId', [None])[0]
        return sid, portal_url
    except:
        return None, None

def pulse_log(sid):
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
        try:
            p = parse_qs(urlparse(portal_url).query)
            gw_addr = p.get('gw_address', ['192.168.110.1'])[0]
            gw_port = p.get('gw_port', ['2060'])[0]
            auth_url = f"http://{gw_addr}:{gw_port}/wifidog/auth?token={sid}"
            requests.get(auth_url, timeout=5)
        except: pass
        threading.Thread(target=pulse_log, args=(sid,), daemon=True).start()
        while True: time.sleep(1)
    else:
        print(f"{RED}[!] PORTAL NOT FOUND. PLEASE CONNECT TO WIFI FIRST!{RESET}")

def main():
    hwid = get_hwid()
    display_activation_screen(hwid)
    key_input = console.input(f"\n{CYAN}[?] Activation Key: {RESET}").strip()
    try:
        response = requests.get(KEY_URL, timeout=10)
        lines = response.text.splitlines()
        # ရှေ့ဆုံးက Key တစ်ခုတည်းကိုပဲ ခွဲထုတ်ပြီး စစ်ဆေးခြင်း
        valid_keys = [line.split('|')[0].strip() for line in lines if line.strip()]
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
