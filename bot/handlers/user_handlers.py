from copy import deepcopy

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from lexicon.lexicon import LEXICON
from db.sqlite import db_start, create_profile, edit_profile

router = Router()


# Этот хэндлер будет срабатывать на команду "/start" -
# добавлять пользователя в базу данных, если его там еще не было
# и отправлять ему приветственное сообщение
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON[message.text])


@router.message(CommandHelp())
async def process_help_command(message: Message):
    await message.answer(f"Ваш ID: {message.from_user.id}")

# # Этот хэндлер будет срабатывать на команду "/help"
# # и отправлять пользователю сообщение со списком доступных команд в боте
# @router.message(Command(commands='help'))
# async def process_help_command(message: Message):
#     await message.answer(LEXICON[message.text])


# # Этот хэндлер будет срабатывать на команду "/beginning"
# # и отправлять пользователю первую страницу книги с кнопками пагинации
# @router.message(Command(commands='beginning'))
# async def process_beginning_command(message: Message):
#     users_db[message.from_user.id]['page'] = 1
#     text = book[users_db[message.from_user.id]['page']]
#     await message.answer(
#         text=text,
#         reply_markup=create_pagination_keyboard(
#             'backward',
#             f'{users_db[message.from_user.id]["page"]}/{len(book)}',
#             'forward'
#         )
#     )


# # Этот хэндлер будет срабатывать на команду "/continue"
# # и отправлять пользователю страницу книги, на которой пользователь
# # остановился в процессе взаимодействия с ботом
# @router.message(Command(commands='continue'))
# async def process_continue_command(message: Message):
#     text = book[users_db[message.from_user.id]['page']]
#     await message.answer(
#         text=text,
#         reply_markup=create_pagination_keyboard(
#             'backward',
#             f'{users_db[message.from_user.id]["page"]}/{len(book)}',
#             'forward'
#         )
#     )


# # Этот хэндлер будет срабатывать на команду "/bookmarks"
# # и отправлять пользователю список сохраненных закладок,
# # если они есть или сообщение о том, что закладок нет
# @router.message(Command(commands='bookmarks'))
# async def process_bookmarks_command(message: Message):
#     if users_db[message.from_user.id]["bookmarks"]:
#         await message.answer(
#             text=LEXICON[message.text],
#             reply_markup=create_bookmarks_keyboard(
#                 *users_db[message.from_user.id]["bookmarks"]
#             )
#         )
#     else:
#         await message.answer(text=LEXICON['no_bookmarks'])


# # Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# # "отменить" во время работы со списком закладок (просмотр и редактирование)
# @router.callback_query(F.data == 'cancel')
# async def process_cancel_press(callback: CallbackQuery):
#     await callback.message.edit_text(text=LEXICON['cancel_text'])
#     await callback.answer()
