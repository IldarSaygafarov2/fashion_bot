from aiogram import types
from aiogram.dispatcher import FSMContext

from data.filters import IsAdmin
from data.loader import bot, dp, manager
from keyboards import default as kb
from states.states import FAQActionState


@dp.message_handler(lambda msg: msg.text == "Вопросы-Ответы", IsAdmin())
async def admin_faq(message: types.Message):
    await FAQActionState.start.set()
    await bot.send_message(
        message.from_user.id,
        "Выберите действие с Q&A",
        reply_markup=kb.admin_events_menu(),
    )


@dp.message_handler(
    IsAdmin(),
    lambda msg: msg.text in ("Добавить", "Удалить", "Изменить"),
    state=FAQActionState.start,
)
async def masters_event(message: types.Message):
    if message.text.lower() == "добавить":
        await bot.send_message(
            message.from_user.id,
            "Напишите новый вопрос",
            reply_markup=types.ReplyKeyboardRemove(),
        )
        await FAQActionState.add_question.set()

    elif message.text.lower() == "удалить":
        await message.reply("Удалить вопрос-ответ", reply_markup=kb.faq_question_menu())
        await FAQActionState.delete.set()
    elif message.text.lower() == "изменить":
        await message.reply("Изменить вопрос-ответ", reply_markup=kb.faq_question_menu())
        await FAQActionState.update.set()



@dp.message_handler(state=FAQActionState.add_question)
async def add_new_question(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    async with state.proxy() as data:
        data["question"] = message.text

    await bot.send_message(chat_id, "Напишите ответ на ваш вопрос")
    await FAQActionState.add_answer.set()


@dp.message_handler(state=FAQActionState.add_answer)
async def add_new_answer(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    async with state.proxy() as data:
        question = data["question"]

    manager.faq.insert_question_answer(
        question=question,
        answer=message.text
    )
    await state.finish()
    await bot.send_message(chat_id, "Вопрос-ответ успешно добавлен", reply_markup=kb.admin_main_menu())


@dp.message_handler(state=FAQActionState.delete)
async def delete_question_answer(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    faq_id = manager.faq.get_faq_id(faq_question=message.text)
    manager.faq.delete_faq_question_answer(faq_id)
    await bot.send_message(chat_id, "Вопрос-ответ удален", reply_markup=kb.admin_main_menu())
    await state.finish()


@dp.message_handler(state=FAQActionState.update)
async def process_update_faq(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    faq_id = manager.faq.get_faq_id(faq_question=message.text)
    async with state.proxy() as data:
        data["faq_id"] = faq_id

    await FAQActionState.update_process.set()
    await bot.send_message(chat_id, f'Выберите действие над: {message.text}', reply_markup=kb.faq_events_menu())


@dp.message_handler(lambda msg: msg.text == "Изменить вопрос", state=FAQActionState.update_process)
async def process_updating_question(message: types.Message):
    chat_id = message.chat.id

    await FAQActionState.update_question.set()
    await bot.send_message(chat_id, "Напишите новый вопрос")


@dp.message_handler(state=FAQActionState.update_question)
async def update_question(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    async with state.proxy() as data:
        faq_id = data["faq_id"]

    manager.faq.update_question(
        faq_id=faq_id,
        new_question=message.text
    )
    await bot.send_message(chat_id, "Вопрос успешно изменен", reply_markup=kb.admin_main_menu())
    await state.finish()


@dp.message_handler(lambda msg: msg.text == "Изменить ответ", state=FAQActionState.update_process)
async def process_updating_question(message: types.Message):
    chat_id = message.chat.id

    await FAQActionState.update_answer.set()
    await bot.send_message(chat_id, "Напишите новый ответ")


@dp.message_handler(state=FAQActionState.update_answer)
async def update_question(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    async with state.proxy() as data:
        faq_id = data["faq_id"]

    manager.faq.update_answer(
        faq_id=faq_id,
        new_answer=message.text
    )
    await bot.send_message(chat_id, "Ответ успешно изменен", reply_markup=kb.admin_main_menu())
    await state.finish()
