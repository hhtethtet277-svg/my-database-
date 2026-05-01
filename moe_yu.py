import os
import sys
import time
import subprocess

# ၁။ လိုအပ်သောဖိုင်များ ဒေါင်းလုဒ်ဆွဲခြင်း
def setup_files():
    files = {
        "ruijiedemo.so": "https://raw.githubusercontent.com/Haruto000x/STARLINK-ROUTER/main/ruijiedemo.cpython-313-aarch64-linux-android.so",
        "run": "https://raw.githubusercontent.com/Haruto000x/STARLINK-ROUTER/main/run"
    }
    
    for filename, url in files.items():
        if not os.path.exists(filename):
            print(f"[*] {filename} ကို ရှာမတွေ့ပါ... ဒေါင်းလုဒ်ဆွဲနေသည်...")
            try:
                subprocess.run(["curl", "-L", "-o", filename, url], check=True, capture_output=True)
                print(f"[+] {filename} ရယူပြီးပါပြီ။")
                if filename == "run":
                    os.chmod(filename, 0o755)
            except Exception as e:
                print(f"[!] ဒေါင်းလုဒ်ဆွဲခြင်း မအောင်မြင်ပါ: {e}")

# ၂။ Key စစ်ဆေးခြင်း Logic
def verify_key():
    key_file = "key.txt"
    if not os.path.exists(key_file):
        with open(key_file, "w") as f:
            f.write("FREE-KEY-123") # Default key တစ်ခု ထည့်ပေးထားမယ်
        print("[!] key.txt အသစ်ဆောက်ပေးထားပါသည်။ ကျေးဇူးပြု၍ Key ထည့်ပါ။")
        return False

    with open(key_file, "r") as f:
        stored_key = f.read().strip()
    
    if len(stored_key) < 5: # Key က အနည်းဆုံး ၅ လုံးရှိရမယ်လို့ သတ်မှတ်ခြင်း
        print("[!] Key မမှန်ကန်ပါ။ (key.txt ကို စစ်ဆေးပါ)")
        return False
    
    print(f"[✔] Key အတည်ပြုပြီးပါပြီ: {stored_key}")
    return True

# ၃။ Tool ကို စတင်ခြင်း
def launch_tool():
    print("\n[+] Starlink Router Tool ကို စတင်နေပါပြီ...")
    time.sleep(1.5)
    
    try:
        # .so ဖိုင်ကို import လုပ်ခြင်း
        import ruijiedemo
        
        # *** အရေးကြီးဆုံးနေရာ ***
        # ruijiedemo ထဲမှာပါတဲ့ run ဖို့ function ကို ဒီမှာ ခေါ်ရပါမယ်
        # သင့်ရဲ့ .so ဖိုင်ထဲက function နာမည်ကို သိရင် အောက်က line မှာ ပြင်လိုက်ပါ
        if hasattr(ruijiedemo, 'main'):
            ruijiedemo.main()
        elif hasattr(ruijiedemo, 'start'):
            ruijiedemo.start()
        else:
            # function နာမည် တန်းသိရင် ဒီလို ခေါ်ပါ
            # ruijiedemo.အခုဒီမှာနာမည်ရေး()
            print("[!] .so ဖိုင်ထဲက Main Function ကို ရှာမတွေ့ပါ။")
            
    except ImportError:
        print("[!] Error: Python 3.13 aarch64 (Android) မဟုတ်လို့ run လို့မရပါ။")
    except Exception as e:
        print(f"[!] တစ်စုံတစ်ရာ မှားယွင်းနေပါသည်: {e}")

# ၄။ ပင်မ လုပ်ဆောင်ချက်
def main():
    while True: # ပရိုဂရမ် တန်းမပိတ်သွားအောင် loop ပတ်ထားမယ်
        os.system("clear")
        print("="*45)
        print("      STARLINK ROUTER AUTO SYSTEM (2026)      ")
        print("="*45)
        
        setup_files()
        
        if verify_key():
            launch_tool()
            break # အောင်မြင်ရင် loop က ထွက်မယ်
        else:
            print("\n[၁] နောက်တစ်ကြိမ် ကြိုးစားမည်")
            print("[၂] ထွက်မည်")
            choice = input("\nရွေးချယ်ရန်: ")
            if choice != '1':
                sys.exit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] ပိတ်လိုက်ပါပြီ။")
        sys.exit()
