Конечно! Вот исправленный код с учетом корректировок для асинхронного вызова set_webhook и использования правильного порта для запуска приложения:

`python
import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# Получаем токен из переменной окружения
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

app = Flask(name)

# Инициализируем бота и диспетчер
application = Application.builder().token(TOKEN).build()

# Обработчик команды /start
async def start(update: Update, context):
    await update.message.reply_text("Привет! Я твой Telegram-бот.")

# Обработчик всех текстовых сообщений
async def handle_message(update: Update, context):
    await update.message.reply_text(f"Ты сказал: {update.message.text}")

# Регистрируем обработчики
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT, handle_message))

# Webhook endpoint для получения обновлений от Telegram
@app.route(f'/{TOKEN}', methods=['POST'])
async def webhook():
    update = request.get_json()
    application.update_queue.put(update)
    return '', 200