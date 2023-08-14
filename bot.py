from requests import get
import asyncio
import logging
from aiogram import Bot, Dispatcher, types

from geopy.geocoders import Nominatim

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

@dp.message_handler(commands=['locate'])
async def location_info(message: types.Message):
    # Получить местоположение пользователя из ответа сервера
    user_location = message.text.split(',')[1].strip()
    
    # Отправить запрос к API геолокации
    response = await Nominatim.reverse('api_address', username=message.from_user.username, country=user_location)
    
    # Получить данные о местоположении пользователя
    address = await response.json()['address']
    latitude = response['lat']
    longitude = response['lng']
    
    # Отобразить местоположение пользователя в сообщении
    print('Местоположение пользователя: {}, {}'.format(latitude, longitude))



# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
