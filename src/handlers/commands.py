from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram import Router

from ..config.statements import templates
from ..db.models import UserWallet
from ..utils import metrics
from ..utils.keyboards import inline, base


commands_router = Router()


@commands_router.message(CommandStart())
async def start(message: Message, wallet: UserWallet) -> None:
    if not wallet.authorized:
        wallet.save_to_db()

    await message.answer(text="⭐", reply_markup=base.account_keyboard)
    await message.answer(
        text=templates.USER_PROFILE_TEMPLATE.format(
            amount=wallet.amout,
            userid=message.from_user.id,
            online=metrics.get_current_online()
        ),
        reply_markup=inline.account_inline_keyboard
    )

