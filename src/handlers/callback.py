import asyncio

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardRemove

from ..config.settings import CUSTOM_CALLBACK_QUERIES_SEPARATOR, POOL_DURATION
from ..config.statements import templates
from ..config.statements.buttons import callback as callback_buttons
from ..config.statements.buttons.text import NEXT_POOL_QUESTION
from ..config.statements.texts import TRADING_ENDED, ENTER_PROMO
from ..db.executor import Executor
from ..db.models import UserWallet, Currencies
from ..filters.database import BaseDBExecutorMessagesFilter
from ..filters.wallet import UserWalletMessagesFilter
from ..utils import pools, currencies
from ..utils.keyboards import inline
from ..utils.states import EnteringPromocode, CurrencyPool

callback_router = Router()


@callback_router.callback_query(F.data == callback_buttons.InsertPromoButton().callback)
async def promocode(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(EnteringPromocode.entering_promocode)
    await callback.message.answer(text=ENTER_PROMO)


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
        text=templates.ECN_POOL_VOLUME_INPUT_INFO.format(
            currency=currency.capitalize(), user_wallet_amount=wallet.amount
        )
    )


@callback_router.callback_query(CurrencyPool.pool_type_input, BaseDBExecutorMessagesFilter())
async def ecn_pool_type_select(callback: CallbackQuery, state: FSMContext, executor: Executor):
    await callback.answer()

    currencies_model, user_wallet = (
        Currencies(executor=executor), UserWallet(executor=executor, userid=callback.from_user.id)
    )

    pool_type: pools.AbstractECNPoolType = pools.get_pool_type_by_code(callback.data)
    pool_data: dict = await state.get_data()

    await state.clear()

    pool_currency, pool_amount_rub, pool_details_message = (
        str(pool_data.get("currency")),
        float(pool_data.get("amount_rub")),
        pool_data.get("pool_details_message")
    )

    start_currency_rate: float = float(currencies_model.get_rate(currency=pool_currency))

    await pool_details_message.edit_text(text=templates.POOL_STARTED.format(pool_amount_rub=pool_amount_rub),
                                         reply_keyboard=ReplyKeyboardRemove())

    await asyncio.sleep(POOL_DURATION)

    end_currency_rate = float(currencies_model.get_rate(currency=pool_currency))
    pool_currency_rate_delta = end_currency_rate - start_currency_rate

    pool_status = pools.pool_is_successfully(pool_type=pool_type, currency_rate_delta=pool_currency_rate_delta)
    pools.apply_pool_result_to_wallet(pool_status=pool_status, pool_value=pool_amount_rub, user_wallet=user_wallet)

    await pool_details_message.edit_text(text=templates.POOL_ENDED_INFO.format(
        pool_type=pool_type.text,
        currency=pool_currency,
        pool_amount_rub=pool_amount_rub,
        start_currency_rate_usd=start_currency_rate,
        start_currency_rate_rub=currencies.convert_usd_to_rub(amount=start_currency_rate),
        end_currency_rate_usd=end_currency_rate,
        end_currency_rate_rub=currencies.convert_usd_to_rub(amount=end_currency_rate)
    ))

    pool_result_template = (
        templates.POOL_ENDED_UNSUCCESSFULLY if not pool_status else templates.POOL_ENDED_SUCCESSFULLY
    )

    await callback.message.answer(
        text=pool_result_template.format(
            pool_type_icon=pool_type.icon,
            pool_result=pools.get_pool_result_description(
                pool_currency_rate_delta=end_currency_rate - start_currency_rate),
            pool_amount_rub=pool_amount_rub,
            wallet_amount=user_wallet.amount
        )
    )

    await callback.message.answer(
        text=NEXT_POOL_QUESTION,
        reply_markup=inline.ecn_pool_continue_inline_keyboard
    )


@callback_router.callback_query(
    F.data == callback_buttons.ContinueTradingButton().callback,
    BaseDBExecutorMessagesFilter()
)
async def continue_trading(callback: CallbackQuery, state: FSMContext, executor: Executor):
    await callback.answer()

    await state.clear()

    currencies_ = currencies.get_current_currencies_rates(executor=executor)

    await callback.message.answer(
        text=templates.ECN_CURRENCIES_RATE.format(
            **currencies_, **currencies.convert_currencies_rates_to_rubles(currencies=currencies_)
        ),
        reply_markup=inline.currencies_inline_keyboard
    )


@callback_router.callback_query(F.data == callback_buttons.StopTradingButton().callback)
async def stop_trading(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await callback.message.answer(text=TRADING_ENDED)
