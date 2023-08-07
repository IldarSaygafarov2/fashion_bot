from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from database.database import TableManager, TableUpdaterManager
from .configs import TOKEN, PROXY_URL

manager = TableManager()
update_manager = TableUpdaterManager()
storage = MemoryStorage()

# переменная с помощью которой можно делать запросы к телеграму
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=storage)
