from aiogram import types
from aiogram import Bot

async def set_default_commands(bot: Bot):
    await bot.set_my_commands(
        [
            types.BotCommand('start', 'Меню')
        ]
    )