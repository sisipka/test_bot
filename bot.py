from requests import get
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, BotCommand


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Объект бота
bot = Bot(token="TOKEN", parse_mode="HTML")  # TOKEN tellegramm bot

# Диспетчер
dp = Dispatcher(bot)

# Меню


# Создаем асинхронную функцию
async def set_main_menu(bot: Bot):

    # Создаем список с командами и их описанием для кнопки menu
    main_menu_commands = [
        BotCommand(command='/help',
                   description='Справка по работе бота'),
        BotCommand(command='/support',
                   description='Поддержка'),
        BotCommand(command='/contacts',
                   description='Другие способы связи'),
        BotCommand(command='/payments',
                   description='Платежи')]

    await bot.set_my_commands(main_menu_commands)

# Кнопки

# b1 = KeyboardButton('/start')
# b2 = KeyboardButton('/help')
# b3 = KeyboardButton('/ip')
# b4 = KeyboardButton('telephon', request_contact=True)
# b5 = KeyboardButton('locate', request_location=True)

# # Замещает обычную клавиатуру, на ту которую создаем
# kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

# kb_client.row(b1, b2, b3).row(b4, b5)

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
    await dp.startup.register(set_main_menu)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
