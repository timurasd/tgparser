import asyncio
import csv
from telethon import TelegramClient

api_id = "<API_ID>"
api_hash = '<API_HASH>'
dialog_name = "<CHAT_NAME>"
text = ["keywords", "to", "search", "goes", "here"]

async def main():

    async with TelegramClient('anon', api_id, api_hash) as client:
        dialogs = await client.get_dialogs()
        dialog = None
        for d in dialogs:
            if dialog_name in d.name:
                dialog = d

        if dialog == None:
            print("try different dialog name")
            exit(1)

        print("Found chat")
        message_count = 1
        total = 8000
        with open("scrap.csv", 'w+', newline='') as f:
            print("Searching for messages")
            async for message in client.iter_messages(dialog):
                if message.message is None:
                    continue
                if not text in message.message:
                    continue
                user = await client.get_entity(message.from_id)
                writer = csv.writer(f, delimiter='\t')
                message = message.message.replace("\n", " ")
                writer.writerow([
                    f"{user.first_name} {user.last_name}",
                    f"@{user.username}",
                    f"{message}"
                    ])
                print(f"{user.first_name} {user.last_name}")
                print(f"{message_count} / {total} {message_count/total}")
                message_count += 1

if __name__ ==  '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
