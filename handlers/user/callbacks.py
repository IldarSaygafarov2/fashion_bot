from aiogram import types
from aiogram.dispatcher import FSMContext

from data.loader import bot, manager, dp
from keyboards import default as kb
from keyboards import inline as i_kb
from keyboards.calendar import SimpleCalendar
from keyboards.calendar import calendar_callback as simple_cal_callback
from states.states import ServiceState
from utils.main import get_photo


@dp.callback_query_handler(lambda call: "back" in call.data, state=ServiceState.cart)
async def back_home(callback: types.CallbackQuery, state: FSMContext):
    chat_id = callback.message.chat.id
    await state.finish()
    await bot.send_message(chat_id, "Выберите действие", reply_markup=kb.main_menu())


@dp.callback_query_handler(lambda call: "service" in call.data, state=ServiceState.cart)
async def add_to_cart(callback: types.CallbackQuery, state: FSMContext):
    chat_id = callback.message.chat.id

    async with state.proxy() as data:
        service_id = manager.service.get_service_id(data["service"])[0]

    masters = manager.master.get_masters(service_id=service_id)

    msg = """
Имя мастера: <b><i>{name}</i></b>
Информация: <b><i>{content}</i></b>
Стоимость услуг: <b><i>{price} сум</i></b>
    """
    await ServiceState.master.set()
    for master_id, name, content, photo, price in masters:
        await bot.send_photo(
            chat_id=chat_id,
            photo=get_photo("masters", photo),
            caption=msg.format(
                name=name,
                content=content,
                price=price
            ),
            parse_mode="HTML",
            reply_markup=i_kb.choose_master(master_id)
        )


@dp.callback_query_handler(lambda call: "master" in call.data, state=ServiceState.master)
async def get_master(callback: types.CallbackQuery, state: FSMContext):
    chat_id = callback.message.chat.id
    _, master_id = callback.data.split("_")
    async with state.proxy() as data:
        data["master"] = master_id

    await ServiceState.day.set()
    await bot.edit_message_reply_markup(
        chat_id,
        callback.message.message_id,
        reply_markup=await SimpleCalendar().start_calendar()
    )


@dp.callback_query_handler(simple_cal_callback.filter(), state=ServiceState.day)
async def process_simple_calendar(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        async with state.proxy() as data:
            data["day"] = date
            master_id = data['master']

            times = manager.work_time.get_master_time(master_id)

        master_full_name = manager.master.get_master_full_name(master_id)
        await ServiceState.time.set()
        await callback_query.message.answer(
            f'Свободное время мастера: {master_full_name[0]}',
            reply_markup=i_kb.master_work_time_menu(times)
        )


@dp.callback_query_handler(state=ServiceState.time)
async def get_time(callback: types.CallbackQuery, state: FSMContext):
    chat_id = callback.message.chat.id
    user_id = manager.user.is_user_exists(chat_id)
    async with state.proxy() as data:
        data["time"] = callback.data
        service_id = manager.service.get_service_id(data['service'])
        _, price, _ = manager.service.get_service_data(data['service'])
        master = data['master']
        date = data['day'].strftime("%d/%m/%Y")
        time = callback.data
        master_name = manager.master.get_master_full_name(master)

        msg = f"""
Вы выбрали:

Услуга: <b>{data['service']}</b>
Стоимость услуги: <b>{price} сум</b>
Мастер: <b>{master_name[0]}</b>
День: <b>{date}</b>
Время: <b>{time}</b>
"""
        await bot.send_message(chat_id, msg, parse_mode="HTML", reply_markup=i_kb.add_to_cart_menu(
            service_id=service_id,
            price=price,
            master_id=master,
            day=date,
            time=time,
            user_id=user_id
        ))

    await ServiceState.cart.set()


@dp.callback_query_handler(state=ServiceState.cart)
async def add_to_cart(callback: types.CallbackQuery, state: FSMContext):
    chat_id = callback.message.chat.id
    user_id = manager.user.is_user_exists(chat_id)[0]
    cart_id = manager.cart.get_cart_id(user_id)[0]

    async with state.proxy() as data:
        service_id = manager.service.get_service_id(data['service'])
        _, price, _ = manager.service.get_service_data(data['service'])
        master = data['master'][0]
        day = data['day'].strftime("%d/%m/%Y")
        time = data["time"]
        print(time)
        print(cart_id, service_id, master)
        manager.cart.update_cart(
            cart_id=cart_id,
            service_id=service_id[0],
            master_id=master,
            day=day,
            added_time=time,
            price=price
        )
        await callback.message.answer(
            "Успешно добавлено в корзину",
            reply_markup=kb.main_menu()
        )
        await state.finish()
