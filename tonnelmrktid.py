# -*- coding: utf-8 -*-
import asyncio
import csv
import json
import os
import sys
import requests
from urllib.parse import unquote
from licensing.methods import Helpers
from termcolor import colored
from telethon import utils, TelegramClient
from telethon.tl.functions.account import UpdateStatusRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import RequestAppWebViewRequest
from telethon.tl.types import InputUser, InputBotAppShortName

# --- License tekshiruv ---
url = "https://raw.githubusercontent.com/Enshteyn40/crdevice/refs/heads/main/mrkt.csv"
machine_code = Helpers.GetMachineCode(v=2)
hash_values_list = requests.get(url, timeout=15).text.splitlines()
if machine_code not in hash_values_list:
    print(colored("Kodni aktivlashtirish uchun @Enshteyn40 ga murojat qiling", "magenta"))
    sys.exit()
print(colored("Oxirgi kod yangilangan vaqti: 23.05.2025 8:28 PM", "magenta"))

# --- API ---
api_id = 22962676
api_hash = '543e9a4d695fe8c6aa4075c9525f7c57'

# --- Yordamchi ---
def ensure_path_and_file(path, filename):
    if not os.path.exists(path):
        print(f"{path} papkasi mavjud emas. Yaratilmoqda...")
        os.makedirs(path)
    filepath = os.path.join(path, filename)
    if not os.path.isfile(filepath):
        print(f"{filename} fayli topilmadi. csv fayl yaratildi.")
        with open(filepath, 'w', encoding='utf-8') as f:
            pass
        sys.exit("GIV fayl yaratildi. Dastur to'xtadi.")
    return filepath

# GIV faylni aniqlash
giv_path = ('/storage/emulated/0/giv' if os.path.exists('/storage/emulated/0/giv')
            else 'C:\\join' if os.path.exists('C:\\join') else None)
if not giv_path:
    sys.exit("Hech qanday mos papka topilmadi")

mrkt_file = ensure_path_and_file(giv_path, 'MRKTGIVLARid.csv')
giv_ids_ozim = [row[0] for row in csv.reader(open(mrkt_file, 'r', encoding='utf-8')) if row]

# Telefon raqamlarini o'qish
with open('phone.csv', 'r', encoding='utf-8') as f:
    phones = [row[0] for row in csv.reader(f) if row]
print(colored(f"Spam bo‘lmagan raqamlar: {len(phones)}", "blue"))

# sessions papkasini tayyorlab qo'yamiz
os.makedirs('sessions', exist_ok=True)

def color(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

async def process_account(phone, index):
    try:
        parsed_phone = utils.parse_phone(phone)
        session_path = f"sessions/{parsed_phone}"
        print(colored(f"[{index}] Login: {parsed_phone}", "green"))

        client = TelegramClient(session_path, api_id, api_hash)

        # Faqat sessiya mavjud va avtorizatsiya qilingan bo'lsa ishlatamiz
        await client.connect()
        try:
            authorized = await client.is_user_authorized()
        except Exception as e:
            # Ba'zan connect bo'lib, ammo query xatolik berishi mumkin
            print(colored(f"[{index}] Authorized tekshiruv xatosi: {e}", "red"))
            authorized = False

        if not authorized:
            print(colored(f"[{index}] Sessiya avtorizatsiya qilinmagan. SKIP.", "yellow"))
            await client.disconnect()
            return

        # Online ko'rsatish (ixtiyoriy)
        try:
            await client(UpdateStatusRequest(offline=False))
        except Exception:
            pass

        # Har bir giveaway uchun aylanish
        for giveaway_code in giv_ids_ozim:
            try:
                # Bot entity-ni bir marta olib ishlatamiz
                bot_entity = await client.get_entity("@main_mrkt_bot")
                bot = InputUser(user_id=bot_entity.id, access_hash=bot_entity.access_hash)
                bot_app = InputBotAppShortName(bot_id=bot, short_name="app")

                web_view = await client(RequestAppWebViewRequest(
                    peer=bot, app=bot_app, platform="android",
                    write_allowed=True, start_param="1062643042"
                ))

                auth_url = web_view.url.replace('tgWebAppVersion=7.0', 'tgWebAppVersion=8.0')
                init_data = unquote(auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0])
                user_json_str = unquote(init_data).split("user=")[1].split("&")[0]
                user_data = json.loads(user_json_str)
                photo_url = user_data.get("photo_url")

                headers = {
                    "content-type": "application/json",
                    "origin": "https://cdn.tgmrkt.io",
                    "referer": "https://cdn.tgmrkt.io/",
                    "user-agent": "Mozilla/5.0"
                }

                # Auth
                auth_res = requests.post(
                    url="https://api.tgmrkt.io/api/v1/auth",
                    json={"appId": 1062643042, "data": init_data, "photo": photo_url},
                    headers=headers, timeout=15
                )
                auth_res.raise_for_status()
                token = auth_res.json().get("token")
                if not token:
                    print(colored("Token olinmadi. SKIP.", "yellow"))
                    continue

                headers["authorization"] = token
                giveaway_id = giveaway_code

                # Mening holatim
                data = requests.get(
                    f"https://api.tgmrkt.io/api/v1/giveaways/{giveaway_id}",
                    headers=headers, timeout=15
                ).json()
                my_tickets_count = data.get("myTicketsCount") or 0
                if my_tickets_count > 0:
                    print(colored("Allaqachon qatnashgan.", "cyan"))
                    continue

                # Validations
                validations = requests.get(
                    f"https://api.tgmrkt.io/api/v1/giveaways/check-validations/{giveaway_id}",
                    headers=headers, timeout=15
                ).json().get("channelValidations", []) or []

                for item in validations:
                    channel = item.get("channel")
                    if not channel:
                        continue
                    try:
                        await client(JoinChannelRequest(channel))
                    except Exception as e:
                        print(colored(f"Kanalga qo'shishda xatolik: {e}", "red"))

                    try:
                        requests.post(
                            f"https://api.tgmrkt.io/api/v1/giveaways/start-validation/{giveaway_id}",
                            params={"channel": channel, "type": "ChannelMember"},
                            headers=headers, timeout=15
                        )
                    except Exception as e:
                        print(colored(f"Validation start xatosi: {e}", "red"))

                # Bilet sotib olish
                response = requests.post(
                    f"https://api.tgmrkt.io/api/v1/giveaways/buy-tickets/{giveaway_id}",
                    params={"count": 1}, headers=headers, timeout=15
                )
                try:
                    resp_json = response.json()
                    if isinstance(resp_json, list) and resp_json:
                        print(color("GIVEAWAYGA MUVAFFAQIYATLI QATNASHDI", "92"))  # yashil
                    else:
                        print(color("GIVEAWAYA OLDIN QATNASHGAN YOKI LIMIT/VALIDATION MUAMMO", "93"))  # sariq
                except Exception:
                    print(color("Pizdes: buy-tickets javobini o‘qishda xatolik", "91"))  # qizil

            except Exception as e:
                print(colored(f"Giveaway xatosi: {e}", "red"))

        await client.disconnect()

    except Exception as e:
        print(colored(f"[{index}] Xatolik: {e}", "red"))

async def main():
    batch_size = 5  # bir vaqtda nechta raqam ishlasin
    tasks = []
    for idx, phone in enumerate(phones, 1):
        tasks.append(process_account(phone, idx))
        if len(tasks) == batch_size:
            await asyncio.gather(*tasks, return_exceptions=True)
            tasks = []
    if tasks:
        await asyncio.gather(*tasks, return_exceptions=True)

if __name__ == '__main__':
    asyncio.run(main())
