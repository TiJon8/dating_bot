# импортируем executor для обращения на сервера Телеграм
from loader import dp, bot
import asyncio

# import middlewares, filters, handlers -> именно в таком порядке импорты обработчиков
from middlewares.middlewares import (
    CustomSimpleMiddleware,
    )
import handlers


async def on_startup():
    print('бот стартавал')

# главная функция запуска поллинга и инициализации дополнительных параметров
async def main():
    dp.message.middleware.register(CustomSimpleMiddleware())
    
    dp.startup.register(on_startup)
    await dp.start_polling(bot)

# запуск поллинга
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('До свидания')