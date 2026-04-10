import os
import requests
import sys
import urllib3
import time
import subprocess
import hashlib

# SSL Warning များ ပိတ်ထားခြင်း
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

KEY_URL = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/main/key.txt"
CACHE_FILE = ".access_granted"

def get_device_id():
    try:
        host_info = os.uname().nodename + os.getlogin()
    except:
        host_info = "ST-ULTRA-V7"
    return "TRB-" + hashlib.md5(host_info.encode()).hexdigest()[:10].upper()

def start_instant_bypass():
    print("\n" + "="*40)
    print("      STARLINK INSTANT BYPASS ACTIVE      ")
    print("="*40)
    print("[*] Connecting to Starlink Terminal...")
    
    # DNS Tunneling & Keep Alive စနစ်
    try:
        while True:
            # Starlink Portal ကို ကျော်ရန် Google Connectivity Check ကို သုံးခြင်း
            requests.get("http://connectivitycheck.gstatic.com/generate_204", timeout=5)
            print("[✔] STATUS: BYPASS SUCCESSFUL!")
            print("[i] အင်တာနက် အသုံးပြုနိုင်ပါပြီ။ Tool ကို မပိတ်ပါနဲ့။")
            time.sleep(10)
    except:
        print("[!] လိုင်းတစ်ချက် ပြတ်သွားသည်။ ပြန်ချိတ်နေပါသည်...")
        time.sleep(2)
        start_instant_bypass()

def check_key():
    device_id = get_device_id()
    print(f"\n[+] YOUR DEVICE ID: {device_id}")
    
    # ၁။ အင်တာနက်ရှိရင် GitHub က Key ကို အရင်စစ်မယ်
    try:
        response = requests.get(KEY_URL, verify=False, timeout=5)
        if device_id in response.text:
            # Key မှန်ရင် ဖုန်းထဲမှာ မှတ်တမ်း (Cache) သိမ်းမယ်
            with open(CACHE_FILE, "w") as f:
                f.write(device_id)
            print("[+] Access Granted! (Online Verified)")
            start_instant_bypass()
            return
    except:
        # ၂။ အင်တာနက်မရှိရင် ဖုန်းထဲက မှတ်တမ်းဟောင်းကို စစ်မယ်
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r") as f:
                if f.read().strip() == device_id:
                    print("[+] Access Granted! (Offline Mode - Cached)")
                    start_instant_bypass()
                    return

    # ၃။ နှစ်ခုလုံးမရှိရင် Access Denied ပြမယ်
    print("[-] Access Denied! Key မရှိသေးပါ။")
    print("[!] ပထမဆုံးအကြိမ်အတွက် Mobile Data/VPN ဖြင့် Key အရင်စစ်ပေးပါ။")
    sys.exit()

if __name__ == "__main__":
    check_key()
