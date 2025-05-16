from telegram import Bot

# === Configuration ===
TELEGRAM_BOT_TOKEN = '761119555'

# === Initialize Telegram Bot ===
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Get updates and print chat IDs
updates = bot.get_updates()

for update in updates:
    print(f"Chat ID: {update.message.chat.id}")
    print(f"Message: {update.message.text}")
