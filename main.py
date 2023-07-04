from aiogram.utils import executor

import handlers
from data.filters import IsAdmin
from data.loader import dp


def main() -> None:
    dp.bind_filter(IsAdmin)
    executor.start_polling(dp)


if __name__ == "__main__":
    main()
