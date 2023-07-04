from aiogram import types
from aiogram.dispatcher import FSMContext

from data.filters import IsAdmin
from data.loader import dp, manager
from keyboards import default as kb
from states.states import AdminCategoryState


@dp.message_handler(IsAdmin(), state=AdminCategoryState.add)
async def add_category(message: types.Message, state: FSMContext):
    manager.category.add_category(category_name=message.text)
    await message.reply(f"Категория: <b>{message.text}</b> успешно добавлена",
                        reply_markup=kb.admin_main_menu(),
                        parse_mode="HTML")
    await state.finish()
