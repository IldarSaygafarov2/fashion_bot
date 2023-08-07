from typing import Optional

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from data.loader import manager


def masters_menu() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    masters = manager.master.get_all_masters()
    buttons = [KeyboardButton(text=master[0]) for master in masters]
    markup.add(*buttons)
    return markup


def registration_button() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton(text="Регистрация")
    markup.add(btn)
    return markup


def phone_number_button() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton(text="Номер телефона", request_contact=True)
    markup.add(btn)
    return markup


def main_menu() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        *[
            KeyboardButton(text="Услуги"),
            KeyboardButton(text="Q&A"),
            KeyboardButton(text="Корзина"),
        ]
    )
    return markup


def categories_menu() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    categories = [category[0] for category in manager.category.get_categories()]
    markup.add(*[KeyboardButton(text=category) for category in categories])
    return markup


def services_menu(services: Optional[list[tuple]] = None) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

    services = [service[0] for service in services]
    markup.add(*[KeyboardButton(text=service) for service in services])
    return markup


def back_menu() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        *[
            KeyboardButton(text="Назад"),
        ]
    )
    return markup


def admin_main_menu() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        *[
            KeyboardButton(text="Категория"),
            KeyboardButton(text="Услуга"),
            KeyboardButton(text="Мастер"),
            KeyboardButton(text="Вопросы-Ответы"),
        ]
    )
    return markup


def admin_events_menu() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(
        *[
            KeyboardButton(text="Добавить"),
            KeyboardButton(text="Изменить"),
            KeyboardButton(text="Удалить"),
        ]
    )
    markup.row(
        KeyboardButton(text="Назад")
    )
    return markup


def faq_question_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    questions = [item[1] for item in manager.faq.get_all_questions()]
    buttons = [
        KeyboardButton(text=question)
        for question in questions
    ]
    markup.add(*buttons)
    return markup


def faq_events_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        KeyboardButton(text="Изменить вопрос"),
        KeyboardButton(text="Изменить ответ")
    ]
    markup.add(*buttons)
    return markup
