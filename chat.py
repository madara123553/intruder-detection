import logging
from telegram import Bot

# Enable logging
logging.basicConfig(level=logging.DEBUG)

# === Configuration ===
TELEGRAM_BOT_TOKEN = '7611195557:'

# === Initialize Telegram Bot ===
bot = Bot(token=TELEGRAM_BOT_TOKEN)

async def get_chat_id():
    try:
        updates = await bot.get_updates()
        for update in updates:
            print(f"Chat ID: {update.message.chat.id}")
    except Exception as e:
        print(f"Error: {e}")

# Run the async function
import asyncio
asyncio.run(get_chat_id())
