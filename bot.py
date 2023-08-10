from requests import get
import asyncio
import logging
from aiogram import Bot, Dispatcher, types


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Объект бота
bot = Bot(token="TOKEN")  # TOKEN tellegramm bot

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

# Приветствие новых пользователей


@dp.message(F.new_chat_members)
async def somebody_added(message: types.Message):
    for user in message.new_chat_members:
        # проперти full_name берёт сразу имя И фамилию
        # (на скриншоте выше у юзеров нет фамилии)
        await message.reply(f"Привет, {user.full_name}")

# Хэндлер на команду /ip


@dp.message_handler(commands=['ip'])
async def send_ip(msg: types.Message):
    await msg.answer(get('https://api.ipify.org').text)


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

if __name__ == "__main__":
    asyncio.run(main())
