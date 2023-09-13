from typing import Callable, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery


class StatelessHandlerCallbackMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[CallbackQuery, dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: dict[str, Any]
    ) -> Any:
        await data.get("state").clear()

        return await handler(event, data)
