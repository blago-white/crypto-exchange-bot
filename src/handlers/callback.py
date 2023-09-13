from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.filters.message.database import BaseDBExecutorMessagesFilter
from src.filters.message.wallet import UserWalletMessagesFilter
from ..config.settings import CUSTOM_CALLBACK_QUERIES_SEPARATOR
from ..config.statements import templates
from ..config.statements.buttons import callback as callback_buttons
from ..config.statements.buttons.text import NEXT_POOL_QUESTION
from ..config.statements.texts import TRADING_ENDED, ENTER_PROMO, USER_VERIFY_SELF_WALLET, NOT_ENOUGH_MONEY
from ..db.executor import Executor
from ..db.models import UserWallet
from ..middlewares.callback import autoanswer
from ..utils import currencies, messages, exceptions
from ..utils.keyboards import inline
from ..utils.pools import utils
from ..utils.states import EnteringPromocode, CurrencyPool

callback_router = Router()
callback_router.callback_query.middleware(autoanswer.AutoAnswerCallbackMiddleware())


@callback_router.callback_query(F.data == callback_buttons.InsertPromoButton().callback)
async def promocode(callback: CallbackQuery, state: FSMContext):
    await state.set_state(EnteringPromocode.entering_promocode)
    await callback.message.answer(text=ENTER_PROMO)


@callback_router.callback_query(
    F.data.startswith(callback_buttons.CurrencySelectButton.CALLBACK_DATA_PREFIX),
    UserWalletMessagesFilter()
)
async def ecn_currency_select(callback: CallbackQuery, state: FSMContext, wallet: UserWallet):
    currency = callback.data.split(CUSTOM_CALLBACK_QUERIES_SEPARATOR)[-1]

    await state.set_state(state=CurrencyPool.pool_volume_input)
    await state.set_data(data=dict(currency=currency))

    await callback.message.answer(text=templates.ECN_POOL_VOLUME_INPUT_INFO.format(
        currency=currency.capitalize(), user_wallet_amount=wallet.amount
    )
    )


@callback_router.callback_query(CurrencyPool.pool_type_input, BaseDBExecutorMessagesFilter())
async def start_ecn_pool(callback: CallbackQuery, state: FSMContext, executor: Executor):
    await state.set_state(state=None)

    try:
        await messages.make_ecn_pool(start_pool_message=callback.message,
                                     pool=await utils.get_pool(callback=callback, user_state=state),
                                     user_wallet=UserWallet(executor=executor, userid=callback.from_user.id))

    except exceptions.NotEnoughMoneyForPool:
        return await callback.message.answer(text=NOT_ENOUGH_MONEY)

    await state.clear()

    await callback.message.answer(text=NEXT_POOL_QUESTION, reply_markup=inline.ecn_pool_continue_inline_keyboard)


@callback_router.callback_query(
    F.data == callback_buttons.ContinueTradingButton().callback,
    BaseDBExecutorMessagesFilter()
)
async def continue_trading(callback: CallbackQuery, state: FSMContext, executor: Executor):
    await state.clear()

    await callback.message.delete()

    currencies_ = currencies.get_current_currencies_rates(executor=executor)

    await callback.message.answer(
        text=templates.ECN_CURRENCIES_RATE.format(
            **currencies_, **currencies.convert_currencies_rates_to_rubles(currencies=currencies_)
        ),
        reply_markup=inline.currencies_inline_keyboard
    )


@callback_router.callback_query(F.data == callback_buttons.StopTradingButton().callback)
async def stop_trading(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(text=TRADING_ENDED)


@callback_router.callback_query(
    F.data.startswith(callback_buttons.VerifyUserWalletButton.CALLBACK_DATA_PREFIX),
    BaseDBExecutorMessagesFilter()
)
async def verify_user_wallet(callback: CallbackQuery, executor: Executor):
    client_id = int(callback.data.split(CUSTOM_CALLBACK_QUERIES_SEPARATOR)[-1])
    user_wallet = UserWallet(executor=executor, userid=client_id)

    user_wallet.verifed = True

    await callback.message.edit_text(text=templates.ADMIN_USER_WALLET_VERIFIED.format(
        userid=client_id
    ))

    await callback.bot.send_message(chat_id=client_id, text=USER_VERIFY_SELF_WALLET)
