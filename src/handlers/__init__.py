from aiogram import Dispatcher
from aiogram.filters import CommandStart

from . import commands


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.message.register(commands.start, CommandStart())
