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

url = "https://raw.githubusercontent.com/Enshteyn40/crdevice/refs/heads/main/mrkt.csv"
machine_code = Helpers.GetMachineCode(v=2)
hash_values_list = requests.get(url).text.splitlines()

if machine_code not in hash_values_list:
    print(colored("Kodni aktivlashtirish uchun @Enshteyn40 ga murojat qiling", "magenta"))
    sys.exit()

print(colored("Oxirgi kod yangilangan vaqti: 23.05.2025 8:28 PM", "magenta"))

api_id = 22962676
api_hash = '543e9a4d695fe8c6aa4075c9525f7c57'

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
with open('phone.csv', 'r') as f:
    phones = [row[0] for row in csv.reader(f)]

print(colored(f"Spam bo‘lmagan raqamlar: {len(phones)}", "blue"))

def color(text, color_code):
        return f"\033[{color_code}m{text}\033[0m"
async def process_account(phone, index):
    try:
        print(colored(f"[{index}] Login: {phone}", "green"))
        parsed_phone = utils.parse_phone(phone)
        client = TelegramClient(f"sessions/{parsed_phone}", api_id, api_hash)
        await client.start(phone=parsed_phone)
        await client(UpdateStatusRequest(offline=False))

        for giveaway_code in giv_ids_ozim:
            try:
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

                auth_res = requests.post(
                    url="https://api.tgmrkt.io/api/v1/auth",
                    json={"appId": 1062643042, "data": init_data, "photo": photo_url},
                    headers=headers, timeout=10
                )
                token = auth_res.json().get("token")
                giveaway_id = giveaway_code

                headers["authorization"] = token
                data = requests.get(f"https://api.tgmrkt.io/api/v1/giveaways/{giveaway_id}", headers=headers).json()
                my_tickets_count = data.get("myTicketsCount")

                if my_tickets_count > 0:
                    print(colored("Allaqachon qatnashgan.", "cyan"))
                    continue

                validations = requests.get(
                    f"https://api.tgmrkt.io/api/v1/giveaways/check-validations/{giveaway_id}",
                    headers=headers).json().get("channelValidations", [])

                for item in validations:
                    channel = item.get("channel")
                    if channel:
                        try:
                            await client(JoinChannelRequest(channel))
                        except Exception as e:
                            print(colored(f"Kanalga qo'shishda xatolik: {e}", "red"))

                        requests.post(
                            f"https://api.tgmrkt.io/api/v1/giveaways/start-validation/{giveaway_id}",
                            params={"channel": channel, "type": "ChannelMember"}, headers=headers
                        )

                response = requests.post(
                    f"https://api.tgmrkt.io/api/v1/giveaways/buy-tickets/{giveaway_id}",
                    params={"count": 1}, headers=headers
                )
                try:
                    data = response.json()
                    if isinstance(data, list) and data:
                        print(color("GIVEAWAYGA MUVAFFAQIYATLI QATNASHDI", "92"))  # yashil
                    else:
                        print(color("GIVEAWAYA OLDIN QATNASHGAN QATNASHMAGAN BOSA XORAMI KANALI BAN BERAYABDI", "93")) 
                except Exception as e:
                    print(color("Pizdes sorob yubotishda xatolik", "91"))  # qizil
            except Exception as e:
                print(colored(f"Giveaway xatosi: {e}", "red"))

        await client.disconnect()
    except Exception as e:
        print(colored(f"[{index}] Xatolik: {e}", "red"))

async def main():
    batch_size = 5
    tasks = []
    for idx, phone in enumerate(phones, 1):
        tasks.append(process_account(phone, idx))
        if len(tasks) == batch_size:
            await asyncio.gather(*tasks)
            tasks = []
    if tasks:
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())
