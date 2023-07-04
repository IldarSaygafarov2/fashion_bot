from aiogram import types

from data.filters import IsAdmin
from data.loader import bot, dp
from keyboards import default as kb
from states.states import AdminMasterState, AdminMasterActionsState


@dp.message_handler(lambda msg: msg.text == "Мастер", IsAdmin())
async def admin_masters(message: types.Message):
    await AdminMasterState.start.set()
    await bot.send_message(message.from_user.id, "Выберите действие с мастерами", reply_markup=kb.admin_events_menu())


@dp.message_handler(IsAdmin(),
                    lambda msg: msg.text in ("Добавить", "Удалить", "Изменить"),
                    state=AdminMasterState.start)
async def masters_event(message: types.Message):
    if message.text.lower() == "добавить":
        await bot.send_message(
            message.from_user.id,
            "Напишите новое полное имя мастера",
            reply_markup=types.ReplyKeyboardRemove()
        )
        await AdminMasterActionsState.full_name.set()

    elif message.text.lower() == "удалить":
        await message.reply("Удалить мастера", reply_markup=kb.masters_menu())
        await AdminMasterState.delete.set()
    elif message.text.lower() == "изменить":
        await message.reply("Изменить мастера", reply_markup=kb.masters_menu())
        await AdminMasterState.update.set()

