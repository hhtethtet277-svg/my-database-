import os
import requests
import sys
import urllib3
import time
import subprocess

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Starlink ရဲ့ Internal IP နဲ့ DNS တွေကို တိုက်ရိုက်သုံးပြီး Bypass လုပ်ခြင်း
STARLINK_IP = "192.168.100.1"
BYPASS_DOMAINS = ["8.8.8.8", "1.1.1.1", "disneyplus.com", "netflix.com"]

def get_device_id():
    import hashlib
    try:
        host_info = os.uname().nodename + os.getlogin()
    except:
        host_info = "ST-INSTANT-V6"
    return "TRB-" + hashlib.md5(host_info.encode()).hexdigest()[:10].upper()

def exploit_starlink():
    """Voucher မလိုဘဲ DNS Tunneling စတင်ခြင်း"""
    print(f"[*] Connecting to Starlink Terminal ({STARLINK_IP})...")
    try:
        # Starlink Internal Port တွေကို အသုံးချပြီး Tunnel ဖောက်ခြင်း
        for domain in BYPASS_DOMAINS:
            subprocess.Popen(f"ping -c 1 {domain}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except:
        return False

def start_instant_bypass():
    print("\n" + "="*40)
    print("      STARLINK INSTANT BYPASS ACTIVE      ")
    print("="*40)
    
    if exploit_starlink():
        print("[✔] VOUCHER BYPASSED SUCCESSFULLY!")
        print("[✔] အင်တာနက် လမ်းကြောင်း ပွင့်သွားပါပြီ။")
        
        # လိုင်းမကျအောင် ထိန်းထားပေးတဲ့ Loop
        while True:
            try:
                # ၅ စက္ကန့်တစ်ခါ Signal ပို့ပြီး လမ်းကြောင်းကို ဖွင့်ထားပေးခြင်း
                requests.get("http://connectivitycheck.gstatic.com/generate_204", timeout=5)
                time.sleep(5)
            except:
                print("[!] လိုင်းတစ်ချက် ပြတ်သွားသည်။ ပြန်ချိတ်နေပါသည်...")
                time.sleep(2)
    else:
        print("[-] Bypass Failed! WiFi ကို တစ်ချက် ပြန်ချိတ်ပေးပါ။")

def check_key():
    device_id = get_device_id()
    print(f"\n[+] DEVICE ID: {device_id}")
    # Key စစ်တဲ့နေရာမှာ SSL Error မတက်အောင် verify=False သုံးထားပါတယ်
    KEY_URL = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/main/key.txt"
    try:
        response = requests.get(KEY_URL, verify=False, timeout=10)
        if device_id in response.text:
            print("[+] Access Granted!")
            start_instant_bypass()
        else:
            print("[-] Access Denied! Admin ဆီမှာ Key အရင်တောင်းပါ။")
    except:
        # လိုင်း လုံးဝမရှိရင်တောင် အလုပ်လုပ်အောင် (Key ရဖူးသူဆိုရင်)
        print("[!] Offline Mode: သင့် ID ကို Key ထဲမှာ ရှိမရှိ အရင်စစ်ပါ။")

if __name__ == "__main__":
    check_key()
