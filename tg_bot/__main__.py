import logging
from aiogram import Bot, Dispatcher, types
import asyncio
import aiohttp


API_TOKEN = '7695782071:AAFwirT7ujIUPi1mKgNf6a4vPHboceRWdqs'

if not API_TOKEN:
    raise ValueError("Необходимо установить переменную окружения BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


async def fetch_text_from_yandex(query: str):
    url = 'http://localhost:1337/question'
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json={'question': query}) as response:
            if response.status == 200:
                json_answer = await response.json()
                return json_answer
            else:
                return "Ошибка при получении данных"


@dp.message(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Отправь мне любое сообщение, и я отправлю его на Яндекс.")


@dp.message()
async def process_message(message: types.Message):
    query = message.text
    result = await fetch_text_from_yandex(query)
    print(result['metadatas'][0])
    await message.reply(f"{result['metadatas'][0][5:]}")


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
