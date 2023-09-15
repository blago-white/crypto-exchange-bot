import asyncio

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.filters.message.database import BaseDBExecutorMessagesFilter
from src.filters.message.wallet import UserWalletMessagesFilter
from .commands import support_chat as support_chat_command_handler
from ..config import settings
from ..config.statements import templates
from ..config.statements import texts
from ..db import dbvalidators
from ..db.executor import Executor
from ..db.models import UserWallet, Promocode, Currencies
from ..utils import states, transactions, validators, currencies
from ..utils.keyboards import reply, keyboards_utils, inline

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
        text=templates.REPLENISHMENT_REQUEST_TEMPLATE.format(amount=transaction.amount)
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

    await support_chat_command_handler(message=message, state=state)

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

    promo_discount = promocode.get_promocode_discount()

    if not promo_discount or type(promo_discount) is not int:
        await message.answer(texts.PROMOCODE_NOT_EXISTS)

    await state.clear()

    wallet.promocode = message.text

    await message.answer(templates.PROMOCODE_APPLIED.format(discount=promo_discount))


@states_handlers_router.message(states.CurrencyPool.pool_volume_input,
                                F.text.isdigit(),
                                BaseDBExecutorMessagesFilter())
async def input_ecn_pool_value(message: Message, state: FSMContext, executor: Executor):
    if int(message.text) < settings.MIN_ECN_POOL_VALUE:
        return await message.answer(text=texts.POOL_VALUE_SMALL)

    if int(message.text) > UserWallet(executor=executor, userid=message.from_user.id).amount:
        return await message.answer(text=texts.NOT_ENOUGH_MONEY)

    requested_currency_name: str | None = (await state.get_data()).get("currency")
    requested_currency_rate = Currencies(executor=executor).get_rate(currency=requested_currency_name)

    if not requested_currency_name:
        return await message.answer(text=texts.POOL_CURRENCY_DOES_NOT_EXISTS)

    await state.set_state(state=states.CurrencyPool.pool_type_input)

    await state.set_data(data=dict(currency=requested_currency_name,
                                   amount_rub=float(message.text)))

    await message.answer(text=templates.ECN_POOL_TYPE_SELECT.format(
        currency=requested_currency_name.capitalize(),
        currency_rate=requested_currency_rate,
        currency_rate_rub=currencies.convert_usd_to_rub(requested_currency_rate)),
        reply_markup=inline.ecn_pool_types_inline_keyboard)


@states_handlers_router.message(states.SupportChat.chat)
async def support_chat(message: Message):
    message_text: str | None = message.text or message.caption
    message_file_id: str | None = (message.photo.pop().file_id if message.photo else None
                                   ) or (message.document.file_id if message.document else None)

    message_credentials_string, admin_answering_keyboard = (
        templates.SUPPORT_CHAT_TEXT_MESSAGE_CREDENTIALS_TEMPLATE.format(
            username=message.from_user.username,
            usermessage=message_text
        ) if message_text else
        templates.SUPPORT_CHAT_MEDIA_MESSAGE_CREDENTIALS_TEMPLATE.format(username=message.from_user.username),
        keyboards_utils.get_support_answering_keyboard(client_id=message.from_user.id)
    )

    if not message_text and not message_file_id:
        return

    await message.reply(text=texts.MESSAGE_SENDED_FOR_SUPPORT)

    if not message_file_id:
        return await message.bot.send_message(chat_id=settings.ADMIN_CHAN_ID,
                                              text=message_credentials_string,
                                              reply_markup=admin_answering_keyboard)

    elif message.photo:
        await message.bot.send_photo(chat_id=settings.ADMIN_CHAN_ID,
                                     photo=message_file_id,
                                     caption=message_credentials_string,
                                     reply_markup=admin_answering_keyboard)

    elif message.document:
        await message.bot.send_document(chat_id=settings.ADMIN_CHAN_ID,
                                        document=message_file_id,
                                        caption=message_credentials_string,
                                        reply_markup=admin_answering_keyboard)
