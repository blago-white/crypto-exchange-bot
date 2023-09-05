from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from src.config import settings


class AdminFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in settings.ADMINS and message.chat.type == "supergroup"


class AdminCallbackFilter(Filter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.from_user.id in settings.ADMINS and callback.message.chat.type == "supergroup"
