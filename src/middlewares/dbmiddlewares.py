from typing import Callable, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.types import Message

from ..db import models, executor


class BaseDBMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: dict[str, Any]
    ) -> Any:
        with executor.Executor() as executor_:
            data.update(executor=executor_)
            return await handler(event, data)


class UserWalletMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: dict[str, Any]
    ) -> Any:
        with executor.Executor() as executor_:
            data.update(wallet=models.UserWallet(executor=executor_, userid=event.from_user.id))
            return await handler(event, data)
