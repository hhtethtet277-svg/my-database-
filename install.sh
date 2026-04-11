#!/bin/bash

# ၁။ Folder အဟောင်းတွေရှိရင် အကုန်ရှင်းမယ်
cd $HOME
rm -rf m
rm -rf my-database-

echo "==========================================="
echo "   🚀 INSTALLING MY RUIJIE BYPASS PRO      "
echo "        BY: HH TET TET                     "
echo "==========================================="

# ၂။ လိုအပ်တဲ့ ပစ္စည်းတွေ သွင်းမယ်
echo "[*] Updating packages..."
pkg update -y && pkg upgrade -y
pkg install python git curl -y

# ၃။ Python library များ သွင်းမယ်
echo "[*] Installing required python libraries..."
pip install requests colorama urllib3

# ၄။ GitHub ကနေ နာမည်အသစ်နဲ့ ပြန်ဒေါင်းမယ်
echo "[*] Downloading tool from GitHub..."
# သင့်ရဲ့ Username (htethtet277-svg) နဲ့ Repo (my-database-) ကို ပြင်ထားပါတယ်
git clone https://github.com/htethtet277-svg/my-database-

# ၅။ Folder ထဲကို ဝင်မယ်
cd my-database-

# ၆။ yoon.py ကို စစ်ပြီး Run မယ်
if [ -f "yoon.py" ]; then
    echo "[✓] Installation Complete!"
    echo "[*] Launching yoon.py..."
    sleep 2
    python yoon.py
else
    echo "❌ Error: yoon.py မတွေ့ပါ။ GitHub မှာ ဖိုင်နာမည် မှန်မမှန် ပြန်စစ်ပါ။"
fi
