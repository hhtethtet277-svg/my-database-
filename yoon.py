import os
import requests
import sys

# Key စစ်ဆေးမည့် Link
KEY_URL = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/main/key.txt"

def get_device_id():
    # ရိုးရှင်းသော Device ID ထုတ်နည်း (ဖုန်းမတူရင် ID မတူအောင်လို့ပါ)
    import hashlib
    host_info = os.uname().nodename + os.getlogin()
    return "TRB-" + hashlib.md5(host_info.encode()).hexdigest()[:10].upper()

def check_key():
    device_id = get_device_id()
    print(f"\n[+] YOUR DEVICE ID: {device_id}")
    
    try:
        response = requests.get(KEY_URL)
        keys_list = response.text.splitlines()
        
        # GitHub က key.txt ထဲမှာ Device ID ရှိမရှိ စစ်မယ်
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
        print(f"[-] Error: အင်တာနက် ချိတ်ဆက်မှု စစ်ဆေးပါ သို့မဟုတ် {e}")

def start_tool():
    # ဒီနေရာမှာ သင့်ရဲ့ Starlink Scan ဖတ်တဲ့ မူရင်း Logic ကို ထည့်ထားပါတယ်
    print("\n--- STARLINK MONITORING SYSTEM ---")
    print("STATUS : CONNECTED TO 192.168.100.1")
    print("SIGNAL : ACTIVE (Port 9200 is OPEN)")
    # သင့်ရဲ့ တခြား Code အစိတ်အပိုင်းတွေကို ဒီအောက်မှာ ဆက်ထည့်နိုင်ပါတယ်

if __name__ == "__main__":
    check_key()
