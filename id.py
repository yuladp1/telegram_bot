import asyncio
from telegram import Bot

TOKEN = '7811217825:AAFJB3VTyQ7jy6VNxzIj8LOOz9dMdhbhGX8'
bot = Bot(token=TOKEN)

async def main():
    updates = await bot.get_updates()
    print(f"Получено апдейтов: {len(updates)}")
    for update in updates:
        msg = update.message
        if msg:
            print("Message ID:", msg.message_id)
            print("Text:", msg.text)
            print("Attributes of message:")
            attrs = [a for a in dir(msg) if not a.startswith('_')]
            for attr in attrs:
                try:
                    value = getattr(msg, attr)
                    print(f"  {attr}: {value}")
                except Exception as e:
                    print(f"  {attr}: error getting value ({e})")
            print("------")

asyncio.run(main())
