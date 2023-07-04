from aiogram import types
from aiogram.dispatcher import FSMContext

from data.loader import bot, dp, manager
from keyboards import default as kb
from states.states import AdminMasterActionsState


@dp.message_handler(state=AdminMasterActionsState.full_name)
async def get_master_full_name(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    async with state.proxy() as data:
        data["full_name"] = message.text

    await AdminMasterActionsState.next()
    await bot.send_message(chat_id, "Напишите описание для этого мастера")


@dp.message_handler(state=AdminMasterActionsState.content)
async def get_master_content(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    async with state.proxy() as data:
        data["content"] = message.text

    await AdminMasterActionsState.next()
    await bot.send_message(chat_id, "Отправьте фотографию мастера")


@dp.message_handler(
    content_types=["document", "photo"], state=AdminMasterActionsState.photo
)
async def get_master_photo(message: types.Message, state: FSMContext):
    file = None

    if message.document:
        file = await bot.get_file(message.document.file_id)
    elif message.photo:
        file = await bot.get_file(message.photo[0].file_id)

    chat_id = message.chat.id
    file_name = file.file_path.split("/")[-1]

    img_io = await bot.download_file_by_id(file.file_id)

    with open(f"media/masters/{file_name}", mode="wb") as img:
        img.write(img_io.read())

    async with state.proxy() as data:
        data["photo"] = file_name

    await AdminMasterActionsState.next()

    await bot.send_message(
        chat_id, 'Напишите стоимость услуг данного мастера\nНапример: "150 000"'
    )


@dp.message_handler(state=AdminMasterActionsState.price)
async def get_master_price(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    price = int("".join(message.text.split(" ")))
    services = manager.service.get_services_name()

    async with state.proxy() as data:
        data["price"] = price
    await AdminMasterActionsState.next()
    await bot.send_message(
        chat_id,
        "Выберите услугу для данного мастера",
        reply_markup=kb.services_menu(services),
    )


@dp.message_handler(state=AdminMasterActionsState.service_id)
async def get_master_service(message: types.Message, state: FSMContext):
    chat_id = message.chat.id

    async with state.proxy() as data:
        full_name = data["full_name"]
        content = data["content"]
        photo = data["photo"]
        price = data["price"]

    service_id = manager.service.get_service_id(message.text)[0]

    # adding new master
    manager.master.add_master(
        full_name=full_name,
        content=content,
        photo=photo,
        price=price,
        service_id=service_id,
    )
    await state.finish()
    await bot.send_message(
        chat_id, "Успешно добавили нового мастера", reply_markup=kb.admin_main_menu()
    )
