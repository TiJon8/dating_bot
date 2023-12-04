from aiogram.filters.base import Filter
from aiogram.types import Message, CallbackQuery
from utils.db.db_api import db_API
from typing import Dict, Any

class StartFilter(Filter):

    async def __call__(self, callback: CallbackQuery, flags: Dict[str, Any]):
        pass
