import datetime
from typing import Callable, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from ..config import settings
from ..config.statements.buttons import text
from ..utils.states import get_user_stortage_key
from ..utils.transactions import Transaction


class TransactionCallbackDataMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: dict[str, Any]
    ) -> Any:
        client_id = int(event.data.split(settings.CUSTOM_CALLBACK_QUERIES_SEPARATOR)[-1])
        user_state: FSMContext = data["state"]
        client_storage_key = get_user_stortage_key(userid=client_id)

        data.update(
            transaction=(await user_state.storage.get_data(
                key=client_storage_key
            )).get("transaction")
        )

        if (not data["transaction"] or
                not self._transaction_actual(transaction=data["transaction"])):
            return await event.message.edit_text(text=text.TRANSACTION_BROKEN)

        await user_state.storage.set_state(key=client_storage_key, state=None)

        return await handler(event, data)

    @staticmethod
    def _transaction_actual(transaction: Transaction) -> bool:
        return (
            datetime.datetime.now() - transaction.initialization_time
        ).total_seconds() < settings.TRANSACTION_COMLETION_TIME_SECONDS
