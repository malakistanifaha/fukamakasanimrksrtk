import sys
import os
import csv
import time
import json
from licensing.methods import Helpers
import base64
from urllib.parse import unquote, parse_qs
from telethon.sync import TelegramClient
from telethon import utils
from telethon.tl.functions.account import UpdateStatusRequest
from telethon.tl.types import InputUser
from telethon.tl.functions.messages import RequestAppWebViewRequest
from telethon.tl.types import InputBotAppShortName
import requests
from telethon.tl.functions.channels import JoinChannelRequest
from datetime import datetime, timezone, timedelta
import pytz

# 🔐 Aktivatsiya
url = "https://raw.githubusercontent.com/Enshteyn40/crdevice/refs/heads/main/primegifts.csv"
machine_code = Helpers.GetMachineCode(v=2)
hash_values_list = requests.get(url).text.splitlines()

if machine_code not in hash_values_list:
    print("Kodni aktivlashtirish uchun @Enshteyn40 ga murojat qiling")
    print(machine_code)
    exit()

# 🎨 Terminal ranglar
def color(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

# 📁 Fayl mavjudligini tekshirish
def ensure_path_and_file(path, filename):
    if not os.path.exists(path): 
        print(f"{path} papkasi mavjud emas. Yaratilmoqda...")
        os.makedirs(path)

    filepath = os.path.join(path, filename)
    if not os.path.isfile(filepath):
        print(f"{filename} fayli topilmadi. Yaratilmoqda...")
        with open(filepath, 'w', encoding='utf-8') as f:
            pass
        sys.exit()
    else:
        print(f"{filename} fayli allaqachon mavjud: {filepath}")
    return filepath

print(color("Oxirgi kod yangilangan vaqti 28.05.2025 11:46 AM", "95"))

# 📱 Qurilmani aniqlash
if os.path.exists('/storage/emulated/0/giv'):
    print("Telefon uchun aniqlandi.")
    mrkt_file = ensure_path_and_file('/storage/emulated/0/giv', 'primegiftsid.csv')
elif os.path.exists('C:\\join'):
    print("Kompyuter uchun aniqlandi.") 
    mrkt_file = ensure_path_and_file('C:\\join', 'primegiftsid.csv')
else:
    print("Hech qanday mos papka topilmadi")
    sys.exit()

# 📲 Raqamlar ro‘yxati
phonecsv = "ozim"
with open(f'{phonecsv}.csv', 'r') as f:
    phlist = [row[0] for row in csv.reader(f)]
print(color('Spam bo‘lmagan raqamlar: ' + str(len(phlist)), "94"))

# 🔐 Telegram API
api_id = 22962676
api_hash = '543e9a4d695fe8c6aa4075c9525f7c57'

current_meid = "1062643042"
current_start_param = f"ref_{current_meid}_giveaway_25"

# 🔄 Har bir raqam bilan ishlash
for indexx, deltaxd in enumerate(phlist, 1):
    try:
        print(color(f"Login {deltaxd}", "92"))
        phone = utils.parse_phone(deltaxd)
        client = TelegramClient(f"sessions/{phone}", api_id, api_hash)
        print(color(f'Index : {indexx}', "96"))

        async def main(start_param, referrer_id):
            await client.start(phone)
            await client(UpdateStatusRequest(offline=False))
            bot_entity = await client.get_entity("@primegiftsbot")
            bot = InputUser(user_id=bot_entity.id, access_hash=bot_entity.access_hash)
            bot_app = InputBotAppShortName(bot_id=bot, short_name="gift")
            web_view = await client(RequestAppWebViewRequest(
                peer=bot,
                app=bot_app,
                platform="android",
                write_allowed=True,
                start_param=start_param
            ))

            auth_url = web_view.url.replace('tgWebAppVersion=7.0', 'tgWebAppVersion=8.0')
            tgwebappdata_part = auth_url.split("#tgWebAppData=")[-1].split("&tgWebAppVersion")[0]
            decoded_twice = unquote(unquote(tgwebappdata_part))
            params = parse_qs(decoded_twice)

            init_data = decoded_twice
            base64_encoded = base64.b64encode(init_data.encode()).decode()

            headers = {
                "accept": "application/json, text/plain, */*",
                "authorization": base64_encoded,
                "content-type": "application/json",
                "origin": "https://bot.primegifts.org",
                "referer": f"https://bot.primegifts.org/?startapp={start_param}",
                "user-agent": "Mozilla/5.0"
            }

            timestamp = int(time.time())
            user_data = json.loads(params["user"][0])
            payload = {
                "firstName": user_data.get("first_name", ""),
                "lastName": user_data.get("last_name", ""),
                "username": user_data.get("username", ""),
                "language": user_data.get("language_code", ""),
                "isPremium": user_data.get("is_premium", False),
                "avatar": user_data.get("photo_url", ""),
                "platform": "tdesktop",
                "referrer": referrer_id
            }

            login_resp = requests.post(f"https://api.primegifts.org/user/login?c={timestamp}", headers=headers, json=payload)
            print("Login status:", login_resp.status_code)

            # 🎁 Giveawaylar ro'yxatini olish
            giveaways_resp = requests.get(f"https://api.primegifts.org/giveaways/active?c={timestamp}", headers=headers)
            giveaways = giveaways_resp.json().get("items", [])
            tashkent_tz = pytz.timezone("Asia/Tashkent")

            with open("tonnelsnopdog.csv", "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Status", "Tugash Vaqti (Toshkent)", "Ticket Narxi", "Ishtirokchilar", "Kanallar", "NFTlar"])

                for giveaway in giveaways:
                    giveaway_id = giveaway.get("id")
                    detail_resp = requests.get(f"https://api.primegifts.org/user/giveaway/{giveaway_id}?c={timestamp}", headers=headers)
                    if detail_resp.status_code != 200:
                        continue

                    detail_data = detail_resp.json()

                    # 🎯 Filtr: ticketPrice == 0 va telegram-boost yo'q
                    if detail_data.get("ticketPrice", 0) != 0:
                        continue
                    if any(t.get("type") == "telegram-boost" for t in detail_data.get("tasks", [])):
                        continue

                    status = detail_data.get("status", "unknown")
                    end_date = detail_data.get("endDate", "")
                    if end_date:
                        dt = datetime.fromisoformat(end_date.replace("Z", "")).replace(tzinfo=timezone.utc)
                        end_date = dt.astimezone(tashkent_tz).strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        end_date = "Noma'lum"

                    ticket_price = detail_data.get("ticketPrice", 0)
                    participants = detail_data.get("participantsAmount", 0)
                    channels = ", ".join(detail_data.get("channels", []))
                    nft_counts = {}
                    for nft in detail_data.get("items", []):
                        if nft.get("type") == "nft":
                            name = nft["name"]
                            nft_counts[name] = nft_counts.get(name, 0) + 1
                    nft_summary = ", ".join([f"{name} ({count})" for name, count in nft_counts.items()]) or "Yo'q"

                    writer.writerow([giveaway_id, status, end_date, ticket_price, participants, channels, nft_summary])
                    print(color(f"✅ ID {giveaway_id} CSVga yozildi", "92"))

            return start_param, referrer_id

        with client:
            current_start_param, current_meid = client.loop.run_until_complete(main(current_start_param, current_meid))

    except Exception as e:
        print(color("Error:", "91"), color(str(e), "91"))
        continue
