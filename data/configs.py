import os

from dotenv import load_dotenv

load_dotenv()

PROXY_URL = "http://proxy.server:3128"
TOKEN = os.getenv("TOKEN")

ADMIN_LIST = [int(x) for x in os.getenv("ADMINS_LIST").split(",") if x]

SERVICE_FIELDS_NAMES = ["Название", "Описание", "Цена", "Фото", "Категория"]
MASTER_FIELDS_NAMES = ["Полное имя", "Описание", "Фото", "Стоимость услуг", "Услуга"]
