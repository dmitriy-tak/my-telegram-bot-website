import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# Получаем токен из переменной окружения
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

app = Flask(__name__)

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
def webhook():
    update = request.get_json()
    print(f"Received update: {update}")  # Выводим обновления в лог
    application.update_queue.put(update)  # Отправляем обновление в очередь для обработки
    return '', 200

# Настройка Webhook
@app.route('/')
def set_webhook():
    # Замените 'your-domain.com' на адрес вашего развернутого сервера
    url = f'https://your-domain.com/{TOKEN}'
    bot = Bot(token=TOKEN)
    bot.set_webhook(url)
    return 'Webhook set!'

if __name__ == '__main__':
    app.run(port=5000)