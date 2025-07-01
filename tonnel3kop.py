# -*- coding: utf-8 -*-
import requests
from licensing.methods import Helpers
import sys
# GitHub repository URL
url = "https://raw.githubusercontent.com/Enshteyn40/crdevice/refs/heads/main/tonnel_3.csv"

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
    import os
    import time
    import base64
    import asyncio
    import csv
    from urllib.parse import unquote
    from cloudscraper import create_scraper
    from Crypto.Hash import MD5
    from Crypto.Cipher import AES
    from telethon import TelegramClient
    from telethon.tl.functions.account import UpdateStatusRequest
    from telethon.tl.functions.messages import RequestAppWebViewRequest
    from telethon.tl.types import InputUser, InputBotAppShortName
    from telethon.tl.functions.channels import JoinChannelRequest
    from telethon import utils
    from colorama import Fore, Style, init
    import sys
    init(autoreset=True)
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


    def evp_kdf(password: bytes, salt: bytes, key_len: int, iv_len: int):
        dtot = b""
        d = b""
        while len(dtot) < key_len + iv_len:
            d = MD5.new(d + password + salt).digest()
            dtot += d
        return dtot[:key_len], dtot[key_len:key_len + iv_len]


    def encrypt_timestamp(timestamp, secret_key):
        text = str(timestamp)
        salt = os.urandom(8)
        key, iv = evp_kdf(secret_key.encode('utf-8'), salt, 32, 16)
        cipher = AES.new(key, AES.MODE_CBC, iv)

        pad_length = AES.block_size - (len(text.encode('utf-8')) % AES.block_size)
        padded_text = text.encode('utf-8') + bytes([pad_length] * pad_length)

        encrypted = cipher.encrypt(padded_text)
        encrypted_data = b"Salted__" + salt + encrypted

        return base64.b64encode(encrypted_data).decode('utf-8')


    async def main():
        def ensure_path_and_file(path, filename):
            if not os.path.exists(path):
                print(f"{path} papkasi mavjud emas. Yaratilmoqda...")
                os.makedirs(path)

            filepath = os.path.join(path, filename)
            if not os.path.isfile(filepath):
                print(Fore.WHITE + f"{filename} fayli topilmadi. csv fayl yaratildi.")
                print(Fore.WHITE + "Endi gividlarni yozib chiqing")
                with open(filepath, 'w', encoding='utf-8') as f:
                    pass
                sys.exit()
            else:
                print(f"{filename} fayli allaqachon mavjud: {filepath}")
            return filepath

        if os.path.exists('/storage/emulated/0/giv'):
            print(Fore.YELLOW + "Telefon uchun papka aniqlandi")
            mrkt_file = ensure_path_and_file('/storage/emulated/0/giv', 'tonnelgivlar.csv')
            giveaway_codes = [row[0] for row in csv.reader(open(mrkt_file, 'r', encoding='utf-8')) if row]
        elif os.path.exists('C:\\join'):
            print(Fore.YELLOW + "Kompyuer uchun papka aniqlandi")
            mrkt_file = ensure_path_and_file('C:\\join', 'tonnelgivlar.csv')
            giveaway_codes = [row[0] for row in csv.reader(open(mrkt_file, 'r', encoding='utf-8')) if row]
        else:
            print(Fore.YELLOW + "Hech qanday mos papka topilamadi (telefonda storage/0  da giv papka yarating) Kompda esa (C/ diskda join papka)")
        with open('phone.csv', 'r') as f:
            phlist = [row[0] for row in csv.reader(f)]
        
        for indexx, deltaxd in enumerate(phlist):
            print("🏳️‍🌈")
            print(Fore.CYAN + f"📲 Login: " + Fore.WHITE + deltaxd)
            print(Fore.MAGENTA + f'📶 Nechanchi raqam: ' + Fore.WHITE + str(indexx + 1))
            phone = utils.parse_phone(deltaxd)
            api_id = 22962676
            api_hash = '543e9a4d695fe8c6aa4075c9525f7c57'
            tg_client = TelegramClient(f"sessions/{phone}", api_id, api_hash)
            secret_key = "yowtfisthispieceofshitiiit"
            for giveaway_code in giveaway_codes:
                try:
                    await process(tg_client, giveaway_code, secret_key)
                    await asyncio.sleep(2.5)
                except Exception as e:
                    print(Fore.RED + "❌ Xatolik yuz berdi (" + Fore.WHITE + f"{deltaxd}" + Fore.RED + f"): {e}")


    async def process(tg_client: TelegramClient, giveaway_code, secret_key):
        print(Fore.YELLOW + "🎁 Ushbu givga qo'shilishni boshladim: " + Fore.WHITE + giveaway_code)
        async with tg_client:
            await tg_client(UpdateStatusRequest(offline=False))
            bot_entity = await tg_client.get_entity("tonnel_network_bot")
            bot = InputUser(user_id=bot_entity.id, access_hash=bot_entity.access_hash)
            bot_app = InputBotAppShortName(bot_id=bot, short_name="gifts")
            web_view = await tg_client(
                RequestAppWebViewRequest(
                    peer='me',
                    app=bot_app,
                    platform="android"
                )
            )
            auth_url = web_view.url.replace('tgWebAppVersion=7.0', 'tgWebAppVersion=8.0')
            init_data = unquote(auth_url.split('tgWebAppData=', 1)[1].split('&tgWebAppVersion', 1)[0])
            headers = {
                "accept": "*/*",
                "accept-encoding": "gzip",
                "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,pl;q=0.6",
                "content-type": "application/json",
                "origin": "https://marketplace.tonnel.network",
                "referer": "https://marketplace.tonnel.network",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "cross-site",
                "user-agent": "Mozilla/5.0"
            }

            with create_scraper() as http_client:
                http_client.headers = headers
                http_client.proxies.update(proxies)
                json_data = {
                    "authData": init_data,
                    "ref": ""
                }
                response = http_client.post(url="https://gifts2.tonnel.network/api/balance/info", json=json_data)
                data = response.json()
                print(Fore.GREEN + '👤 User info: ' + Fore.WHITE + data.get("name", "NO"))

                json_data = {
                    "authData": init_data,
                    "giveAwayId": giveaway_code
                }
                response = http_client.post(url="https://gifts2.tonnel.network/api/giveaway/info", json=json_data)
                data = response.json()
                status = data.get("status")
                criteria = data.get("data", {}).get("eligibilityCriteria", {})
                print(Fore.CYAN + '📋 Talablar: ' + Fore.WHITE + str(criteria))

                chat = data["data"]["chat"]
                otherchats = data["data"]["otherChatIds"]
                
                premium_channels = [chat] + otherchats
                for chat in premium_channels:
                    await tg_client(JoinChannelRequest(chat))
                    print(Fore.BLUE + "➕ Kanalga qo'shilayabman: " + Fore.WHITE + str(chat))

                if status != "not_joined":
                    print(Fore.YELLOW + "ℹ️ Giveaway holati: " + Fore.WHITE + status)
                    return

                timestamp = str(int(time.time()))
                wtf = encrypt_timestamp(timestamp, secret_key)

                json_data = {
                    "authData": init_data,
                    "giveAwayId": giveaway_code,
                    "timestamp": timestamp, 
                    "wtf": wtf
                }

                response = http_client.post(url="https://gifts.coffin.meme/api/giveaway/join", json=json_data)
                if response.ok:
                    join_data = response.json()
                    if join_data.get("status") == "success":
                        print(Fore.GREEN + "✅ Givga muvaffaqiyatli qo‘shildi!")
                    elif "already participated" in join_data.get("message", ""):
                        print(Fore.YELLOW + "⚠️ Oldin qatnashgan!")
                    else:
                        print(Fore.RED + "❌ Xato: " + Fore.WHITE + join_data.get("message"))
                else:
                    print(Fore.RED + "🚫 Join API xatolik: " + Fore.WHITE + f"{response.status_code} {response.text}")


    if __name__ == "__main__":
        asyncio.run(main())
else:
    print(color("Kodni aktivlashtirish uchun @Enshteyn40  ga murojat qiling", "95"))  # magenta
