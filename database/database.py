from .managers.base import Manager
from .managers.cart import CartManager
from .managers.category import CategoryManager
from .managers.faq import FAQManager
from .managers.master import MasterManager, MasterUpdateManager
from .managers.service import ServiceManager, ServiceUpdateManager
from .managers.user import UserManager
from .managers.work_time import WorkTimeManager


class TableManager:
    def __init__(self) -> None:
        self.base: Manager = Manager()
        self.user: UserManager = UserManager()
        self.category: CategoryManager = CategoryManager()
        self.service: ServiceManager = ServiceManager()
        self.master: MasterManager = MasterManager()
        self.work_time: WorkTimeManager = WorkTimeManager()
        self.cart: CartManager = CartManager()
        self.faq: FAQManager = FAQManager()


class TableUpdaterManager:
    def __init__(self) -> None:
        self.service: ServiceUpdateManager = ServiceUpdateManager()
        self.master: MasterUpdateManager = MasterUpdateManager()
