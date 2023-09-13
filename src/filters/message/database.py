from typing import Any

from aiogram.filters import Filter
from aiogram.types import Message

from src.db import executor


class BaseDBExecutorMessagesFilter(Filter):
    async def __call__(self, message: Message) -> Any:
        with executor.Executor() as executor_:
            return dict(executor=executor_)
