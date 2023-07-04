from aiogram import types
from aiogram.dispatcher import FSMContext

from data.filters import IsAdmin
from data.loader import dp, manager
from keyboards import default as kb
from states.states import AdminCategoryState


@dp.message_handler(IsAdmin(), state=AdminCategoryState.update)
async def update_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["update"] = message.text

    await message.reply("Напишите новое название категории")
    await AdminCategoryState.update_2.set()


@dp.message_handler(IsAdmin(), state=AdminCategoryState.update_2)
async def update_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        category_id = manager.category.get_category_id(data["update"])

        manager.category.update_category(message.text, category_id)
        name = manager.category.get_category_name(category_id)

    await message.reply(f"Изменили категорию на {name}", reply_markup=kb.admin_main_menu())
    await state.finish()