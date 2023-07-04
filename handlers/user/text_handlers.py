from aiogram import types
from aiogram.dispatcher import FSMContext

from data.loader import bot, dp, manager
from keyboards import default as kb
from keyboards import inline as i_kb
from states.states import RegistrationState, ServiceState

from .commands import start


@dp.message_handler(lambda msg: msg.text == "Регистрация")
async def react_to_registration(message: types.Message) -> None:
    await RegistrationState.username.set()
    await message.reply("Напишите ваше имя")


@dp.message_handler(state=RegistrationState.username)
async def react_to_number(message: types.Message, state: FSMContext) -> None:
    await message.reply("Отправьте ваш номер", reply_markup=kb.phone_number_button())

    async with state.proxy() as data:
        data["username"] = message.text

    await RegistrationState.phone_number.set()


@dp.message_handler(state=RegistrationState.phone_number, content_types=["contact"])
async def react_to_number(message: types.Message, state: FSMContext) -> None:
    chat_id = message.from_user.id

    async with state.proxy() as data:
        data["phone_number"] = message.contact.phone_number

        manager.user.add_user(
            username=data["username"],
            phone_number=data["phone_number"],
            telegram_id=chat_id,
        )
        user_id = manager.user.is_user_exists(chat_id)
        manager.cart.add_user_id(user_id[0])

    await bot.send_message(
        message.from_user.id,
        text="Регистрация прошла успешно, приятного использования",
        reply_markup=kb.main_menu(),
    )
    await state.finish()


@dp.message_handler(lambda msg: msg.text == "Услуги")
async def get_categories(message: types.Message) -> None:
    chat_id = message.from_user.id

    await bot.send_message(
        chat_id, "Выберите категорию услуги", reply_markup=kb.categories_menu()
    )


@dp.message_handler(
    lambda msg: msg.text.title() in manager.category.format_categories()
)
async def get_category_service(message: types.Message) -> None:
    chat_id = message.from_user.id
    category_id = manager.category.get_category_id(message.text)
    services = manager.service.get_services_name(category_id)
    await ServiceState.service.set()

    await bot.send_message(
        chat_id,
        f"Выберите сервис категории: <b>{message.text}</b>",
        reply_markup=kb.services_menu(services),
        parse_mode="HTML",
    )


@dp.message_handler(state=ServiceState.service)
async def get_service_data(message: types.Message, state: FSMContext) -> None:
    chat_id = message.from_user.id
    async with state.proxy() as data:
        data["service"] = message.text
    service_id = manager.service.get_service_id(service_name=message.text)

    content, price, photo = manager.service.get_service_data(message.text)
    with open(f"media/services/photos/{photo}", mode="rb") as file:
        photo_bytes = file.read()

    msg = f"""
<i>{content}</i>

Стоимость: <b>{price}</b> сум
"""
    await bot.send_photo(
        chat_id,
        photo=photo_bytes,
        caption=msg,
        parse_mode="HTML",
        reply_markup=i_kb.to_cart_menu(service_id[0]),
    )
    await ServiceState.cart.set()


@dp.message_handler(lambda msg: msg.text == "Корзина")
async def show_cart(message: types.Message) -> None:
    chat_id = message.chat.id
    user_id = manager.user.is_user_exists(chat_id)[0]

    if not user_id:
        bot.send_message(chat_id, "Что-то пошло не так...")
        await start(message)

    total_price = manager.cart.get_total_price(user_id)
    cart_products = manager.cart.get_cart_info(user_id)
    msg = "Ваша корзина \n\n"
    count = 0
    for service_id, master_id, day, time, price in cart_products:
        count += 1
        service = manager.service.get_service_name_by_id(service_id)
        master = manager.master.get_master_full_name(master_id)

        msg += f"""
{count}.
Услуга: <b>{service[0]}</b>
Стоимость услуги: <b>{price} сум</b>
Мастер: <b>{master[0]}</b>
День: <b>{day}</b>
Время: <b>{time}</b>\n
"""

    msg += f"""
Общая стоимость услуг: <b>{total_price[0]} сум</b>    
"""
    await bot.send_message(chat_id, msg, parse_mode="HTML")


@dp.message_handler(lambda msg: msg.text == "Q&A")
async def get_questions(message: types.Message) -> None:
    chat_id = message.chat.id
    questions = manager.faq.get_all_questions()
    message_text = ""

    for index, item in enumerate(questions, start=1):
        message_text += f"""
{index}. {item[1]}

{item[2]}
"""

    await bot.send_message(chat_id, message_text)
