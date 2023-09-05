from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from ..config.statements.buttons import callback as callback_buttons
from ..utils.states import EnteringPromocode

callback_router = Router()


@callback_router.callback_query(F.data == callback_buttons.InsertPromoButton.callback())
async def promocode(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(EnteringPromocode.entering_promocode)
    await callback.message.answer("Введите ваш промокод!")
