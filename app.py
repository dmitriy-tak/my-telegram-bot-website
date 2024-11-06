import os
from flask import Flask, request
from telegram import Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# Получаем токен из переменной окружения
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

app = Flask(__name__)

# Инициализируем бота
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, update_queue=None)

# Обработчик команды /start
def start(update, context):
    update.message.reply_text("Привет! Я твой Telegram-бот.")

# Обработчик всех текстовых сообщений
def handle_message(update, context):
    update.message.reply_text(f"Ты сказал: {update.message.text}")

# Регистрируем обработчики
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text, handle_message))

# Webhook endpoint для получения обновлений от Telegram
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = request.get_json()
    dispatcher.process_update(update)
    return '', 200

# Настройка Webhook
@app.route('/')
def set_webhook():
    # Замените 'your-domain.com' на адрес вашего развернутого сервера
    url = f'https://{os.getenv("RENDER_EXTERNAL_URL")}/{TOKEN}'
    bot.set_webhook(url)
    return 'Webhook set!'

if __name__ == '__main__':
    app.run(debug=True)