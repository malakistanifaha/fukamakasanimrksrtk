# -*- coding: utf-8 -*-
import requests
from licensing.methods import Helpers

# GitHub repository URL
url = "https://raw.githubusercontent.com/Enshteyn40/crdevice/refs/heads/main/mrkt.csv"

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
    from telethon import types, utils, errors
    import time
    from urllib.parse import unquote
    from telethon.sync import TelegramClient
    from telethon.tl.functions.account import UpdateStatusRequest
    from telethon.tl.types import InputUser
    from telethon.tl.functions.messages import RequestAppWebViewRequest
    from telethon.tl.types import InputBotAppShortName
    import requests
    print(color("Oxirgi kod yanilangan vaqti 15.05.2025 9:39 PM", "95"))  # magenta
    phonecsv = "phone"
    with open(f'{phonecsv}.csv', 'r') as f:
        phlist = [row[0] for row in csv.reader(f)]
    print(color('Spam bolmagan raqamlar: ' + str(len(phlist)), "94"))  # ko‘k
    
    givid = str(input("Givid kiriting: "))
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
            async def main():
                bot_entity = await client.get_entity("@main_mrkt_bot")
                bot = InputUser(user_id=bot_entity.id, access_hash=bot_entity.access_hash)
                bot_app = InputBotAppShortName(bot_id=bot, short_name="app")
                web_view = await client(
                    RequestAppWebViewRequest(
                        peer=bot,
                        app=bot_app,
                        platform="android",
                        write_allowed=True,
                        start_param=givid
                    )
                )
                auth_url = web_view.url.replace('tgWebAppVersion=7.0', 'tgWebAppVersion=8.0')
                init_data = unquote(auth_url.split('tgWebAppData=', 1)[1].split('&tgWebAppVersion', 1)[0])
                
                init_data_decoded = unquote(init_data)

                user_json_str = init_data_decoded.split("user=", 1)[1].split("&", 1)[0]

                user_data = json.loads(user_json_str)
                photo_url = user_data.get("photo_url")

                
                headers = {
                    "accept": "*/*",
                    "accept-encoding": "gzip, deflate, br, zstd",
                    "accept-language": "en-US,en;q=0.9",
                    "content-type": "application/json",
                    "origin": "https://cdn.tgmrkt.io",
                    "referer": "https://cdn.tgmrkt.io/",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0"
                }
                
                jsondata = {
                    "appId": 1062643042,
                    "data": init_data,
                    "photo": photo_url
                }
                
                response = requests.post(url="https://api.tgmrkt.io/api/v1/auth", json=jsondata, headers=headers, timeout=10)
                response_data = response.json()
                token = response_data.get("token")
                giveaway_id = response_data.get("giveawayId")
                print(color("Giveaway ID:", "93"), color(giveaway_id, "91"))  # sariq va qizil
                
                headers = {
                    "accept": "*/*",
                    "accept-encoding": "gzip, deflate, br, zstd",
                    "accept-language": "en-US,en;q=0.9",
                    "authorization": token,
                    "origin": "https://cdn.tgmrkt.io",
                    "referer": "https://cdn.tgmrkt.io/",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0"
                }
                response = requests.get(url=f"https://api.tgmrkt.io/api/v1/giveaways/{giveaway_id}", headers=headers, timeout=10)
                data = json.loads(response.text)
                gift_names = [gift['name'] for gift in data.get("gifts", [])]
                participants_count = data.get("participantsCount")
                my_tickets_count = data.get("myTicketsCount")
                print(f"\033[97m O'YNALAYOTGAN GIFT NOMLARI:\033[0m")
                for name in gift_names:
                    print(f"\033[97m- {name}\033[0m")
                print(f"\033[97m Ishtirokchilar soni: {participants_count}\033[0m")
                print(f"\033[97m Mening chiptalarim soni: {my_tickets_count}\033[0m")

                
                if my_tickets_count > 0:
                    print(color("GIVEAWAYGA OLDIN QATNASHAN EKAN", "92"))  # yashil
                else:
                    print(color("GIVEAWAYA QO'SHILISHNI BOSHLADIM", "95"))  # magenta
                    premium_channels = []
                    
                    response = requests.get(url=f"https://api.tgmrkt.io/api/v1/giveaways/check-validations/{giveaway_id}", headers=headers, timeout=10)
                    data = response.json()
                    validations = data.get("channelValidations", [])
                    for item in validations:
                        channel = item.get("channel")
                        if channel:
                            premium_channels.append(channel)
                    for ochiq_link in premium_channels:
                        try:
                            await client(JoinChannelRequest(ochiq_link)) 
                            print(color(f"Kanalga a'zo bo'ldi {ochiq_link}", "92"))  # yashil
                        except Exception as e:
                            print(color(f"Kanalga qo'shilishda xatolik {ochiq_link}: {e}", "91"))  # qizil
                    birinchi = premium_channels[0] if premium_channels else None
                    params = {
                        "channel": birinchi,
                        "type": "ChannelMember"
                    }
                    response = requests.post(url=f"https://api.tgmrkt.io/api/v1/giveaways/start-validation/{giveaway_id}", params=params, headers=headers, timeout=10)
                    params = {
                        "count": 1
                    }
                    response = requests.post(url=f"https://api.tgmrkt.io/api/v1/giveaways/buy-tickets/{giveaway_id}", params=params, headers=headers, timeout=10)
                    try:
                        data = response.json()
                        if isinstance(data, list) and data:
                            print(color("GIVEAWAYGA MUVAFFAQIYATLI QATNASHDI", "92"))  # yashil
                        else:
                            print(color("GIVEAWAYA OLDIN QATNASHGAN QATNASHMAGAN BOSA XORAMI KANALI BAN BERAYABDI", "93")) 
                    except Exception as e:
                        print(color("Pizdes sorob yubotishda xatolik", "91"))  # qizil
            with client:
                client.loop.run_until_complete(main())
        except Exception as e:
            print(color("Error:", "91"), color(str(e), "91"))  # qizil
            continue
else:
    print(color("Kodni aktivlashtirish uchun @Enshteyn40  ga murojat qiling", "95"))  # magenta
