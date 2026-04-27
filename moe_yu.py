import asyncio
import aiohttp
import sys
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from tqdm.asyncio import tqdm

# Configuration
CONFIG = {
    "timeout": 5,
    "concurrency_limit": 50, # 200 က များလွန်းလို့ Server က Block လုပ်နိုင်ပါတယ်
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) MoeYuSAN/1.0"
}

console = Console()

class MoeYuSANEngine:
    def __init__(self):
        self.banner = "[bold cyan]M O E   Y U   S A N   P R O   E N G I N E[/bold cyan]"

    def display_banner(self):
        console.clear()
        console.print(Align.center(self.banner))
        console.print(Align.center("[bold green]v7.8 - Professional API Tester[/bold green]\n"))

    async def test_endpoint(self, session, url, payload_key, value):
        """Standardized Request Template"""
        try:
            # တကယ်တမ်းဆိုရင်တော့ ဒီနေရာမှာ headers တွေ tokens တွေ အစုံလိုအပ်ပါတယ်
            async with session.post(url, data={payload_key: value}, timeout=CONFIG["timeout"]) as resp:
                status = resp.status
                text = await resp.text()
                
                # Success criteria (ဒီနေရာမှာ ကိုယ်စမ်းမယ့် API အပေါ်မူတည်ပြီး ပြင်ပါ)
                if status == 200 and "Login Success" in text:
                    return value, True
        except Exception:
            pass
        return value, False

    async def run_engine(self, url, payload_key, start, end):
        console.print(f"[yellow][*] Starting Target: {url}[/yellow]")
        
        connector = aiohttp.TCPConnector(limit=CONFIG["concurrency_limit"])
        async with aiohttp.ClientSession(connector=connector, headers={"User-Agent": CONFIG["user_agent"]}) as session:
            tasks = []
            for i in range(start, end + 1):
                tasks.append(self.test_endpoint(session, url, payload_key, str(i)))
            
            # Progress tracker
            for f in tqdm.as_completed(tasks, desc="Processing"):
                val, success = await f
                if success:
                    console.print(f"\n[bold green][+] Match Found: {val}[/bold green]")
                    return

def main():
    engine = MoeYuSANEngine()
    while True:
        engine.display_banner()
        console.print(Panel("[white]1. Run Test\n2. Exit[/white]", title="[cyan]MENU[/cyan]"))
        choice = input(" [?] Option: ")
        
        if choice == "1":
            target = input(" [>] Target URL: ")
            key = input(" [>] Payload Key: ")
            s = int(input(" [>] Start: "))
            e = int(input(" [>] End: "))
            asyncio.run(engine.run_engine(target, key, s, e))
            input("\n[!] Finished. Press Enter...")
        elif choice == "2":
            sys.exit()

if __name__ == "__main__":
    main()
