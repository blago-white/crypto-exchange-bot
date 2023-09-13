from aiogram.filters import Filter
from aiogram.types import Message

from src.db import models, executor


class UserWalletMessagesFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        with executor.Executor() as executor_:
            return dict(wallet=models.UserWallet(executor=executor_, userid=message.from_user.id))
