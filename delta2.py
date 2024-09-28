import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
import aiohttp


API_TOKEN = '7695782071:AAFwirT7ujIUPi1mKgNf6a4vPHboceRWdqs'

if not API_TOKEN:
    raise ValueError("Необходимо установить переменную окружения BOT_TOKEN")

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

async def fetch_text_from_yandex(query: str):
    url = f"https://yandex.ru/search/?text={query}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                html = await response.text()
                # Здесь вы можете использовать парсер HTML, чтобы извлечь нужный текст
                # Для упрощения примера просто возвращаем первые 20 символов HTML
                return html[600:1000]
            else:
                return "Ошибка при получении данных"
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Отправь мне любое сообщение, и я отправлю его на Яндекс.")
@dp.message_handler()
async def process_message(message: types.Message):
    query = message.text
    result = await fetch_text_from_yandex(query)
    await message.reply(f"Первые 20 символов ответа: {result}")
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
