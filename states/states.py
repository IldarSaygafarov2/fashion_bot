from aiogram.dispatcher.filters.state import State, StatesGroup


class RegistrationState(StatesGroup):
    username = State()
    phone_number = State()
    lang = State()


class ServiceState(StatesGroup):
    service = State()
    cart = State()
    master = State()
    day = State()
    time = State()


class AdminCategoryState(StatesGroup):
    add = State()
    delete = State()
    update = State()
    update_2 = State()


class AdminAddServiceState(StatesGroup):
    name = State()
    content = State()
    price = State()
    photo = State()
    category = State()


class AdminServiceState(StatesGroup):
    start = State()
    add = State()
    name = State()
    delete = State()
    update = State()
    update_2 = State()


class AdminMasterState(StatesGroup):
    start = State()
    add = State()
    name = State()
    delete = State()
    update = State()
    update_2 = State()


class AdminUpdateServiceState(StatesGroup):
    service_id = State()
    name = State()
    content = State()
    photo = State()
    category = State()
    price = State()


class AdminMasterActionsState(StatesGroup):
    full_name = State()
    content = State()
    photo = State()
    price = State()
    service_id = State()


class FAQActionState(StatesGroup):
    start = State()
    add_question = State()
    add_answer = State()
    update = State()
    update_process = State()
    update_question = State()
    update_answer = State()
    delete = State()
