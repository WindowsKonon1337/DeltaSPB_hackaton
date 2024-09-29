import asyncio
import logging

import aiohttp
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command

API_TOKEN = '7695782071:AAFwirT7ujIUPi1mKgNf6a4vPHboceRWdqs'

if not API_TOKEN:
    raise ValueError("Необходимо установить переменную окружения BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


async def get_llm_answer(query: str):
    url = 'http://search_engine:1337/predict'
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json={'question': query}) as response:
            if response.status == 200:
                json_answer = await response.json()
                return json_answer
            else:
                return "Ошибка при получении данных"


@dp.message()
async def process_message(message: types.Message):
    query = message.text
    if query == '/start':
        await message.answer('Привет! я бот технической поддержки RuTube! Пришли мне сообщение и я помогу тебе ответить на него!.')
        return
    result = await get_llm_answer(query)
    await message.answer(f'```json\n{result}\n```', parse_mode='markdown')


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
