import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

# Telegram bot token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is not set in .env file")
