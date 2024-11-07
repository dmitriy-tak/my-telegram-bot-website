import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from flask import Flask, request
import os
import asyncio

API_TOKEN = 'your-telegram-bot-token'
WEBHOOK_URL = 'your-webhook-url'

# Создание приложения Flask
app = Flask(__name__)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создание объекта бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Асинхронная функция для обработки вебхуков
@app.route("/webhook", methods=["POST"])
async def webhook():
    json_str = request.get_data(as_text=True)
    update = types.Update.parse_raw(json_str)
    await dp.process_update(update)
    return "OK", 200

# Функция для установки вебхука
async def set_webhook():
    await bot.set_webhook(WEBHOOK_URL)

# Запуск приложения Flask
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(set_webhook())  # Устанавливаем вебхук при запуске
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))