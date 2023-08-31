from aiogram.types import Message

from ..config.statements import templates
from ..db.models import UserWallet
from ..utils import metrics


async def start(message: Message, wallet: UserWallet) -> None:
    if not wallet.authorized:
        wallet.save_to_db()

    await message.answer(
        text=templates.USER_PROFILE_TEMPLATE.format(
            amount=wallet.amout,
            userid=message.from_user.id,
            online=metrics.get_current_online()
        )
    )

