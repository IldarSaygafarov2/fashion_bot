from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data import configs as conf


def service_fields_menu(fields_dict: dict, service_id: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(text=value, callback_data=f"edit-{key}-{service_id}")
        for key, value in fields_dict.items()
    ]
    markup.add(*buttons)
    return markup


def service_actions_menu(service_id: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(text=value, callback_data=f"{field}_{service_id}")
        for field, value in conf.SERVICE_FIELDS_NAMES.items()
    ]
    markup.add(*buttons)
    return markup


def to_cart_menu(service_id: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(text="Выбрать", callback_data=f"service_{service_id}"),
        InlineKeyboardButton(text="Назад", callback_data="back"),
    )
    return markup


def choose_master(master_id: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(text="Выбрать", callback_data=f"master_{master_id}")
    )
    return markup


def master_work_time_menu(work_times: list) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        *[
            InlineKeyboardButton(text=time[0], callback_data=time[0])
            for time in work_times
        ]
    )
    return markup


def add_to_cart_menu(
    service_id: int, price: int, master_id: int, day: str, time: str, user_id: int
) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(
            text="Добавить в корзину",
            callback_data=f"{service_id}_{price}_{master_id}_{day}_{time}_{user_id}",
        )
    )
    return markup
