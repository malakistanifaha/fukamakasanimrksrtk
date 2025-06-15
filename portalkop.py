# -*- coding: utf-8 -*-
import requests
from licensing.methods import Helpers
import sys
import os
import csv
import json
from telethon.tl.functions.channels import JoinChannelRequest
from telethon import types, utils, errors
import time
from urllib.parse import unquote
from telethon.sync import TelegramClient
from telethon.tl.functions.account import UpdateStatusRequest
from telethon.tl.types import InputUser
from telethon.tl.functions.messages import RequestAppWebViewRequest
from telethon.tl.types import InputBotAppShortName
from datetime import datetime, timezone, timedelta

def color(text, color_code):
    color_map = {
        "red": "91",
        "green": "92",
        "yellow": "93",
        "blue": "94",
        "magenta": "95",
        "cyan": "96",
        "white": "97",
        "bold_white": "1;97"
    }
    code = color_map.get(color_code, "97")
    return f"\033[{code}m{text}\033[0m"

url = "https://raw.githubusercontent.com/Enshteyn40/crdevice/refs/heads/main/portal.csv"
response = requests.get(url)
lines = response.text.splitlines()
hash_values_list = [line.strip() for line in lines]

def GetMachineCode():
    return Helpers.GetMachineCode(v=2)

machine_code = GetMachineCode()
print(color(machine_code, "white"))

if machine_code in hash_values_list:
    print(color("Oxirgi kod yanilangan vaqti 14.06.2025 04:09 PM", "magenta"))

    def ensure_path_and_file(path, filename):
        if not os.path.exists(path):
            print(color(f"{path} papkasi mavjud emas. Yaratilmoqda...", "yellow"))
            os.makedirs(path)
        filepath = os.path.join(path, filename)
        if not os.path.isfile(filepath):
            print(color(f"{filename} fayli topilmadi. csv fayl yaratildi.", "red"))
            with open(filepath, 'w', encoding='utf-8') as f:
                pass
            sys.exit()
        else:
            print(color(f"{filename} fayli allaqachon mavjud: {filepath}", "green"))
        return filepath

    if os.path.exists('/storage/emulated/0/giv'):
        print(color("Telefon uchun aniqlandi.", "cyan"))
        mrkt_file = ensure_path_and_file('/storage/emulated/0/giv', 'giftawey.csv')
    elif os.path.exists('C:\\join'):
        print(color("Kompyuter uchun aniqlandi.", "cyan"))
        mrkt_file = ensure_path_and_file('C:\\join', 'giftawey.csv')
    else:
        print(color("Hech qanday mos papka topilmadi", "red"))
        sys.exit()

    with open(mrkt_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        giv_ids_ozim = [row for row in reader if row]
        
    file_path_1 = r"C:\join\proxyglob.csv"
    file_path_2 = r"/storage/emulated/0/giv/proxyglob.csv"

    if os.path.exists(file_path_1):
        with open(file_path_1, 'r') as f:
            reader = csv.reader(f)
            ROTATED_PROXY = next(reader)[0]
    elif os.path.exists(file_path_2):
        with open(file_path_2, 'r') as f:
            reader = csv.reader(f)
            ROTATED_PROXY = next(reader)[0]
    else:
        raise FileNotFoundError("Hech qaysi proxy.csv fayli topilmadi.")

    proxies = {
        "http": ROTATED_PROXY,
        "https": ROTATED_PROXY
    }

    phonecsv = "phone"
    with open(f'{phonecsv}.csv', 'r') as f:
        phlist = [row[0] for row in csv.reader(f)]
    print(color(f'Spam bo\'lmagan raqamlar: {len(phlist)}', "yellow"))

    inviter_id_by_giveaway = {}

    for indexx, deltaxd in enumerate(phlist):
        try:
            print(color(f"Login {deltaxd}", "green"))
            phone = utils.parse_phone(deltaxd)
            api_id = 22962676
            api_hash = '543e9a4d695fe8c6aa4075c9525f7c57'
            client = TelegramClient(f"sessions/{phone}", api_id, api_hash)
            client.start(phone)
            client(UpdateStatusRequest(offline=False))
            me = client.get_me()
            
            print(color(f'Index: {indexx + 1}', "blue"))

            async def main():
                for giv_index, (giveaway_code, group_size_str) in enumerate(giv_ids_ozim):
                    group_size = int(group_size_str)
                    acc_idx = indexx + 1

                    if acc_idx % group_size == 0:
                        current_inviter_id = inviter_id_by_giveaway.get(giv_index, "")
                    else:
                        current_inviter_id = ""

                    bot_entity = await client.get_entity("@giftsgiveawaybot")
                    bot = InputUser(user_id=bot_entity.id, access_hash=bot_entity.access_hash)
                    bot_app = InputBotAppShortName(bot_id=bot, short_name="start")
                    web_view = await client(RequestAppWebViewRequest(
                        peer=bot,
                        app=bot_app,
                        platform="android",
                        write_allowed=True,
                        start_param=giveaway_code
                    ))
                    auth_url = web_view.url.replace('tgWebAppVersion=7.0', 'tgWebAppVersion=8.0')
                    init_data = unquote(auth_url.split('tgWebAppData=', 1)[1].split('&tgWebAppVersion', 1)[0])

                    headers = {
                        "Content-Type": "application/json",
                        "Origin": "https://giftaway.org",
                        "Referer": "https://giftaway.org/",
                        "User-Agent": "Mozilla/5.0"
                    }
                    jsondata = {
                        "init_data": init_data,
                        "inviter_id": current_inviter_id
                    }
                    response = requests.post(url="https://api.giftaway.org/api/auth", json=jsondata, proxies=proxies, headers=headers, timeout=10)
                    jwt_token = response.json()["result"]["jwt"]

                    headers["Authorization"] = f"Bearer {jwt_token}"
                    response = requests.get(url=f"https://api.giftaway.org/api/giveaway/{giveaway_code}", headers=headers, proxies=proxies, timeout=10)
                    result = response.json()["result"]

                    if result.get("is_completed", False):
                        print(color("✅ Allaqachon ushbu giveawayda qatnashgan", "green"))
                        dt = datetime.fromisoformat(result["ending_at"]).astimezone(timezone(timedelta(hours=5)))
                        print(color("⏳ Tugash vaqti:", "blue"), dt.strftime("%d.%m.%Y %H:%M"))
                        print(color("🎟 Tiketlar soni:", "magenta"), result["my_tickets"])
                        print(color("🎁 Sovg'alar nomlari:", "yellow"))
                        for gift in result["gifts"]:
                            print("-", gift["name"])
                        print(color("➡️ Keyingi giveawayga yoki raqamga o'tamiz", "bold_white"))
                    else:
                        print(color("❌ Giveawayda hali qatnashmagan", "red"))
                        print(color("📌 Ishtirokchilar soni:", "cyan"), result["participants"])
                        print(color("📋 Vazifalar:", "blue"))
                        premium_channels = [task["value"] for task in result["tasks"] if task["value"]]
                        for ch in premium_channels:
                            print("-", ch)
                            try:
                                await client(JoinChannelRequest(ch))
                                print(color(f"Kanalga a'zo bo'ldi {ch}", "green"))
                            except Exception as e:
                                print(color(f"Kanalga qo'shilishda xatolik {ch}: {e}", "red"))
                        time.sleep(2)
                        for ch in premium_channels:
                            print("-", ch)
                            try:
                                await client(JoinChannelRequest(ch))
                                print(color(f"Kanalga a'zo bo'ldi {ch}", "green"))
                            except Exception as e:
                                print(color(f"Kanalga qo'shilishda xatolik {ch}: {e}", "red"))
                        response = requests.post(url=f"https://api.giftaway.org/api/giveaway/{giveaway_code}/complete", headers=headers, proxies=proxies, timeout=10)
                        if response.status_code == 200:
                            completion = response.json()
                            if completion.get("result", {}).get("completed", False):
                                print(color("✅ Giveawayga qatnashdi", "green"))
                            else:
                                print(color("❌ Giveawayga qatnasha olmadi", "red"))
                        else:
                            print(color(f"❌ So‘rov xatolik bilan tugadi: {response.status_code}", "red"))

                    if (acc_idx) % group_size == 0:
                        inviter_id_by_giveaway[giv_index] = me.id
                        print(color(f"🆕 Ushbu giveaway uchun yangi ref ID olindi: {me.id} (CSVdagi {giv_index + 1}-qatordagi giveaway)", "cyan"))

            with client:
                client.loop.run_until_complete(main())
        except Exception as e:
            print(color("Error:", "red"), color(str(e), "red"))
            continue
else:
    print(color("Kodni aktivlashtirish uchun @Enshteyn40 ga murojat qiling", "magenta"))
