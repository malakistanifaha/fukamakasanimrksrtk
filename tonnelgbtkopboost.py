# -*- coding: utf-8 -*-
import requests
from licensing.methods import Helpers
import sys

# GitHub repository URL
url = "https://raw.githubusercontent.com/Enshteyn40/crdevice/refs/heads/main/tonnel3boost.csv"

# Kodni tekshirish
response = requests.get(url)
lines = response.text.splitlines()
hash_values_list = [line.strip() for line in lines]

def GetMachineCode():
    return Helpers.GetMachineCode(v=2)

def color(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

machine_code = GetMachineCode()
print(machine_code)

if machine_code not in hash_values_list:
    print(color("Kodni aktivlashtirish uchun @Enshteyn40 ga murojat qiling", "95"))
    sys.exit()

# Asosiy kutubxonalarni import qilish
import os
import time
import base64
import asyncio
import csv
from urllib.parse import unquote
from cloudscraper import create_scraper
from Crypto.Hash import MD5
from Crypto.Cipher import AES
from datetime import datetime, timedelta, timezone
from telethon import TelegramClient, functions, utils
from telethon.tl.functions.account import UpdateStatusRequest
from telethon.tl.functions.messages import RequestAppWebViewRequest
from telethon.tl.types import InputUser, InputBotAppShortName
from telethon.tl.functions.channels import JoinChannelRequest
from colorama import Fore, init
init(autoreset=True)

# Proxy
ROTATED_PROXY = None
if os.path.exists(r"C:\\join\\proxy.csv"):
    with open(r"C:\\join\\proxy.csv") as f:
        ROTATED_PROXY = next(csv.reader(f))[0]
elif os.path.exists(r"/storage/emulated/0/giv/proxy.csv"):
    with open(r"/storage/emulated/0/giv/proxy.csv") as f:
        ROTATED_PROXY = next(csv.reader(f))[0]

proxies = {"http": ROTATED_PROXY, "https": ROTATED_PROXY}

def evp_kdf(password: bytes, salt: bytes, key_len: int, iv_len: int):
    dtot = b""
    d = b""
    while len(dtot) < key_len + iv_len:
        d = MD5.new(d + password + salt).digest()
        dtot += d
    return dtot[:key_len], dtot[key_len:key_len+iv_len]

def encrypt_timestamp(timestamp, secret_key):
    text = str(timestamp)
    salt = os.urandom(8)
    key, iv = evp_kdf(secret_key.encode(), salt, 32, 16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pad_length = AES.block_size - len(text.encode()) % AES.block_size
    padded_text = text.encode() + bytes([pad_length]*pad_length)
    encrypted = cipher.encrypt(padded_text)
    return base64.b64encode(b"Salted__" + salt + encrypted).decode()

async def main():
    path, filename = '', 'tonnelgivlar.csv'
    if os.path.exists('/storage/emulated/0/giv'):
        path = '/storage/emulated/0/giv'
    elif os.path.exists('C:\\join'):
        path = 'C:\\join'
    else:
        print(Fore.RED + "Papka topilmadi.")
        sys.exit()

    mrkt_file = os.path.join(path, filename)
    if not os.path.exists(mrkt_file):
        open(mrkt_file, 'w').close()
        print(Fore.YELLOW + f"{mrkt_file} yaratildi. Ma’lumotlarni kiriting.")
        sys.exit()

    giveaway_codes = [row[0] for row in csv.reader(open(mrkt_file, 'r', encoding='utf-8')) if row]
    if not os.path.exists('boostlilar.csv'):
        print(Fore.RED + "boostlilar.csv topilmadi!")
        sys.exit()

    phlist = [row[0] for row in csv.reader(open('boostlilar.csv', 'r'))]
    secret_key = "yowtfisthispieceofshitiiit"

    for i, phone in enumerate(phlist, 1):
        print(Fore.CYAN + f"[{i}] Login: {phone}")
        client = TelegramClient(f"sessions/{utils.parse_phone(phone)}", 22962676, '543e9a4d695fe8c6aa4075c9525f7c57')
        for code in giveaway_codes:
            try:
                await process(client, code, secret_key)
                await asyncio.sleep(2.5)
            except Exception as e:
                print(Fore.RED + f"❌ Xatolik: {e}")

async def process(client, giveaway_code, secret_key):
    print(Fore.YELLOW + f"🎁 Giv: {giveaway_code}")
    async with client:
        await client(UpdateStatusRequest(offline=False))
        bot_entity = await client.get_entity("tonnel_network_bot")
        bot = InputUser(user_id=bot_entity.id, access_hash=bot_entity.access_hash)
        bot_app = InputBotAppShortName(bot_id=bot, short_name="gifts")

        web_view = await client(RequestAppWebViewRequest(peer='me', app=bot_app, platform="android"))
        init_data = unquote(web_view.url.split('tgWebAppData=')[1].split('&')[0])

        headers = {
            "accept": "*/*", "content-type": "application/json",
            "user-agent": "Mozilla/5.0", "origin": "https://marketplace.tonnel.network",
            "referer": "https://marketplace.tonnel.network"
        }

        with create_scraper() as http_client:
            http_client.headers = headers
            http_client.proxies.update(proxies)

            r1 = http_client.post("https://gifts2.tonnel.network/api/balance/info", json={"authData": init_data, "ref": ""})
            print(Fore.GREEN + f"👤 User: {r1.json().get('name', 'NO')}")

            r2 = http_client.post("https://gifts2.tonnel.network/api/giveaway/info", json={"authData": init_data, "giveAwayId": giveaway_code})
            data = r2.json()
            status, criteria = data.get("status"), data["data"].get("eligibilityCriteria", {})
            chat, otherchats = data["data"]["chat"], data["data"]["otherChatIds"]

            for ch in [chat] + otherchats:
                await client(JoinChannelRequest(ch))
                print(Fore.BLUE + f"➕ Kanal: {ch}")

            if status == "not_joined" and criteria.get("only_boosters", False):
                print(Fore.YELLOW + "🔷 Boost talab qilinmoqda.")
                result = await client(functions.premium.GetMyBoostsRequest())

                if not result.my_boosts:
                    print(Fore.RED + "🚫 Boost topilmadi.")
                    return

                oldest_boost = None
                for b in sorted(result.my_boosts, key=lambda b: b.date):
                    if datetime.now(timezone.utc) - b.date >= timedelta(hours=24):
                        oldest_boost = b
                        break

                if not oldest_boost or not getattr(oldest_boost.peer, 'channel_id', None):
                    print(Fore.RED + "❌ Eng eski boostning channel_id yo‘q.")
                    return

                slot, ch_id = oldest_boost.slot, oldest_boost.peer.channel_id
                channel_name = next((c.title for c in result.chats if c.id == ch_id), "NOMA’LUM")

                print(Fore.CYAN + f"✅ Slot: {slot} | Kanal: {channel_name}")
                try:
                    await client(functions.premium.ApplyBoostRequest(peer=chat, slots=[slot]))
                    print(Fore.GREEN + f"🚀 Boost {slot} berildi.")
                except Exception as e:
                    print(Fore.RED + f"❌ Boost xatolik: {e}")
                return

            timestamp = str(int(time.time()))
            wtf = encrypt_timestamp(timestamp, secret_key)

            r3 = http_client.post("https://gifts.coffin.meme/api/giveaway/join", json={
                "authData": init_data, "giveAwayId": giveaway_code,
                "timestamp": timestamp, "wtf": wtf
            })
            if r3.ok:
                if r3.json().get("status") == "success":
                    print(Fore.GREEN + "✅ Giv muvaffaqiyatli!")
                else:
                    print(Fore.RED + f"❌ {r3.json().get('message')}")
            else:
                print(Fore.RED + f"🚫 API xatolik: {r3.status_code}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except asyncio.CancelledError:
        print(Fore.RED + "❌ Asinxron vazifa bekor qilindi.")
