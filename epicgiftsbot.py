# -*- coding: utf-8 -*-
import requests
from licensing.methods import Helpers
import sys
# GitHub repository URL
url = "https://raw.githubusercontent.com/Enshteyn40/crdevice/refs/heads/main/epicgifts.csv"

# URL'dan CSV faylni yuklab olish
response = requests.get(url)

# Ma'lumotlarni qatorlarga ajratish
lines = response.text.splitlines()

# Olingan qatorlarni tozalash
hash_values_list = [line.strip() for line in lines]

def GetMachineCode():
    machine_code = Helpers.GetMachineCode(v=2)
    return machine_code
def color(text, color_code):
        return f"\033[{color_code}m{text}\033[0m"

machine_code = GetMachineCode()

print(machine_code)

# Mashina kodini tekshirish
if machine_code in hash_values_list:
    import json
    from telethon.tl.functions.channels import JoinChannelRequest
    import csv
    import fake_useragent
    from telethon import types, utils, errors
    import time
    from urllib.parse import unquote
    from telethon.sync import TelegramClient
    from telethon.tl.functions.account import UpdateStatusRequest
    from telethon.tl.types import InputUser
    from telethon.tl.functions.messages import RequestAppWebViewRequest
    from telethon.tl.types import InputBotAppShortName
    import requests
    from termcolor import colored
    import os
    print(color("Oxirgi kod yanilangan vaqti 30.06.2025 6:10 PM", "95"))  # magenta
    def ensure_path_and_file(path, filename):
        if not os.path.exists(path):
            print(f"{path} papkasi mavjud emas. Yaratilmoqda...")
            os.makedirs(path)

        filepath = os.path.join(path, filename)
        if not os.path.isfile(filepath):
            print(f"{filename} fayli topilmadi. csv fayl yaratildi.")
            print("Endi gividlarni yozib chiqing")
            with open(filepath, 'w', encoding='utf-8') as f:
                pass
            sys.exit()
        else:
            print(f"{filename} fayli allaqachon mavjud: {filepath}")
        return filepath

    if os.path.exists('/storage/emulated/0/giv'):
        print("Telefon uchun  aniqlandi.")
        mrkt_file = ensure_path_and_file('/storage/emulated/0/giv', 'epicgiftlar.csv')
        giv_ids_ozim = [row[0] for row in csv.reader(open(mrkt_file, 'r', encoding='utf-8')) if row]
    elif os.path.exists('C:\\join'):
        print("Kompyuter uchun  aniqlandi.")
        mrkt_file = ensure_path_and_file('C:\\join', 'epicgiftlar.csv')
        giv_ids_ozim = [row[0] for row in csv.reader(open(mrkt_file, 'r', encoding='utf-8')) if row]
    else:
        print("Hech qanday mos papka topilmadi")

    phonecsv = "ozim"
    with open(f'{phonecsv}.csv', 'r') as f:
        phlist = [row[0] for row in csv.reader(f)]
    print(color('Spam bolmagan raqamlar: ' + str(len(phlist)), "94"))  # ko‘k
    qowiwjm = 0
    qowiwjm2 = len(phlist) 
    indexx = 0
    for deltaxd in phlist[qowiwjm:qowiwjm2]:
        try:
            indexx += 1
            phone = deltaxd
            print(color(f"Login {phone}", "92"))  # yashil
            phone = utils.parse_phone(deltaxd)
            api_id = 22962676
            api_hash = '543e9a4d695fe8c6aa4075c9525f7c57'
            client = TelegramClient(f"sessions/{phone}", api_id, api_hash) 
            client.start(phone)
            client(UpdateStatusRequest(offline=False))
            print(color(f'Index : {indexx}', "96"))  # cyan
            import aiohttp
            # ...
            async def main():
                async with aiohttp.ClientSession() as session:
                    for giveaway_code in giv_ids_ozim:
                        bot_entity = await client.get_entity("@epic_gift_bot")
                        bot = InputUser(user_id=bot_entity.id, access_hash=bot_entity.access_hash)
                        bot_app = InputBotAppShortName(bot_id=bot, short_name="app")
                        web_view = await client(
                            RequestAppWebViewRequest(
                                peer=bot,
                                app=bot_app,
                                platform="desktop",
                                write_allowed=True,
                                start_param=f"giveaway_{giveaway_code}"
                            )
                        )
                        auth_url = web_view.url.replace('tgWebAppVersion=7.0', 'tgWebAppVersion=8.0')
                        init_data = unquote(auth_url.split('tgWebAppData=', 1)[1].split('&tgWebAppVersion', 1)[0])

                        headers = {
                            'accept': 'application/json, text/plain, */*',
                            'accept-language': 'en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
                            'authorization': f'tma {init_data}',
                            'cache-control': 'no-cache',
                            'origin': 'https://epicgift.app',
                            'pragma': 'no-cache',
                            'priority': 'u=1, i',
                            'referer': 'https://epicgift.app/',
                            'sec-ch-ua': '"Microsoft Edge WebView2";v="137", "Microsoft Edge";v="137", "Not/A)Brand";v="24", "Chromium";v="137"',
                            'sec-ch-ua-mobile': '?0',
                            'sec-ch-ua-platform': '"Android"',
                            'sec-fetch-dest': 'empty',
                            'sec-fetch-mode': 'cors',
                            'sec-fetch-site': 'same-site',
                            'user-agent': fake_useragent.UserAgent(platforms=["mobile"], os=["Android"], browsers=["Chrome Mobile"]).random,
                            'x-client-info': '{"platform":"android","platformVersion":"9.0","appVersion":"1.0","deviceType":"mobile","startParam":"giveaway_%s"}' % giveaway_code,
                        }
                        # Giveaway info request 
                        async with session.get(f"https://api.epicgift.app/giveaway/{giveaway_code}", headers=headers, timeout=10) as response:
                            data = await response.json()
                            
                            if data.get("joined", False):
                                print("✅ Giveawayda allaqachon qatnashgan ekan — keyingisiga o‘tamiz.")
                                continue  # bu joyda keyingi giveaway_code'ga o'tadi
                            else:
                                prizes = data.get("giveaway", {}).get("prizes", [])
                                num_prizes = len(prizes)
                                participants = data.get("participants", 0)
                                requirements = data.get("giveaway", {}).get("requirements", [])
                                premium_channels = [
                                    req["payload"]["channel"]
                                    for req in requirements
                                    if req.get("type") == "join_channel"
                                ]

                                total_value = 0
                                from collections import defaultdict
                                print("\n🎁 Sovg'alar qiymatlari:")

                                # Har bir sovg'a nomi uchun [soni, umumiy qiymat] ni saqlash
                                prize_summary = defaultdict(lambda: [0, 0])

                                for prize in prizes:
                                    title = prize.get("title", "No Title")
                                    floor_price = prize.get("floorPriceTon", 0)
                                    prize_summary[title][0] += 1
                                    prize_summary[title][1] += floor_price
                                    total_value += floor_price

                                # Natijalarni chiroyli chiqarish
                                for title, (count, total_price) in prize_summary.items():
                                    item_str = f"{count}x " if count > 1 else ""
                                    print(f"- {item_str}{title}: {round(total_price, 2)} TON")

                                print("\n📦 Sovg'alar soni:", num_prizes)
                                print("👥 Qatnashchilar soni:", participants)
                                print("🔗 Kanalga qo‘shilish talablari:")
                                for ch in premium_channels:
                                    print("-", ch)
                                print(f"\n💰 Giveaway jamg‘armasi: {round(total_value, 2)} TON")
                                
                                print(colored(f"🔗 Topilgan kanallar: {len(premium_channels)}", "cyan"))
                                for ochiq_link in premium_channels:
                                    try:
                                        await client(JoinChannelRequest(ochiq_link))
                                        print(colored(f"Kanalga a'zo bo'ldi {ochiq_link}", "green"))
                                    except Exception as e:
                                        print(colored(f"Kanalga qo'shilishda xatolik {ochiq_link}: {e}", "red"))


                            # User info request
                            async with session.get("https://api.epicgift.app/user", headers=headers, timeout=10) as response:
                                if response.status == 200:
                                    try:
                                        response_data = await response.json()
                                        username = response_data["user"]["username"]
                                        balance = response_data["user"]["balance"]
                                        ref = response_data["user"]["ref"]
                                        print("👤 Username:", username)
                                        print("💰 Balance:", balance)
                                        print("🔗 Referral:", ref)
                                    except Exception as e:
                                        print(color("⚠️ JSON o‘qishda xatolik: " + str(e), "91"))
                                        print(color("Response text: " + await response.text(), "93"))
                                else:
                                    print(color(f"❌ HTTP kod {response.status}, xatolik bo‘ldi", "91"))
                                    print(color("Javob matni:", "93"))
                                    print(await response.text())
                            async with session.post("https://api.epicgift.app/giveaway/1/join", headers=headers, timeout=10) as response:
                                if response.status == 200:
                                    response_data = await response.json()
                                    if response_data.get("message") == "Joined giveaway":
                                        print("✅ Giveawayda muvaffaqiyatli qatnashdi")
                                    else:
                                        print("📩 Server javobi:", response.get("message"))
                                else:
                                    print("")
            with client:
                client.loop.run_until_complete(main())
        except Exception as e:
            print(color("Error:", "91"), color(str(e), "91"))  # qizil
            continue
else:
    print(color("Kodni aktivlashtirish uchun @Enshteyn40  ga murojat qiling", "95"))  # magenta
