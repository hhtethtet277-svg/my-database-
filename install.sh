#!/bin/bash

# Folder အဟောင်းများ ရှင်းလင်းခြင်း
cd $HOME
rm -rf m
rm -rf my-database-

echo "-----------------------------------------------"
echo "      INSTALLING RUIJIE BYPASS PRO             "
echo "-----------------------------------------------"

# လိုအပ်သော ပတ်ဝန်းကျင်များ ပြင်ဆင်ခြင်း
pkg update -y
pkg install python git curl -y
pip install requests colorama urllib3

# GitHub မှ အသစ်ပြန်ဒေါင်းခြင်း
git clone https://github.com/hhtethtet277-svg/my-database-

# Run ရန် ညွှန်ကြားချက်
cd my-database-
echo "[✓] Setup Finished! Starting tool..."
python yoon.py
