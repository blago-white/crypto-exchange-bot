from aiogram import Dispatcher
from aiogram.filters import CommandStart

from . import commands, callback


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.include_router(commands.commands_router)
    dispatcher.include_router(callback.callback_router)
