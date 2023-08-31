from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery

from ..config.statements.buttons.callback import InsertPromoButton

callback_router = Router()


@callback_router.callback_query(F.data == InsertPromoButton.callback())
async def promocode(callback: CallbackQuery):
    await callback.message.answer("insert promo please!")
    await callback.answer()
