from aiogram.types import Message

from ..config.statements import commands
from ..utils import metrics


async def start(message: Message) -> None:
    await message.answer(
        text=commands.START_COMMAND_TEXT.format(
            userid=message.from_user.id,
            online=metrics.get_current_online()
        )
    )
