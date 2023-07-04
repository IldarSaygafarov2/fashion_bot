from aiogram import types
from aiogram.dispatcher import FSMContext

from data.filters import IsAdmin
from data.loader import dp, manager
from keyboards import default as kb
from states.states import AdminCategoryState


@dp.message_handler(IsAdmin(), state=AdminCategoryState.delete)
async def delete_category(message: types.Message, state: FSMContext):
    manager.category.delete_category(message.text)
    await message.reply(f"Категория {message.text} успешно удалена", reply_markup=kb.admin_main_menu())
    await state.finish()

