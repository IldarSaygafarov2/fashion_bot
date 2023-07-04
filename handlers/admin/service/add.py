from aiogram import types
from aiogram.dispatcher import FSMContext

from data.loader import bot, dp, manager
from keyboards import default as kb
from states.states import AdminAddServiceState


@dp.message_handler(state=AdminAddServiceState.name)
async def get_service_name(message: types.Message, state: FSMContext):
    chat_id = message.chat.id

    await bot.send_message(chat_id, "Напишите описание для услуги")
    await AdminAddServiceState.content.set()
    async with state.proxy() as data:
        data["name"] = message.text


@dp.message_handler(state=AdminAddServiceState.content)
async def get_service_content(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    await bot.send_message(chat_id, "Напишите стоимость услуги, например '300 000' ")
    await AdminAddServiceState.price.set()
    async with state.proxy() as data:
        data["content"] = message.text


@dp.message_handler(state=AdminAddServiceState.price)
async def get_service_price(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    price = int("".join(message.text.split(" ")))

    await bot.send_message(chat_id, "Отправьте фотографию услуги")
    await AdminAddServiceState.photo.set()

    async with state.proxy() as data:
        data["price"] = price


@dp.message_handler(
    state=AdminAddServiceState.photo, content_types=["document", "photo"]
)
async def get_service_photo(message: types.Message, state: FSMContext):
    file = None

    if message.document:
        file = await bot.get_file(message.document.file_id)
    elif message.photo:
        file = await bot.get_file(message.photo[0].file_id)

    chat_id = message.chat.id
    file_name = file.file_path.split("/")[-1]

    await bot.send_message(
        chat_id, "Выберите категорию для услуги", reply_markup=kb.categories_menu()
    )
    img_io = await bot.download_file_by_id(file.file_id)

    with open(f"media/services/photos/{file_name}", mode="wb") as img:
        img.write(img_io.read())

    await AdminAddServiceState.category.set()
    async with state.proxy() as data:
        data["photo"] = file_name


@dp.message_handler(state=AdminAddServiceState.category)
async def get_service_category(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    category_id = manager.category.get_category_id(message.text)

    async with state.proxy() as data:
        name = data["name"]
        content = data["content"]
        price = data["price"]
        photo = data["photo"]
        manager.service.add_service(
            name=name,
            content=content,
            price=int(price),
            photo=photo,
            category_id=category_id,
        )

        with open(f"media/services/photos/{photo}", "rb") as file:
            photo_bytes = file.read()

        msg = f"""
Добавили услугу:

<i>{name}</i>
<i>{content}</i>

Стоимость: <b>{price}</b> сум
"""
        await bot.send_photo(
            chat_id,
            photo=photo_bytes,
            caption=msg,
            parse_mode="HTML",
            reply_markup=kb.admin_main_menu(),
        )

    await state.finish()
