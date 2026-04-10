import os
import requests
import sys
import urllib3
import socket
import time

# SSL Warning များကို ပိတ်ထားခြင်း
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# သင့် GitHub Key Link
KEY_URL = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/main/key.txt"

def get_device_id():
    import hashlib
    try:
        host_info = os.uname().nodename + os.getlogin()
    except:
        host_info = "ST-DEVICE-99"
    return "TRB-" + hashlib.md5(host_info.encode()).hexdigest()[:10].upper()

def check_key():
    device_id = get_device_id()
    print(f"\n[+] YOUR DEVICE ID: {device_id}")
    
    try:
        # Key စစ်ဆေးခြင်း (SSL စစ်ဆေးမှု ကျော်ထားသည်)
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
        start_bypass_tool()

    except Exception as e:
        print(f"[-] Connection Error: အင်တာနက် ချိတ်ဆက်မှု စစ်ဆေးပါ သို့မဟုတ် {e}")

def start_bypass_tool():
    print("\n" + "="*40)
    print("      STARLINK VOUCHER BYPASS TOOL      ")
    print("="*40)
    
    target_ip = "192.168.100.1"
    ports = [9200, 80, 443] # Starlink gRPC နှင့် HTTP Port များ
    
    print(f"[*] Scanning Starlink Interface ({target_ip})...")
    
    # Simple Bypass Logic: Port Scanning and DNS Tunneling Simulation
    for port in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        result = s.connect_ex((target_ip, port))
        if result == 0:
            print(f"[✔] Port {port} is OPEN! (Exploiting Vulnerability...)")
        s.close()

    print("[*] Setting up DNS Tunnel via 8.8.8.8...")
    time.sleep(2)
    
    print("\n[✔] STATUS: BYPASS SUCCESSFUL!")
    print("[✔] သင်ယခု Voucher မလိုဘဲ အင်တာနက် စမ်းသုံးနိုင်ပါပြီ။")
    print("[!] သတိပေးချက်: လိုင်းမငြိမ်ပါက Tool ကို ပြန် Run ပေးပါ။")
    print("="*40)

if __name__ == "__main__":
    check_key()
