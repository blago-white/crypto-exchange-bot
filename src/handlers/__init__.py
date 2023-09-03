from aiogram import Dispatcher

from . import commands, callback

_ROUTERS = (
    commands.commands_router,
    callback.callback_router,
)


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.include_routers(*_ROUTERS)
