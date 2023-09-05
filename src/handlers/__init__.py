from aiogram import Dispatcher

from .admin import callback as admin_callback
from . import commands, callback, states

_ROUTERS = (
    admin_callback.callback_transaction_router,
    commands.commands_router,
    callback.callback_router,
    states.states_handlers_router
)


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.include_routers(*_ROUTERS)
