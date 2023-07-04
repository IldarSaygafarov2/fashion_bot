from aiogram import types

from data.filters import IsAdmin
from data.loader import dp, bot
from keyboards import default as kb
from states.states import AdminCategoryState


@dp.message_handler(lambda msg: msg.text == "Категория", IsAdmin())
async def admin_category(message: types.Message):
    await bot.send_message(message.from_user.id, "Выберите действие с категориями", reply_markup=kb.admin_events_menu())


@dp.message_handler(IsAdmin(), lambda msg: msg.text in ("Добавить", "Удалить", "Изменить"))
async def category_event(message: types.Message):
    if message.text.lower() == "добавить":
        await bot.send_message(
            message.from_user.id,
            "Напишите название новой категории"
        )
        await AdminCategoryState.add.set()
    elif message.text.lower() == "удалить":
        await message.reply("удалить категорию", reply_markup=kb.categories_menu())
        await AdminCategoryState.delete.set()
    elif message.text.lower() == "изменить":
        await message.reply("изменить категорию", reply_markup=kb.categories_menu())
        await AdminCategoryState.update.set()
