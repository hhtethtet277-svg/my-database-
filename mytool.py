import requests
import sys

# အစ်ကို့ရဲ့ GitHub Key Link
DB_URL = "https://raw.githubusercontent.com/hhtethtet277-svg/my-database-/refs/heads/main/key.txt"

def verify_license():
    print("\n\033[96m╔══════════════════════════════════════╗\033[0m")
    print("\033[96m║        MY PREMIUM CUSTOM TOOL        ║\033[0m")
    print("\033[96m╚══════════════════════════════════════╝\033[0m")
    
    user_key = input("\033[93m[?]\033[0m Enter Your License Key: ").strip()

    try:
        response = requests.get(DB_URL, timeout=10)
        if response.status_code != 200:
            print("\033[91m[!] Database Error!\033[0m")
            return False
            
        key_list = response.text.splitlines()
        for entry in key_list:
            if "|" in entry:
                data = entry.split("|")
                if len(data) >= 2:
                    if user_key == data[1]:
                        print("\n\033[92m[✓] Access Granted!\033[0m")
                        return True
        
        print("\n\033[91m[X] Invalid License Key!\033[0m")
        return False
    except Exception as e:
        print("\n\033[91m[!] Connection Error!\033[0m")
        return False

if __name__ == "__main__":
    if verify_license():
        print("\n\033[95m[*] Tool Starting... Welcome, Moe Yu!\033[0m")
        # အစ်ကိုလုပ်ချင်တဲ့ function တွေကို ဒီအောက်မှာ ထပ်တိုးနိုင်ပါတယ်
    else:
        sys.exit()
