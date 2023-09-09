from aiogram import Dispatcher

from . import commands, callback, states
from .admin import callback as admin_callback, commands as admin_commands, states as admin_states

_ROUTERS = (
    admin_commands.admin_commands_router,
    admin_callback.callback_transaction_router,
    admin_states.admin_states_router,
    commands.commands_router,
    callback.callback_router,
    states.states_handlers_router
)


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.include_routers(*_ROUTERS)
