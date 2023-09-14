from aiogram import Dispatcher, Router

from . import commands, callback, states
from .admin import callback as admin_callback, commands as admin_commands, states as admin_states
from ..middlewares import replenishment

_ROUTERS = (
    admin_commands.admin_commands_router,
    admin_callback.admin_callback_router,
    admin_states.admin_states_router,
    commands.commands_router,
    callback.callback_router,
    states.states_handlers_router
)

client_router = Router()
admin_router = Router()

client_router.include_routers(commands.commands_router,
                              callback.callback_router,
                              states.states_handlers_router)

client_router.message.middleware(replenishment.TransactionBlockingMiddleware())
client_router.callback_query.middleware(replenishment.TransactionBlockingMiddleware())

admin_router.include_routers(admin_commands.admin_commands_router,
                             admin_callback.admin_callback_router,
                             admin_states.admin_states_router)


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.include_routers(client_router, admin_router)
