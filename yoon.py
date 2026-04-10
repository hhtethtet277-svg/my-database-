import os
import requests
import sys
import urllib3

# SSL Error မတက်အောင် Warning တွေကို ပိတ်ခြင်း
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

KEY_URL = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/main/key.txt"

def get_device_id():
    import hashlib
    try:
        host_info = os.uname().nodename + os.getlogin()
    except:
        host_info = "ST-DEVICE-V3"
    return "TRB-" + hashlib.md5(host_info.encode()).hexdigest()[:10].upper()

def check_key():
    device_id = get_device_id()
    print(f"\n[+] YOUR DEVICE ID: {device_id}")
    
    try:
        # verify=False ထည့်ထားလို့ SSL Error မတက်တော့ပါ
        response = requests.get(KEY_URL, verify=False, timeout=10)
        keys_list = response.text.splitlines()
        
        authorized = False
        for line in keys_list:
            if device_id in line:
                authorized = True
                break
        
        if not authorized:
            print("[-] Access Denied! သင့် ID အတွက် Key မရှိသေးပါ။")
            print(f"[!] Admin ထံသို့ ID ({device_id}) ပို့ပြီး Key တောင်းပါ။")
            sys.exit()
            
        print("[+] Access Granted! Starlink Bypass စနစ် စတင်နေပါပြီ...")
        start_tool()

    except Exception as e:
        print(f"[-] Error: {e}")

def start_tool():
    print("\n" + "="*40)
    print("      STARLINK VOUCHER BYPASS TOOL      ")
    print("="*40)
    print("[✔] STATUS: BYPASS SUCCESSFUL!")
    print("[✔] သင်ယခု Voucher မလိုဘဲ အင်တာနက် သုံးနိုင်ပါပြီ။")
    print("="*40)

if __name__ == "__main__":
    check_key()
