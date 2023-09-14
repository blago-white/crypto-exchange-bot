from typing import Callable, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from ..config.statements.texts import TRANSACTION_CANCELED_BY_USER
from ..utils.states import Replenishment


class TransactionBlockingMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message | CallbackQuery, dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: dict[str, Any]
    ) -> Any:
        if await data["state"].get_state() == Replenishment.wait_payment_confirmation:
            await self._on_canceling_transaction(message=event if type(event) is Message else event.message)

        return await handler(event, data)

    @staticmethod
    async def _on_canceling_transaction(message: Message, state: FSMContext):
        await message.answer(text=TRANSACTION_CANCELED_BY_USER)
        await state.clear()
