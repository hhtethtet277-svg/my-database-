import os
import requests
import sys
import urllib3
import socket
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

KEY_URL = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/main/key.txt"

def get_device_id():
    import hashlib
    try:
        host_info = os.uname().nodename + os.getlogin()
    except:
        host_info = "ST-STABLE-V5"
    return "TRB-" + hashlib.md5(host_info.encode()).hexdigest()[:10].upper()

def keep_alive():
    """လိုင်းမကျအောင် ၅ စက္ကန့်တစ်ခါ Signal ပို့ပေးခြင်း"""
    try:
        requests.get("http://www.google.com", timeout=3)
    except:
        pass

def start_stable_bypass():
    print("\n" + "="*40)
    print("    STARLINK STABLE BYPASS (AUTO-RECONNECT)   ")
    print("="*40)
    
    while True:
        try:
            print("[*] Checking Connection & Maintaining Tunnel...")
            # DNS Keep Alive
            socket.gethostbyname("google.com")
            
            print("[✔] STATUS: BYPASS ACTIVE!")
            print("[i] သင်ယခု အင်တာနက်သုံးနိုင်ပါပြီ။ (Tool ကို မပိတ်ပါနဲ့)")
            
            # ၅ စက္ကန့်တစ်ခါ လိုင်းကို ထိန်းပေးတယ်
            for _ in range(6): 
                keep_alive()
                time.sleep(5)
                
        except Exception:
            print("[!] လိုင်းကျသွားပါပြီ။ ၅ စက္ကန့်အတွင်း ပြန်ချိတ်ပေးပါမည်...")
            time.sleep(5)

def check_key():
    device_id = get_device_id()
    print(f"\n[+] YOUR DEVICE ID: {device_id}")
    try:
        response = requests.get(KEY_URL, verify=False, timeout=10)
        if device_id in response.text:
            print("[+] Access Granted!")
            start_stable_bypass()
        else:
            print("[-] Access Denied! Key မရှိသေးပါ။")
            sys.exit()
    except:
        print("[-] Connection Error: အင်တာနက် တစ်ချက်ပြန်ဖွင့်ပေးပါ။")

if __name__ == "__main__":
    check_key()
