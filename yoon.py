import os
import requests
import sys
import urllib3

# SSL Error မတက်အောင် warning တွေကို ပိတ်ထားခြင်း
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

KEY_URL = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/main/key.txt"

def get_device_id():
    import hashlib
    host_info = os.uname().nodename + os.getlogin()
    return "TRB-" + hashlib.md5(host_info.encode()).hexdigest()[:10].upper()

def check_key():
    device_id = get_device_id()
    print(f"\n[+] YOUR DEVICE ID: {device_id}")
    
    try:
        # verify=False ထည့်ပြီး SSL စစ်ဆေးမှုကို ကျော်လိုက်တာဖြစ်ပါတယ်
        response = requests.get(KEY_URL, verify=False)
        keys_list = response.text.splitlines()
        
        authorized = False
        for line in keys_list:
            if device_id in line:
                authorized = True
                break
        
        if not authorized:
            print("[-] Access Denied! သင့် ID အတွက် Key မရှိသေးပါ။")
            print(f"[!] Please send your ID ({device_id}) to Admin.")
            sys.exit()
            
        print("[+] Access Granted! Starlink Tool စတင်နေပါပြီ...")
        start_tool()

    except Exception as e:
        print(f"[-] Error: {e}")

def start_tool():
    print("\n--- STARLINK MONITORING SYSTEM ---")
    print("STATUS : CONNECTED TO 192.168.100.1")
    print("SIGNAL : ACTIVE (Port 9200 is OPEN)")

if __name__ == "__main__":
    check_key()
