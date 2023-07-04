from aiogram import types
from aiogram.dispatcher import FSMContext

from data import configs as conf
from data.filters import IsAdmin
from data.loader import bot, dp, manager, update_manager
from handlers.user.commands import admin_start
from keyboards import default as kb
from keyboards import inline as i_kb
from states.states import AdminServiceState, AdminUpdateServiceState
from utils.main import combine_fields


@dp.message_handler(IsAdmin(), state=AdminServiceState.update)
async def update_service(message: types.Message) -> None:
    chat_id = message.chat.id
    service_id = manager.service.get_service_id(message.text)
    columns = manager.base.get_table_columns_names("service")
    columns = [item for item in columns if item != "service_id"]

    fields = combine_fields(columns, conf.SERVICE_FIELDS_NAMES)
    await AdminUpdateServiceState.service_id.set()

    await bot.send_message(
        chat_id,
        "Какое из приведенных ниже полей, вы хотите изменить?",
        reply_markup=i_kb.service_fields_menu(fields, service_id[0]),
    )


@dp.callback_query_handler(
    lambda call: call.data.startswith("edit"), state=AdminUpdateServiceState.service_id
)
async def handle_field_for_update(call: types.CallbackQuery, state: FSMContext) -> None:
    _, field_name, service_id = call.data.split("-")

    async with state.proxy() as data:
        data["service_id"] = service_id

    if field_name == "content":
        await AdminUpdateServiceState.content.set()
        await call.message.answer("Напишите новое описание для услуги")

    elif field_name == "name":
        await AdminUpdateServiceState.name.set()
        await call.message.answer("Напишите новое название для услуги")
    elif field_name == "photo":
        await AdminUpdateServiceState.photo.set()
        await call.message.answer("Отправьте новую фотку для услуги")
        # await edit_service_photo(call)
    elif field_name == "category_id":
        await AdminUpdateServiceState.category.set()
        await call.message.answer(
            "Выберите новую категорию для услуги", reply_markup=kb.categories_menu()
        )
    elif field_name == "price":
        await AdminUpdateServiceState.price.set()
        await call.message.answer("Напишите новую цену для услуги. Например '150 000' ")


@dp.message_handler(state=AdminUpdateServiceState.content)
async def edit_service_content_proceed(
    message: types.Message, state: FSMContext
) -> None:
    chat_id = message.chat.id

    async with state.proxy() as data:
        service_id = data["service_id"]

    # обновляем поле content
    update_manager.service.update_service_content(
        service_id=service_id, service_content=message.text
    )
    await state.finish()
    await bot.send_message(chat_id, "Описание успешно изменено")
    await admin_start(message)


@dp.message_handler(state=AdminUpdateServiceState.name)
async def edit_service_name(message: types.Message, state: FSMContext) -> None:
    chat_id = message.chat.id

    async with state.proxy() as data:
        service_id = data["service_id"]

    update_manager.service.update_service_name(
        service_id=service_id, service_name=message.text
    )
    await state.finish()
    await bot.send_message(chat_id, "Название успешно изменено")
    await admin_start(message)


@dp.message_handler(state=AdminUpdateServiceState.price)
async def edit_service_price(message: types.Message, state: FSMContext) -> None:
    chat_id = message.chat.id
    price = int("".join(message.text.split(" ")))
    async with state.proxy() as data:
        service_id = data["service_id"]

    update_manager.service.update_service_price(
        service_id=service_id, service_price=price
    )
    await state.finish()
    await bot.send_message(chat_id, "Цена успешно изменена")
    await admin_start(message)


@dp.message_handler(
    state=AdminUpdateServiceState.photo, content_types=["document", "photo"]
)
async def edit_service_photo(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        service_id = data["service_id"]

    file = None

    if message.document:
        file = await bot.get_file(message.document.file_id)
    elif message.photo:
        file = await bot.get_file(message.photo[0].file_id)

    chat_id = message.chat.id
    file_name = file.file_path.split("/")[-1]

    img_io = await bot.download_file_by_id(file.file_id)

    with open(f"media/services/photos/{file_name}", mode="wb") as img:
        img.write(img_io.read())

    update_manager.service.update_service_photo(service_id, file_name)
    await state.finish()
    await bot.send_message(chat_id, "Фотография успешно изменена")
    await admin_start(message)


@dp.message_handler(state=AdminUpdateServiceState.category)
async def edit_service_category(message: types.Message, state: FSMContext) -> None:
    chat_id = message.chat.id
    async with state.proxy() as data:
        service_id = data["service_id"]
    category_id = manager.category.get_category_id(message.text)
    update_manager.service.update_service_category_id(service_id, category_id)
    await state.finish()
    await bot.send_message(chat_id, "Категория успешно изменена")
    await admin_start(message)
