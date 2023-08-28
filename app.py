# импортируем executor для обращения на сервера Телеграм
from loader import dp
from aiogram import executor

# import middlewares, filters, handlers -> именно в таком порядке импорты обработчиков
import handlers
from utils.notify_startup import on_startup_notify
from utils.set_bot_commands import set_default_commands
from utils.db.db_api import db_API



async def on_startup(dp):

    await set_default_commands(dp)
    db_API.check_table()

    await on_startup_notify(dp)


# запуск поллинга
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, allowed_updates=['message', 'chat_member'])