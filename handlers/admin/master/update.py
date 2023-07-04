from aiogram import types
from aiogram.dispatcher import FSMContext

from data import configs as conf
from data.filters import IsAdmin
from data.loader import bot, dp, manager, update_manager
from keyboards import default as kb
from keyboards import inline as i_kb
from states.states import AdminMasterActionsState, AdminMasterState
from utils.main import combine_fields
from handlers.user.commands import admin_start


@dp.message_handler(state=AdminMasterState.update)
async def get_master_to_update(message: types.Message, state: FSMContext) -> None:
    chat_id = message.chat.id

    # getting master_id my master name
    master_id = manager.master.get_master_id(master_name=message.text)

    # all columns from master table
    columns = manager.base.format_table_columns_names(
        table_name="master", excluded_columns=["master_id", "is_working"]
    )

    fields = combine_fields(columns, conf.MASTER_FIELDS_NAMES)
    await AdminMasterActionsState.service_id.set()

    await bot.send_message(
        chat_id,
        "Какое из приведенных ниже полей, вы хотите изменить?",
        reply_markup=i_kb.service_fields_menu(fields, master_id),
    )


@dp.callback_query_handler(
    lambda call: call.data.startswith("edit"), state=AdminMasterActionsState.service_id
)
async def handle_fields_for_update(
    call: types.CallbackQuery, state: FSMContext
) -> None:
    _, field, master_id = call.data.split("-")

    async with state.proxy() as data:
        data["master_id"] = master_id

    if field == "content":
        await AdminMasterActionsState.content.set()
        await call.message.answer("Напишите новое описане работы мастера")
    elif field == "full_name":
        await AdminMasterActionsState.full_name.set()
        await call.message.answer("Напишите новое полное имя работы мастера")
    elif field == "photo":
        await AdminMasterActionsState.photo.set()
        await call.message.answer("Отправьте новую фотку для мастера")
    elif field == "service_id":
        await AdminMasterActionsState.service_id.set()
        await call.message.answer(
            "Выберите новую услугу для мастера", reply_markup=kb.categories_menu()
        )
    elif field == "price":
        await AdminMasterActionsState.price.set()
        await call.message.answer(
            "Напишите новую цену для услуг мастера. Например '150 000' "
        )


@dp.message_handler(state=AdminMasterActionsState.content, content_types=["text"])
async def get_new_master_content(message: types.Message, state: FSMContext) -> None:
    chat_id = message.chat.id

    async with state.proxy() as data:
        master_id = data["master_id"]

    update_manager.master.update_master_content(
        master_id=master_id, new_content=message.text
    )

    await state.finish()
    await bot.send_message(chat_id, "Описание мастера успешно изменено")
    await admin_start(message)


@dp.message_handler(state=AdminMasterActionsState.full_name, content_types=["text"])
async def get_new_master_full_name(message: types.Message, state: FSMContext) -> None:
    chat_id = message.chat.id

    async with state.proxy() as data:
        master_id = data["master_id"]

    update_manager.master.update_master_full_name(
        master_id=master_id, new_full_name=message.text
    )

    await state.finish()
    await bot.send_message(chat_id, "Имя мастера успешно изменено")
    await admin_start(message)


@dp.message_handler(
    state=AdminMasterActionsState.photo, content_types=["document", "photo"]
)
async def get_new_master_photo(message: types.Message, state: FSMContext) -> None:
    chat_id = message.chat.id

    async with state.proxy() as data:
        master_id = data["master_id"]

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

    # updating photo file name in db
    update_manager.master.update_master_photo(master_id=master_id, new_photo=file_name)

    await state.finish()
    await bot.send_message(chat_id, "Фотография успешно изменена")
    await admin_start(message)


@dp.message_handler(state=AdminMasterActionsState.service_id, content_types=["text"])
async def get_new_master_service(message: types.Message, state: FSMContext) -> None:
    chat_id = message.chat.id
    service_id = manager.service.get_service_id(service_name=message.text)

    async with state.proxy() as data:
        master_id = data["master_id"]

    update_manager.master.update_master_service(
        master_id=master_id, new_service_id=service_id
    )
    await state.finish()
    await bot.send_message(chat_id, "Услуга успешно изменена")
    await admin_start(message)


@dp.message_handler(state=AdminMasterActionsState.price, content_types=["text"])
async def get_new_master_price(message: types.Message, state: FSMContext) -> None:
    chat_id = message.chat.id
    price = int("".join(message.text.split(" ")))

    async with state.proxy() as data:
        master_id = data["master_id"]

    update_manager.master.update_master_price(master_id=master_id, new_price=price)

    await state.finish()
    await bot.send_message(chat_id, "Цена успешно изменена")
    await admin_start(message)
