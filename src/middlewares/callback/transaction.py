import datetime
from typing import Callable, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.config import settings
from src.config.statements import texts
from src.utils.transactions import Transaction


class TransactionCallbackDataMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[CallbackQuery, dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: dict[str, Any]
    ) -> Any:
        client_id = int(event.data.split(settings.CUSTOM_CALLBACK_QUERIES_SEPARATOR)[-1])
        client_state: FSMContext = data['dispatcher'].fsm.resolve_context(
            bot=event.bot, chat_id=client_id, user_id=client_id
        )

        data.update(
            transaction=(await client_state.get_data()).get("transaction")
        )

        if (not data["transaction"] or
                not self._transaction_actual(transaction=data["transaction"])):
            return await event.message.edit_text(text=texts.TRANSACTION_BROKEN)

        await client_state.set_state(state=None)

        return await handler(event, data)

    @staticmethod
    def _transaction_actual(transaction: Transaction) -> bool:
        if not transaction:
            return

        return (
                datetime.datetime.now() - transaction.initialization_time
        ).total_seconds() < settings.TRANSACTION_COMLETION_TIME_SECONDS
