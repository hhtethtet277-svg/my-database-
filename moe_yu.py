import os
import sys
import time
import subprocess

# --- ၁။ လိုအပ်သော Library နှင့် File များ စစ်ဆေးခြင်း ---
def setup_everything():
    # ping3 library ရှိမရှိစစ်မယ်၊ မရှိရင် သွင်းမယ်
    try:
        import ping3
    except ImportError:
        print("[*] Installing required library: ping3...")
        subprocess.run([sys.executable, "-m", "pip", "install", "ping3"], check=True)

    # လိုအပ်တဲ့ binary ဖိုင်တွေ ဒေါင်းမယ်
    files = {
        "ruijiedemo.so": "https://raw.githubusercontent.com/Haruto000x/STARLINK-ROUTER/main/ruijiedemo.cpython-313-aarch64-linux-android.so",
        "run": "https://raw.githubusercontent.com/Haruto000x/STARLINK-ROUTER/main/run"
    }
    for filename, url in files.items():
        if not os.path.exists(filename):
            print(f"[*] {filename} ကို ဒေါင်းလုဒ်ဆွဲနေသည်...")
            subprocess.run(["curl", "-L", "-o", filename, url], check=True)
            if filename == "run":
                os.chmod(filename, 0o755)

# --- ၂။ Tool ကို စတင် Run ခြင်း ---
def launch_tool():
    print("\n[+] Starlink Router Tool ကို စတင်နေပါပြီ...")
    time.sleep(1)
    try:
        import ruijiedemo
        print("[✔] Module loaded successfully!")
        
        # dir(ruijiedemo) အရ အထဲမှာပါတဲ့ main function ကို ခေါ်မယ်
        # များသောအားဖြင့် Compiled file တွေမှာ 'main' function ပါလေ့ရှိတယ်
        if hasattr(ruijiedemo, 'main'):
            ruijiedemo.main()
        elif hasattr(ruijiedemo, 'MoeYu'):
            ruijiedemo.MoeYu()
        else:
            print("[!] အောင်မြင်စွာ Load လုပ်ပြီးပါပြီ။")
            print(f"Functions available: {dir(ruijiedemo)}")
            
    except Exception as e:
        print(f"\n[!] Error ဖြစ်ပွားမှု: {e}")

# --- ၃။ ပင်မ လုပ်ဆောင်ချက် ---
def main():
    os.system("clear")
    print("="*45)
    print("      STARLINK ROUTER AUTO SYSTEM (2026)      ")
    print("="*45)
    
    setup_everything()
    
    # Key ရှိမရှိ စစ်ဆေးခြင်း
    if os.path.exists("key.txt"):
        launch_tool()
    else:
        print("[!] key.txt မရှိသေးပါ။ Key အရင်ထည့်ပါ။")

if __name__ == "__main__":
    main()
