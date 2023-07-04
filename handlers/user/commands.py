from aiogram import types

from data.configs import ADMIN_LIST
from data.loader import bot, dp, manager
from keyboards import default as kb


@dp.message_handler(commands=["admin"])
async def admin_start(message: types.Message):
    if message.chat.id in ADMIN_LIST:
        await message.reply("Выберите действие", reply_markup=kb.admin_main_menu())
    else:
        await message.reply("У вас нет прав для этой команды", reply_markup=kb.main_menu())



@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    chat_id = message.from_user.id
    if not manager.user.is_user_exists(telegram_id=chat_id):
        await bot.send_message(message.from_user.id, text='Пройдите регистрацию', reply_markup=kb.registration_button())
        return
    await bot.send_message(message.from_user.id, text='Добро пожаловать', reply_markup=kb.main_menu())


