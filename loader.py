from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from data import config

from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aioredis import Redis


# реализация Redis хранилища
redisCLI = Redis(host='127.0.0.1',
                port=6379,
                decode_responses=True)

storage = RedisStorage(
    redis=redisCLI,
    key_builder=DefaultKeyBuilder(with_destiny=True)
)


# создание объектов бота и диспетчера
bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=storage)
