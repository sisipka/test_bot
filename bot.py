from requests import get
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Объект бота
bot = Bot(token="TOKEN", parse_mode="HTML")  # TOKEN tellegramm bot

# Диспетчер
dp = Dispatcher(bot)

# Кнопки

b1 = KeyboardButton('/start')
b2 = KeyboardButton('/ip')
b3 = KeyboardButton('/locate')

# Замещает обычную клавиатуру, на ту которую создаем
kb_client = ReplyKeyboardMarkup(resize_keyboard)

kb_client.add(b1).row(b2, b3)

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
    else:
        await msg.answer('Не понимаю, что это значит.')


# test


# Запуск процесса поллинга новых апдейтов


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
