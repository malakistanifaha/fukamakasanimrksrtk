# -*- coding: utf-8 -*-
import requests
from licensing.methods import Helpers

# GitHub repository URL
url = "https://raw.githubusercontent.com/Enshteyn40/crdevice/refs/heads/main/portal.csv"

# URL'dan CSV faylni yuklab olish
response = requests.get(url)
lines = response.text.splitlines()
hash_values_list = [line.strip() for line in lines]

def GetMachineCode():
    machine_code = Helpers.GetMachineCode(v=2)
    return machine_code

machine_code = GetMachineCode()
print(machine_code)

if machine_code in hash_values_list:
    from telethon.sync import TelegramClient
    import csv
    from telethon.tl.functions.account import UpdateStatusRequest
    from telethon import utils
    import time
    from datetime import datetime
    import pytz

    phonecsv = "ozim"
    ovoz_berildi = []
    ovoz_berilamadi = []

    with open(f'{phonecsv}.csv', 'r') as f:
        phlist = [row[0] for row in csv.reader(f)]

    print('NOMERLAR: ' + str(len(phlist)))

    user = "@giftsgiveawaybot"
    api_id = 6810439
    api_hash = '66ac3b67cce1771ce129819a42efe02e'

    with open('giftaweyutgan.csv', 'w', newline='', encoding='utf-8') as spamemas_file:
        writer = csv.writer(spamemas_file)
        writer.writerow(['Phone', 'Message Time'])

        for indexx, deltaxd in enumerate(phlist, start=1):
            try:
                phone = utils.parse_phone(deltaxd)
                print(f'[{indexx}]: {phone}')
                client = TelegramClient(f"sessions/{phone}", api_id, api_hash)
                client.start(phone)
                client(UpdateStatusRequest(offline=False))

                async def main():
                    try:
                        entity = await client.get_entity(user)
                        messages = await client.get_messages(entity, limit=3)
                        for msg in messages:
                            if msg.text and "Congratulations! You've Won a Prize!" in msg.text:
                                msg_time = msg.date.astimezone(pytz.timezone("Asia/Tashkent")).strftime('%Y-%m-%d %H:%M:%S')
                                writer.writerow([phone, msg_time])
                                print(f"✅ {phone} - Yutdi: {msg_time}")
                                return
                        print(f"❌ {phone} - Yutmadi")
                    except Exception as e:
                        print(f"⚠️ {phone} - Xatolik: {e}")

                with client:
                    client.loop.run_until_complete(main())

            except Exception as e:
                print(f"🚫 {phone} - Umumiy xatolik: {e}")
                continue
else:
    print("@enshteyn40 ga murojaat qiling")
