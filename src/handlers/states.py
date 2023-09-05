import asyncio
import logging

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from ..config import settings
from ..config.statements import templates
from ..config.statements.buttons import text
from ..config.statements import texts
from ..db import dbvalidators
from ..db.models import UserWallet, Promocode
from ..db.executor import Executor
from ..filters.wallet import UserWalletMessagesFilter
from ..filters.database import BaseDBExecutorMessagesFilter
from ..utils import states, transactions, validators
from ..utils.keyboards import reply, keyboards_utils

states_handlers_router = Router()


@states_handlers_router.message(states.Replenishment.choosing_payment_amount)
async def make_transaction(message: Message, state: FSMContext) -> None:
    if not validators.replenishment_amount_number_valid(message.text):
        return await message.answer(text=texts.NOT_CORRECT_REPLENISHMENT_AMOUNT)

    transaction = transactions.Transaction(
        client=transactions.TransactionClient(id=message.from_user.id, username=message.from_user.username),
        amount=int(message.text),
        discount=(await state.get_data()).get("discount", 0)
    )

    await state.set_state(states.Replenishment.wait_payment_confirmation)

    await state.set_data(data=dict(transaction=transaction))

    await message.answer(
        text=templates.REPLENISHMENT_REQUEST_TEMPLATE.format(amount=transaction.amount),
        reply_markup=ReplyKeyboardRemove()
    )

    await message.bot.send_message(
        chat_id=settings.ADMIN_CHAN_ID,
        text=templates.USER_SEND_REQUEST_FOR_REPLENISHMENT_TEMPLATE.format(
            username=transaction.client.username,
            amount=transaction.amount,
            request_number=transaction.id,
            date=transaction.initialization_time
        ),
        reply_markup=keyboards_utils.get_transaction_confirmation_keyboard(
            client_id=message.from_user.id
        )
    )

    await asyncio.sleep(settings.TRANSACTION_COMLETION_TIME_SECONDS)

    if await state.get_state() == states.Replenishment.wait_payment_confirmation:
        await message.bot.send_message(
            chat_id=transaction.client.id,
            text=texts.TRANSACTION_CANCELED,
            reply_markup=reply.account_keyboard
        )

        await state.clear()


@states_handlers_router.message(states.Withdraw.choosing_withdraw_amount, UserWalletMessagesFilter())
async def select_card_for_withdraw(message: Message, state: FSMContext, wallet: UserWallet) -> None:
    if not validators.withdraw_amount_number_valid(withdraw_amount_text=message.text, wallet_amount=wallet.amount):
        return await message.answer(text=texts.NOT_CORRECT_WITHDRAW_AMOUNT)

    await state.set_state(states.Withdraw.choosing_withdraw_card)
    await state.set_data(data=dict(withdraw_amount=int(message.text)))
    await message.answer(text=templates.WITHDRAW_REQUEST_CARD_INFO.format(amount=message.text))


@states_handlers_router.message(states.Withdraw.choosing_withdraw_card, UserWalletMessagesFilter())
async def withdraw_request(message: Message, state: FSMContext, wallet: UserWallet) -> None:
    if not validators.card_number_valid(message.text):
        return await message.answer(text=texts.NOT_CORRECT_CARD_REQUISITES)

    wallet -= (await state.get_data())["withdraw_amount"]

    await state.clear()
    await message.answer(text=texts.WITHDRAW_REQUEST_SAVED)


@states_handlers_router.message(
    states.EnteringPromocode.entering_promocode, BaseDBExecutorMessagesFilter(), UserWalletMessagesFilter()
)
async def enter_promocode(message: Message, state: FSMContext, executor: Executor, wallet: UserWallet):
    if not dbvalidators.promocode_valid(message.text):
        await message.answer(texts.PROMOCODE_NOT_CORRECT)

    promocode = Promocode(executor=executor, promocode=message.text)

    logging.debug(msg=f"{promocode=} {promocode.title=}")

    promo_discount = promocode.get_promocode_discount()

    if not promo_discount or type(promo_discount) is not int:
        await message.answer(texts.PROMOCODE_NOT_EXISTS)

    await state.clear()

    wallet.promocode = message.text

    await message.answer(templates.PROMOCODE_APPLIED.format(discount=promo_discount))
