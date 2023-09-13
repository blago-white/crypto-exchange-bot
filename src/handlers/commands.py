from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.filters.message.database import BaseDBExecutorMessagesFilter
from src.filters.message.wallet import UserWalletMessagesFilter
from ..config import settings
from ..config.statements import templates, texts
from ..config.statements.buttons import text
from ..db.executor import Executor
from ..db.models import UserWallet
from ..middlewares.callback import states as states_middlewares
from ..utils import metrics, states, currencies
from ..utils.keyboards import inline, reply, keyboards_utils

commands_router = Router()
commands_router.message.middleware(states_middlewares.StatelessHandlerCallbackMiddleware())


@commands_router.message(CommandStart(), UserWalletMessagesFilter())
@commands_router.message(F.text == text.TO_ACCOUNT_COMMAND, UserWalletMessagesFilter())
async def start(message: Message, wallet: UserWallet) -> None:
    if not wallet.authorized:
        wallet.save()

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


@commands_router.message(F.text == text.ECN_OPEN_COMMAND, BaseDBExecutorMessagesFilter())
async def ecn_open(message: Message, executor: Executor) -> None:
    if UserWallet(executor=executor, userid=message.from_user.id).amount < settings.MIN_ECN_OPEN_WALLET_AMOUNT:
        return await message.answer(text=texts.NEED_REPLENISHMENT)

    currencies_ = currencies.get_current_currencies_rates(executor=executor)

    await message.answer(text=texts.USER_AGREEMENT, reply_markup=inline.agreement_inline_keyboard)

    await message.answer(
        text=templates.ECN_CURRENCIES_RATE.format(
            **currencies_, **currencies.convert_currencies_rates_to_rubles(currencies=currencies_)
        ),
        reply_markup=inline.currencies_inline_keyboard
    )


@commands_router.message(F.text == text.SEND_MONEY_COMMAND, UserWalletMessagesFilter())
async def send_money(message: Message, state: FSMContext, wallet: UserWallet) -> None:
    await state.set_state(states.Replenishment.choosing_payment_amount)
    await message.answer(text=texts.REPLENISHMENT_REQUEST_AMOUNT_INFO)

    promocode_discount = wallet.promocode

    if promocode_discount:
        await state.set_data(data=dict(discount=promocode_discount))
        await message.answer(text=templates.PROMOCODE_WILL_BE_USED.format(discount=promocode_discount))


@commands_router.message(F.text == text.RECEIVE_MONEY_COMMAND, UserWalletMessagesFilter())
async def withdraw_money(message: Message, state: FSMContext, wallet: UserWallet) -> None:
    if not wallet.verifed:
        return await message.answer(
            text=templates.WALLET_VERIFICATION_REQUIRED.format(firstname=message.from_user.first_name)
        )

    await state.set_state(states.Withdraw.choosing_withdraw_amount)
    await message.answer(text=templates.WITHDRAW_REQUEST_AMOUNT_INFO.format(amount=wallet.amount))


@commands_router.message(Command(text.VERIFY_COMMAND))
async def verify_request(message: Message) -> None:
    await message.answer(text=texts.USER_VERIFICATION_PAYMENT_WAIT)

    await message.bot.send_message(
        chat_id=settings.ADMIN_CHAN_ID,
        text=templates.WAIT_FOR_PAYMENT_VERIFICATION.format(
            usertag=message.from_user.username,
            userid=message.from_user.id
        ),
        reply_markup=keyboards_utils.get_wallet_verification_confirmation_keyboard(client_id=message.from_user.id)
    )


@commands_router.message(Command(text.INFO))
async def admin_bot_info(message: Message):
    await message.reply(text=texts.BOT_INFO)
