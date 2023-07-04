from aiogram import types

from data.loader import bot, dp, manager
from keyboards import default as kb
from states.states import AdminMasterState


@dp.message_handler(state=AdminMasterState.delete)
async def delete_master(message: types.Message) -> None:
    chat_id = message.chat.id
    master_id = manager.master.get_master_id(master_name=message.text)
    manager.master.delete_master(master_id)
    await bot.send_message(
        chat_id, "Мастер успешно удален", reply_markup=kb.admin_main_menu()
    )
