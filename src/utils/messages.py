import asyncio

from aiogram.types import Message

from . import currencies
from .exceptions import NotEnoughMoneyForPool
from .pools import ECNPool, utils
from ..config import settings
from ..config.statements import templates
from ..config.statements import texts
from ..db.models import UserWallet, Currencies
from ..utils.keyboards import reply
from ..utils.transactions import Transaction


async def make_ecn_pool(
        start_pool_message: Message,
        pool: ECNPool,
        user_wallet: UserWallet) -> None:
    currencies_model = Currencies(executor=user_wallet.executor)

    if user_wallet.amount < pool.pool_amount:
        raise NotEnoughMoneyForPool

    start_currency_rate: float = float(currencies_model.get_rate(currency=pool.pool_currency))

    await start_pool_message.edit_text(text=templates.POOL_STARTED.format(
        pool_amount_rub=pool.pool_amount,
        elapsed_time=int(False)
    ))

    await start_pool_timer(message_for_timer=start_pool_message,
                           message_template=templates.POOL_STARTED.format(
                               pool_amount_rub=pool.pool_amount,
                               elapsed_time="{elapsed_time}"
                           ))

    end_currency_rate = float(currencies_model.get_rate(currency=pool.pool_currency))

    pool_currency_rate_delta = end_currency_rate - start_currency_rate

    pool_result_success = utils.pool_is_successfully(pool_type=pool.pool_type,
                                                     currency_rate_delta=pool_currency_rate_delta)

    utils.apply_pool_result_to_wallet(pool_status=pool_result_success,
                                      pool_value=pool.pool_amount,
                                      user_wallet=user_wallet)

    await start_pool_message.edit_text(text=templates.POOL_ENDED_INFO.format(
        pool_type=pool.pool_type.text,
        currency=pool.pool_currency,
        pool_amount_rub=pool.pool_amount,
        start_currency_rate_usd=start_currency_rate,
        start_currency_rate_rub=currencies.convert_usd_to_rub(amount=start_currency_rate),
        end_currency_rate_usd=end_currency_rate,
        end_currency_rate_rub=currencies.convert_usd_to_rub(amount=end_currency_rate)
    ))

    await start_pool_message.answer(
        text=(templates.POOL_ENDED_UNSUCCESSFULLY if not pool_result_success else
              templates.POOL_ENDED_SUCCESSFULLY).format(
            pool_type_icon=pool.pool_type.icon,
            pool_result=utils.get_pool_result_description(pool_currency_rate_delta=pool_currency_rate_delta),
            pool_amount_rub=pool.pool_amount,
            wallet_amount=user_wallet.amount
        ))


async def send_transaction_result_success(transaction: Transaction, admin_confirmation_message: Message) -> None:
    await _send_transaction_result(success=True,
                                   transaction=transaction,
                                   admin_confirmation_message=admin_confirmation_message)


async def start_pool_timer(message_for_timer: Message, message_template: str):
    for elapsed_time in range(settings.MIN_MESSAGE_UPDATE_DELAY, settings.POOL_DURATION,
                              settings.MIN_MESSAGE_UPDATE_DELAY):
        await asyncio.sleep(settings.MIN_MESSAGE_UPDATE_DELAY)
        await message_for_timer.edit_text(text=message_template.format(elapsed_time=elapsed_time))


async def send_transaction_result_cancel(transaction: Transaction, admin_confirmation_message: Message) -> None:
    await _send_transaction_result(success=False,
                                   transaction=transaction,
                                   admin_confirmation_message=admin_confirmation_message)


async def _send_transaction_result(
        success: bool, transaction: Transaction,
        admin_confirmation_message: Message) -> None:
    admin_message_template, client_message_template = (
        templates.REQUEST_FOR_REPLENISHMENT_CONFIRMED_TEMPLATE, texts.TRANSACTION_ACCEPTED) if success else (
        templates.REQUEST_FOR_REPLENISHMENT_CANCELED_TEMPLATE, texts.TRANSACTION_CANCELED
    )

    await admin_confirmation_message.edit_text(
        text=admin_message_template.format(
            request_number=transaction.id,
            username=transaction.client.username,
            date=transaction.initialization_time
        )
    )

    await admin_confirmation_message.bot.send_message(
        chat_id=transaction.client.id,
        text=client_message_template.format(amount=transaction.amount),
        reply_markup=reply.account_keyboard
    )
