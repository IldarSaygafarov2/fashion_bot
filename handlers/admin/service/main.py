from aiogram import types

from data.filters import IsAdmin
from data.loader import bot, dp, manager
from keyboards import default as kb
from states.states import (AdminAddServiceState, AdminServiceState)


@dp.message_handler(lambda msg: msg.text == "Услуга", IsAdmin())
async def admin_service(message: types.Message):
    await AdminServiceState.start.set()
    await bot.send_message(message.from_user.id, "Выберите действие с услугами", reply_markup=kb.admin_events_menu())


@dp.message_handler(IsAdmin(),
                    lambda msg: msg.text in ("Добавить", "Удалить", "Изменить"),
                    state=AdminServiceState.start)
async def service_event(message: types.Message):
    services = manager.service.get_services_name()
    if message.text.lower() == "добавить":
        await bot.send_message(
            message.from_user.id,
            "Напишите название услуги"
        )
        await AdminAddServiceState.name.set()

    elif message.text.lower() == "удалить":
        await message.reply("Удалить услугу", reply_markup=kb.services_menu(services))
        await AdminServiceState.delete.set()
    elif message.text.lower() == "изменить":
        await message.reply("Изменить услугу", reply_markup=kb.services_menu(services))
        await AdminServiceState.update.set()

