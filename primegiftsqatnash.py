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

# 🔐 Aktivatsiya
url = "https://raw.githubusercontent.com/Enshteyn40/crdevice/refs/heads/main/primegifts.csv"
machine_code = Helpers.GetMachineCode(v=2)
hash_values_list = requests.get(url).text.splitlines()

if machine_code not in hash_values_list:
    print("Kodni aktivlashtirish uchun @Enshteyn40 ga murojat qiling")
    print(machine_code)
    exit()

# 🎨 Rangli chiqarish
def color(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

# 📁 Fayl mavjudligini tekshirish
def ensure_path_and_file(path, filename):
    if not os.path.exists(path): 
        print(color(f"{path} papkasi mavjud emas. Yaratilmoqda...", "93"))
        os.makedirs(path)

    filepath = os.path.join(path, filename)
    if not os.path.isfile(filepath):
        print(color(f"{filename} fayli topilmadi. Yaratilmoqda...", "93"))
        with open(filepath, 'w', encoding='utf-8') as f:
            pass
        sys.exit()
    else:
        print(color(f"{filename} fayli allaqachon mavjud: {filepath}", "92"))
    return filepath

print(color("Oxirgi kod yangilangan vaqti 20.06.2025 02:11 AM", "95"))

# 📱 Qurilma aniqlash
if os.path.exists('/storage/emulated/0/giv'):
    print(color("Telefon uchun aniqlandi.", "96"))
    mrkt_file = ensure_path_and_file('/storage/emulated/0/giv', 'primegiftsid.csv')
elif os.path.exists('C:\\join'):
    print(color("Kompyuter uchun aniqlandi.", "96"))
    mrkt_file = ensure_path_and_file('C:\\join', 'primegiftsid.csv')
else:
    print(color("Hech qanday mos papka topilmadi", "91"))
    sys.exit()

# 📲 Telefon raqamlar ro‘yxati
phonecsv = "phone"
with open(f'{phonecsv}.csv', 'r') as f:
    phlist = [row[0] for row in csv.reader(f)]
print(color('Spam bo‘lmagan raqamlar: ' + str(len(phlist)), "94"))

# Telegram API
api_id = 22962676
api_hash = '543e9a4d695fe8c6aa4075c9525f7c57'

# CSVdagi giveaway IDlarni o‘qish
with open(mrkt_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    giv_ids_ozim = [row[0] for row in reader if row]

# 🔄 Har bir raqam bilan ishlash
for indexx, deltaxd in enumerate(phlist, 1):
    try:
        print(color(f"Login {deltaxd}", "92"))
        phone = utils.parse_phone(deltaxd)
        client = TelegramClient(f"sessions/{phone}", api_id, api_hash)
        print(color(f'Index : {indexx}', "96"))

        async def main():
            await client.start(phone)
            await client(UpdateStatusRequest(offline=False))

            for givid in giv_ids_ozim:
                start_param = f"ref_1062643042_giveaway_{givid}"
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
                    "referrer": "1062643042"
                }

                login_resp = requests.post(f"https://api.primegifts.org/user/login?c={timestamp}", headers=headers, json=payload)
                print(color("Login status:", "96"), color(str(login_resp.status_code), "97"))
                
                response = requests.get(f"https://api.primegifts.org/user/giveaway/{givid}?c={timestamp}", headers=headers)
                data = response.json()
                status = data.get("status", "unknown")
                end_date = data.get("endDate", "")
                if end_date:
                    utc_dt = datetime.fromisoformat(end_date.replace("Z", "")).replace(tzinfo=timezone.utc)
                    toshkent_dt = utc_dt.astimezone(timezone(timedelta(hours=5)))
                    formatted_dt = toshkent_dt.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    formatted_dt = "Noma'lum"
                participants = data.get("participantsAmount", 0)
                channels = data.get("channels", [])
                premium_channels = []
                channels_raw = data.get("channels", [])
                for ch in channels_raw:
                    if isinstance(ch, str):
                        premium_channels.append(f"@{ch}")
                    elif isinstance(ch, dict):
                        username = ch.get("username")
                        if username:
                            premium_channels.append(f"@{username}")
                for ch in premium_channels:
                    print(color(f"- {ch}", "96"))
                    try:
                        await client(JoinChannelRequest(ch))
                        print(color(f"Kanalga a'zo bo'ldi {ch}", "92"))
                    except Exception as e:
                        print(color(f"Kanalga qo'shilishda xatolik {ch}: {e}", "91"))
                items = data.get("items", [])
                item_list = [f"{item.get('name', 'No Name')} (Model: {item.get('model', {}).get('name', 'No Model')})" for item in items]
                winners = [str(w) for w in data.get("winners", [])] or ["(Yo'q)"]
                purchased_tickets = data.get("purchasedTickets", 0)
                tasks = data.get("tasks", [])
                task_list = [f"{t.get('name', 'No name')} ({t.get('type', 'unknown')}) - {'✅' if t.get('completed') else '❌'}" for t in tasks]

                print(color(f"\n🟡 Giveaway Status: {status}", "93"))
                print(color(f"⏳ Tugash vaqti: {formatted_dt}", "95"))
                print(color(f"👥 Ishtirokchilar soni: {participants}", "94"))
                print(color(f"📢 Kanallar: {', '.join(channels)}", "96"))

                print(color("\n🎁 Sovg'alar:", "92"))
                for gift in item_list:
                    print(color(f"  - {gift}", "92"))

                print(color(f"\n🏆 G'oliblar: {', '.join(winners)}", "95"))
                print(color(f"🎟 Xarid qilingan chiptalar: {purchased_tickets}", "96"))
                print(color("\n📋 Vazifalar:", "94"))
                
                if purchased_tickets == 0:
                    print(color("GIVEAWAYA QO'SHILISHNI BOSHLADIM", "92"))
                    for task in task_list:
                        print(color(f"  - {task}", "93"))
                    
                    task_ids = [t.get("id") for t in tasks if "id" in t]

                    for task_id in task_ids:
                        task_url = f"https://api.primegifts.org/user/giveaway/tasks/check?c={timestamp}"
                        response = requests.post(task_url, headers=headers, json={"taskId": task_id})
                        print(color(f"🧩 Task ID {task_id} bajardimi: {response.status_code} -> {response.text}", "96"))
                else:
                    print(color("⚠️ Avval bu giveawayda qatnashgan ekan", "91"))
                    
        with client:
            client.loop.run_until_complete(main())

    except Exception as e:
        print(color("Error:", "91"), color(str(e), "91"))
        continue
