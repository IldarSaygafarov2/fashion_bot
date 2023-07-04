from aiogram import types
from aiogram.dispatcher.filters import Filter
from .configs import ADMIN_LIST
admins = set()


class IsAdmin(Filter):
    key = "is_admin"

    async def check(self, message: types.Message) -> bool:
        return message.from_user.id in ADMIN_LIST
