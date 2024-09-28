
!pip install -m aiogram==2.8
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor

   
API_TOKEN = '7695782071:AAFwirT7ujIUPi1mKgNf6a4vPHboceRWdqs'

   
logging.basicConfig(level=logging.INFO)

   
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

async def process_message_text(text: str):
       
    print(f"Обработанный текст: {text}")

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Отправь мне любое сообщение, и я его обработаю.")

@dp.message_handler()
async def echo(message: types.Message):
       # Передаем текст сообщения в функцию для обработки
    await process_message_text(message.text)
       # Отправляем ответ пользователю
    await message.reply("Ваше сообщение было обработано.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
   
