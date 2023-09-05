from aiogram import Router, F
from aiogram.types import CallbackQuery

from ..config.statements.buttons import callback as callback_buttons

callback_router = Router()


@callback_router.callback_query(F.data == callback_buttons.InsertPromoButton.callback())
async def promocode(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("insert promo please!")
