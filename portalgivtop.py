
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
import random
from urllib.parse import unquote
from telethon.sync import TelegramClient
from telethon.tl.functions.account import UpdateStatusRequest
from telethon.tl.types import InputUser
from telethon.tl.functions.messages import RequestAppWebViewRequest
from telethon.tl.types import InputBotAppShortName
from datetime import datetime, timezone, timedelta
from pathlib import Path

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

def retry_request(method, url, max_retries=5, **kwargs):
    for attempt in range(max_retries):
        try:
            if method == 'GET':
                return requests.get(url, **kwargs)
            elif method == 'POST':
                return requests.post(url, **kwargs)
        except requests.exceptions.RequestException as e:
            print(color(f"⚠️ So‘rovda xatolik (urinish {attempt+1}/{max_retries}): {e}", "yellow"))
            time.sleep(2 + random.uniform(0.5, 1.5))
    raise Exception(f"❌ Maksimal {max_retries} marta urinildi, ammo {url} bajarilmadi")

def write_success_to_csv(giveaway_id, channels, endtime, participants, gift_names):
    outpath = Path("portaluz.csv")
    existing_ids = set()
    if outpath.exists():
        with open(outpath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_ids.add(row.get("Giveaway ID", ""))
    if giveaway_id in existing_ids:
        return
    write_header = not outpath.exists()
    with open(outpath, "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["Giveaway ID", "Channels", "Tugash vaqti", "Participants", "Gifts"])
        writer.writerow([
            giveaway_id,
            ", ".join(channels),
            endtime,
            participants,
            ", ".join(gift_names)
        ])

# Ma'lumotni yuklash
url = "https://raw.githubusercontent.com/Enshteyn40/crdevice/refs/heads/main/portal.csv"
response = requests.get(url)
lines = response.text.splitlines()
hash_values_list = [line.strip() for line in lines]
machine_code = Helpers.GetMachineCode(v=2)
print(color(machine_code, "white"))

if machine_code in hash_values_list:
    file_path_1 = r"C:\\join\\proxy.csv"
    file_path_2 = r"/storage/emulated/0/giv/proxy.csv"
    if os.path.exists(file_path_1):
        with open(file_path_1, 'r') as f:
            ROTATED_PROXY = next(csv.reader(f))[0]
    elif os.path.exists(file_path_2):
        with open(file_path_2, 'r') as f:
            ROTATED_PROXY = next(csv.reader(f))[0]

    proxies = {
        "http": ROTATED_PROXY,
        "https": ROTATED_PROXY
    }

    print(color("Oxirgi kod yanilangan vaqti 14.06.2025 04:09 PM", "magenta"))

    phonecsv = "ozim"
    with open(f'{phonecsv}.csv', 'r') as f:
        phlist = [row[0] for row in csv.reader(f)]
    print(color(f'Spam bo\'lmagan raqamlar: {len(phlist)}', "yellow"))

    for indexx, deltaxd in enumerate(phlist):
        try:
            print(color(f"Login {deltaxd}", "green"))
            phone = utils.parse_phone(deltaxd)
            api_id = 22962676
            api_hash = '543e9a4d695fe8c6aa4075c9525f7c57'
            client = TelegramClient(f"sessions/{phone}", api_id, api_hash)
            client.start(phone)
            client(UpdateStatusRequest(offline=False))

            print(color(f'Index: {indexx + 1}', "blue"))
            print()

            async def main():
                bot_entity = await client.get_entity("@giftsgiveawaybot")
                bot = InputUser(user_id=bot_entity.id, access_hash=bot_entity.access_hash)
                bot_app = InputBotAppShortName(bot_id=bot, short_name="start")
                web_view = await client(RequestAppWebViewRequest(
                    peer=bot,
                    app=bot_app,
                    platform="android",
                    write_allowed=True,
                    start_param="start"
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
                    "inviter_id": 0
                }

                response = retry_request("POST", "https://api.giftaway.org/api/auth", json=jsondata, proxies=proxies, headers=headers, timeout=10)
                jwt_token = response.json()["result"]["jwt"]
                headers["Authorization"] = f"Bearer {jwt_token}"

                toshkent_tz = timezone(timedelta(hours=5))

                if indexx == 0:
                    try:
                        list_url = "https://api.giftaway.org/api/giveaway/list/5?page=1&count=100"
                        response = retry_request("GET", list_url, headers=headers, proxies=proxies, timeout=10)
                        data = response.json()

                        for g in data["result"]["giveaways"]:
                            gid = g["id"]
                            try:
                                detail = retry_request("GET", f"https://api.giftaway.org/api/giveaway/{gid}", headers=headers, proxies=proxies, timeout=10)
                                r = detail.json()["result"]
                                end_time = datetime.fromisoformat(r["ending_at"]).astimezone(toshkent_tz)

                                if (
                                    r.get("is_completed") is False
                                    and not any(t.get("type") in [2, 3] for t in r.get("tasks", []))
                                    and end_time > datetime.now(toshkent_tz)
                                ):
                                    joined_channels = [task.get("value") for task in r["tasks"] if task.get("type") in [1, 4]]
                                    gift_names = [gift.get("name") for gift in r.get("gifts", [])]
                                    participants = r.get("participants", 0)
                                    
                                    write_success_to_csv(
                                        gid,
                                        joined_channels,
                                        end_time.strftime("%Y-%m-%d %H:%M"),
                                        participants,
                                        gift_names
                                    )


                            except Exception as e:
                                print(color(f"❌ Giveaway ID {gid} tafsilotlarida xatolik: {e}", "red"))
                                continue

                    except Exception as e:
                        print(color(f"❌ Giveaway ro‘yxatini olishda umumiy xatolik: {e}", "red"))
                        return
            with client:
                client.loop.run_until_complete(main())

        except Exception as e:
            print(color("Error:", "red"), color(str(e), "red"))
            continue

else:
    print(color("Kodni aktivlashtirish uchun @Enshteyn40 ga murojat qiling", "magenta"))
