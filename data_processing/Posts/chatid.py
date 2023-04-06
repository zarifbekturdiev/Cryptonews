import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv
from telegram import Bot

BASE_DIR = Path(__file__).parent.parent.parent
load_dotenv(BASE_DIR / '.env')


async def main():
    TOKEN = os.getenv('TELEGRAM_TOKEN')
    bot = Bot(token=TOKEN)
    updates = await bot.get_updates()
    chat_id = updates[-1].message.chat_id
    print(chat_id)


asyncio.run(main())
