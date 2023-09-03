from aiogram.filters import Filter
from aiogram.types import Message

from src.config import settings


class AdminFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in settings.ADMINS
