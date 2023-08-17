from requests import get
import asyncio
import logging
from aiogram import Bot, Dispatcher, executor, types, utils, filters
from aiogram.filters import Command


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Объект бота
bot = Bot(token="TOKEN", parse_mode="HTML")  # TOKEN tellegramm bot

# Диспетчер
dp = Dispatcher(bot)

# Хэндлер на команду /start


@dp.message_handler(commands=['start'])
async def send_welcome(msg: types.Message):
    await msg.answer(f'Я бот. Приятно познакомиться, {msg.from_user.first_name}')

# Хэндлер на команду /help


@dp.message_handler(commands=['help'])
async def send_help(msg: types.Message):
    await msg.reply('Я бот. Создан для тестов и экспериментов')

# Хэндлер на команду /ip


@dp.message_handler(commands=['ip'])
async def send_ip(msg: types.Message):
    await msg.answer(get('https://api.ipify.org').text)

# Хэндлер Привет


@dp.message_handler(content_types=['text'])
async def get_text_messages(msg: types.Message):
    if msg.text.lower() == 'привет':
        await msg.answer('Привет!')
    elif msg.text.lower() == 'myip':
        await msg.answer(get('https://api.ipify.org').text)
    else:
        await msg.answer('Не понимаю, что это значит.')


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

# test


@dp.message(Command("test"))
async def any_message(message: types.Message):
    await message.answer("Hello, <b>world</b>!", parse_mode="HTML")
    await message.answer("Hello, *world*\!", parse_mode="MarkdownV2")


if __name__ == "__main__":
    asyncio.run(main())
