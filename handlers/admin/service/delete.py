from aiogram import types
from aiogram.dispatcher import FSMContext

from data.filters import IsAdmin
from data.loader import bot, dp, update_manager
from handlers.user.commands import admin_start
from states.states import (AdminServiceState)


@dp.message_handler(IsAdmin(), state=AdminServiceState.delete)
async def delete_service(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    update_manager.service.delete_service(message.text)

    await state.finish()
    await bot.send_message(chat_id, 'Услуша успешно удалена')
    await admin_start(message)


