#!/bin/bash

# ၁။ ပင်မနေရာကို အရင်သွားပြီး အဟောင်းရှိရင် ရှင်းမယ်
cd $HOME
rm -rf my-database-

echo "🚀 Installing Aladdin Ruijie Bypass..."

# ၂။ လိုအပ်တဲ့ Python ပစ္စည်းတွေ သွင်းမယ်
pkg update && pkg upgrade -y
pkg install python git -y
pip install requests colorama urllib3

# ၃။ GitHub ကနေ သင့်ရဲ့ ကိုယ်ပိုင် Tool ကို ဒေါင်းမယ်
# သင့်ရဲ့ Repository Link ကို ပြောင်းပေးထားပါတယ်
git clone https://github.com/hhtethtet277-svg/my-database-

# ၄။ Folder ထဲကို ဝင်မယ်
cd my-database-

# ၅။ yoon.py ကို စတင် Run မယ်
# သင့်ဖိုင်နာမည်က yoon.py ဖြစ်လို့ အဲဒါကိုပဲ run ခိုင်းထားပါတယ်
if [ -f "yoon.py" ]; then
    python yoon.py
else
    echo "❌ Error: yoon.py missing! Please check your file name on GitHub."
fi
