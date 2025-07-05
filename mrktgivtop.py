# -*- coding: utf-8 -*-
import requests
from licensing.methods import Helpers

# GitHub repository URL
url = "https://raw.githubusercontent.com/Enshteyn40/crdevice/refs/heads/main/mrkt.csv"

# URL'dan CSV faylni yuklab olish
response = requests.get(url)
lines = response.text.splitlines()
hash_values_list = [line.strip() for line in lines]

def GetMachineCode():
    return Helpers.GetMachineCode(v=2)

def color(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

machine_code = GetMachineCode()
print(machine_code)

if machine_code in hash_values_list:
    import json
    from telethon.tl.functions.channels import JoinChannelRequest
    import csv
    from telethon import types, utils, errors
    from datetime import datetime, timedelta, timezone
    from urllib.parse import unquote
    from telethon.sync import TelegramClient
    from telethon.tl.functions.account import UpdateStatusRequest
    from telethon.tl.types import InputUser
    from telethon.tl.functions.messages import RequestAppWebViewRequest
    from telethon.tl.types import InputBotAppShortName
    import time

    print(color("Oxirgi kod yangilangan vaqti 07.06.2025 9:10 PM", "95"))
    print(color("Ozim.csv yaratilib faqat 1 ta raqam yozilad", "95"))
    free_only_input = input("Faqat tekin giftlarni topaymi? (ha/yoq): ").strip().lower()
    premium_input = input("Premium uchun giftlarni topaymi? (ha/yoq): ").strip().lower()
    boost_input = input("Channel boost kerakmi? (ha/yoq): ").strip().lower()
    trader_input = input("Active traders uchun giftlarni topaymi? (ha/yoq): ").strip().lower()
    sont = int(input("Nechta giveaway qidirsin: "))
    phonecsv = "ozim"
    
    with open(f'{phonecsv}.csv', 'r') as f:
        phlist = [row[0] for row in csv.reader(f)]

    print(color('Spam bo‘lmagan raqamlar: ' + str(len(phlist)), "94"))
    indexx = 0

    for deltaxd in phlist:
        try:
            indexx += 1
            phone = deltaxd
            print(color(f"Login: {phone}", "92"))
            phone = utils.parse_phone(deltaxd)
            api_id = 22962676
            api_hash = '543e9a4d695fe8c6aa4075c9525f7c57'
            client = TelegramClient(f"sessions/{phone}", api_id, api_hash)

            async def main():
                await client.start(phone)
                await client(UpdateStatusRequest(offline=False))
                bot_entity = await client.get_entity("@main_mrkt_bot")
                bot = InputUser(user_id=bot_entity.id, access_hash=bot_entity.access_hash)
                bot_app = InputBotAppShortName(bot_id=bot, short_name="app")
                web_view = await client(
                    RequestAppWebViewRequest(
                        peer=bot,
                        app=bot_app,
                        platform="android",
                        write_allowed=True,
                        start_param="1062643042"
                    )
                )
                auth_url = web_view.url.replace('tgWebAppVersion=7.0', 'tgWebAppVersion=8.0')
                init_data = unquote(auth_url.split('tgWebAppData=', 1)[1].split('&tgWebAppVersion', 1)[0])
                user_json_str = unquote(init_data).split("user=", 1)[1].split("&", 1)[0]
                user_data = json.loads(user_json_str)
                photo_url = user_data.get("photo_url")

                headers = {
                    "accept": "*/*",
                    "content-type": "application/json",
                    "origin": "https://cdn.tgmrkt.io",
                    "referer": "https://cdn.tgmrkt.io/",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
                }

                jsondata = {
                    "appId": 1062643042,
                    "data": init_data,
                    "photo": photo_url
                }

                response = requests.post("https://api.tgmrkt.io/api/v1/auth", json=jsondata, headers=headers, timeout=10)
                token = response.json().get("token")

                headers["authorization"] = token
                base_url = "https://api.tgmrkt.io/api/v1/giveaways"
                all_items = []
                cursor = ""

                while len(all_items) < sont:
                    params = {
                        "type": "Free",
                        "count": 20,
                        "cursor": cursor
                    }

                    response = requests.get(base_url, headers=headers, params=params)
                    if response.status_code != 200:
                        print(f"❌ Xatolik: {response.status_code}")
                        break

                    data = response.json()
                    items = data.get("items", [])

                    all_items = []
                    # JSON dan ma’lumot olish
                    data = response.json()
                    items = data.get("items", [])

                    for item in items:
                        is_premium = item.get("isForPremium", False)
                        is_boost = item.get("isChanelBoostRequired", False)
                        is_trader = item.get("isForActiveTraders", False)

                        # agar tekin (3 ta ham False) kerak bo‘lsa, shuni tekshir
                        if free_only_input == "ha":
                            if not is_premium and not is_boost and not is_trader:
                                all_items.append(item)
                            continue  # shu itemni tekshirib bo‘ldi, boshqa shartlar kerak emas

                        # agar tekin kerak emas bo‘lsa, qolgan 3 shartni tekshir
                        if (
                            (premium_input == "ha" and is_premium) or (premium_input == "yoq" and not is_premium)
                        ) and (
                            (boost_input == "ha" and is_boost) or (boost_input == "yoq" and not is_boost)
                        ) and (
                            (trader_input == "ha" and is_trader) or (trader_input == "yoq" and not is_trader)
                        ):
                            all_items.append(item)

                    print(f"🔄 {len(all_items)} ta mos keluvchi gift yig‘ildi...")

                    cursor = data.get("nextCursor", "")
                    if not cursor:
                        print("✅ Barcha sahifalar tugadi.")
                        break


                    time.sleep(0.3)

                all_items.sort(key=lambda x: x.get("endAt", ""))

                with open("mrktgivlartopilgani.csv", "w", encoding="utf-8") as fout:
                    print(f"\n🎯 Topilgan jami mos giftlar: {len(all_items)} ta\n")

                    for i, item in enumerate(all_items, start=1):
                        gift = item.get("previewGift", {})
                        title = gift.get("title", "Noma'lum")
                        model = gift.get("modelName", "Noma'lum")
                        giveawayid = item.get("id", "Noma'lum")
                        participants = item.get("participantsCount", 0)
                        channels = item.get("chanels", [])
                        channels_str = ", ".join(channels) if channels else "Yo'q"
                        end_at = item.get("endAt", "")

                        try:
                            end_time = datetime.strptime(end_at, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
                            now = datetime.now(timezone.utc)
                            remaining_minutes = int((end_time - now).total_seconds() / 60)
                            time_left = f"⏳ {remaining_minutes} daqiqa qoldi" if remaining_minutes > 0 else "❌ Tugagan"
                            end_time_str = end_time.strftime("%Y-%m-%d %H:%M:%S")
                        except:
                            end_time_str = end_at
                            time_left = "⛔ Noma'lum vaqt"

                        print(f"{i}. 🎁 Gift: {title} ({model})")
                        print(f"   🆔 Giveaway id: {giveawayid}")
                        print(f"   👥 Ishtirokchilar: {participants}")
                        print(f"   🕒 Tugash vaqti: {end_time_str}")
                        print(f"   ⏰ Qolgan vaqt: {time_left}")
                        print(f"   📡 Kanallar: {channels_str}")
                        print("-" * 50)

                        fout.write(f"{i}. 🎁 Gift: {title} ({model})\n")
                        fout.write(f"   🆔 Giveaway id: {giveawayid}\n")
                        fout.write(f"   👥 Ishtirokchilar: {participants}\n")
                        fout.write(f"   🕒 Tugash vaqti: {end_time_str}\n")
                        fout.write(f"   ⏰ Qolgan vaqt: {time_left}\n")
                        fout.write(f"   📡 Kanallar: {channels_str}\n")
                        fout.write("-" * 50 + "\n")

            with client:
                client.loop.run_until_complete(main())

        except Exception as e:
            print(color("Error:", "91"), color(str(e), "91"))
            continue
else:
    print(color("Kodni aktivlashtirish uchun @Enshteyn40 ga murojat qiling", "95"))
