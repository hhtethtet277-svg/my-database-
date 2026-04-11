#!/bin/bash

# ၁။ အရင်ရှိနေတဲ့ folder အဟောင်းကို ဖျက်မယ်
cd $HOME
rm -rf my-database-

echo "==========================================="
echo "   🚀 INSTALLING MY RUIJIE BYPASS PRO      "
echo "        BY: HH TET TET                     "
echo "==========================================="

# ၂။ လိုအပ်တဲ့ Python နဲ့ Git ကို သွင်းမယ်
echo "[*] Updating packages..."
pkg update -y && pkg upgrade -y
pkg install python git curl -y

# ၃။ Python library များ သွင်းမယ်
echo "[*] Installing required python libraries..."
pip install requests colorama urllib3

# ၄။ GitHub ကနေ ကိုယ်ပိုင် Tool ကို ဒေါင်းမယ်
echo "[*] Downloading tool from GitHub..."
git clone https://github.com/hhtethtet277-svg/my-database-

# ၅။ Folder ထဲကို ဝင်မယ်
cd my-database-

# ၆။ yoon.py ရှိမရှိ စစ်ပြီး Run မယ်
if [ -f "yoon.py" ]; then
    echo "[✓] Installation Complete!"
    echo "[*] Launching yoon.py..."
    sleep 2
    python yoon.py
else
    echo "❌ Error: yoon.py မတွေ့ပါ။ GitHub မှာ ဖိုင်နာမည် မှန်မမှန် ပြန်စစ်ပါ။"
fi
