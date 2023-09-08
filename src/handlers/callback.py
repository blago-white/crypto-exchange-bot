from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from ..config.statements.buttons import callback as callback_buttons
from ..config.statements.templates import ECN_POOL_VOLUME_INPUT_INFO
from ..utils.states import EnteringPromocode, CurrencyPool
from ..config.settings import CUSTOM_CALLBACK_QUERIES_SEPARATOR
from ..filters.wallet import UserWalletMessagesFilter
from ..db.models import UserWallet

callback_router = Router()


@callback_router.callback_query(F.data == callback_buttons.InsertPromoButton().callback)
async def promocode(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(EnteringPromocode.entering_promocode)
    await callback.message.answer("Введите ваш промокод!")


@callback_router.callback_query(
    F.data.startswith(callback_buttons.CurrencySelectButton.CALLBACK_DATA_PREFIX),
    UserWalletMessagesFilter()
)
async def ecn_currency_select(callback: CallbackQuery, state: FSMContext, wallet: UserWallet):
    await callback.answer()

    currency = callback.data.split(CUSTOM_CALLBACK_QUERIES_SEPARATOR)[-1]

    await state.set_state(state=CurrencyPool.pool_volume_input)
    await state.set_data(
        data=dict(currency=currency)
    )

    await callback.message.answer(
        text=ECN_POOL_VOLUME_INPUT_INFO.format(currency=currency, user_wallet_amount=wallet.amount)
    )
