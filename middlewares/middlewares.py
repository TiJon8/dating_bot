from typing import Any, Awaitable, Callable, Dict, List, Union, Optional, Tuple, cast, MutableMapping

import asyncio

from utils.types import *
from utils.db.db_api import db_API

from cachetools import TTLCache

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import (
    TelegramObject,
    Update,
    Message,
    CallbackQuery
)

DEFAULT_LATENCY = 0.2
DEFAULT_TTL = 0.3


class CustomSimpleMiddleware(BaseMiddleware):

    def __init__(
        self,
        album_key: str = "album",
        latency: float = DEFAULT_LATENCY,
        ttl: float = DEFAULT_TTL,
    ) -> None:
        self.album_key = album_key
        self.latency = latency
        self.cache: MutableMapping[str, Dict[str, Any]] = TTLCache(maxsize=10_000, ttl=ttl)

    @staticmethod
    def get_content(message: Message) -> Optional[Tuple[Media, str]]:
        if message.photo:
            return message.photo[-1], "photo"
        if message.video:
            return message.video, "video"
        if message.audio:
            return message.audio, "audio"
        if message.document:
            return message.document, "document"
        return None
    

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if isinstance(event, Message) and event.media_group_id:
            key = event.media_group_id
            media, content_type = cast(Tuple[Media, str], self.get_content(event))


            if key in self.cache:
                if content_type not in self.cache[key]:
                    self.cache[key][content_type] = [media]
                    return None
                
                self.cache[key]["messages"].append(event)
                self.cache[key][content_type].append(media)

                return None
            
            self.cache[key] = {
                    content_type: [media],
                    "messages": [event],
                    "caption": event.html_text,
                }

            await asyncio.sleep(self.latency)
            data[self.album_key] = Album.model_validate(
                self.cache[key], context={"bot": data["bot"]}
            )

        
        return await handler(event, data)

