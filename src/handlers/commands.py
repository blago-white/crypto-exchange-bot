import asyncio

from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from ..config import settings
from ..config.statements import templates
from ..config.statements.buttons import text
from ..db import validators
from ..db.models import UserWallet
from ..middlewares import dbmiddlewares
from ..utils import metrics, transactions
from ..utils.keyboards import inline, reply, keyboards_utils
from ..utils.states import Replenishment

commands_router = Router()
wallet_handlers_router = Router()
wallet_handlers_router.message.middleware(dbmiddlewares.UserWalletMiddleware())
commands_router.include_router(wallet_handlers_router)


@wallet_handlers_router.message(CommandStart())
@wallet_handlers_router.message(F.text == text.TO_ACCOUNT_COMMAND)
async def start(message: Message, wallet: UserWallet) -> None:
    if not wallet.authorized:
        wallet.save_wallet()

    await message.answer(text="⭐", reply_markup=reply.account_keyboard)
    await message.answer_photo(
        photo=settings.ACCOUNT_IMAGE_ID,
        caption=templates.USER_PROFILE_TEMPLATE.format(
            amount=wallet.amount,
            userid=message.from_user.id,
            online=metrics.get_current_online()
        ),
        reply_markup=inline.account_inline_keyboard
    )


@wallet_handlers_router.message(F.text == text.ECN_OPEN_COMMAND)
async def ecn_open(message: Message, wallet: UserWallet) -> None:
    if wallet.amount < settings.MIN_DEPOSIT_AMOUNT_RUB:
        return await message.answer(text=text.NEED_REPLENISHMENT)

    await message.answer(text=text.USER_AGREEMENT, reply_markup=inline.agreement_inline_keyboard)


@commands_router.message(F.text == text.SEND_MONEY_COMMAND, StateFilter(None))
async def send_money(message: Message, state: FSMContext) -> None:
    await state.set_state(Replenishment.choosing_payment_amount)
    await message.answer(text=text.REPLENISHMENT_REQUEST_AMOUNT_INFO)


@wallet_handlers_router.message(F.text == text.RECEIVE_MONEY_COMMAND)
async def receive_money(message: Message, wallet: UserWallet) -> None:
    return


@commands_router.message(Replenishment.choosing_payment_amount)
async def make_transaction(message: Message, state: FSMContext) -> None:
    if not validators.replenishment_amount_number_valid(message.text):
        return await message.answer(text=text.NOT_CORRECT_AMOUNT)

    transaction = transactions.Transaction(
        client=transactions.TransactionClient(id=message.from_user.id, username=message.from_user.username),
        amount=int(message.text)
    )

    await state.set_state(Replenishment.wait_payment_confirmation)

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

    if await state.get_state() == Replenishment.wait_payment_confirmation:
        await message.bot.send_message(
            chat_id=transaction.client.id,
            text=text.TRANSACTION_CANCELED,
            reply_markup=reply.account_keyboard
        )

        await state.clear()
