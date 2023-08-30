from aiogram import Bot, Dispatcher

from .settings import Config
from .handlers import commands


async def setup_bot(config: Config) -> None:
    bot = _get_bot_instance(token=config.bot.token)
    dispatcher = _get_configured_dispatcher()

    await _start_pooling(dispatcher=dispatcher, bot=bot)


def _get_configured_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher()
    dispatcher.message.register(commands.start)

    return dispatcher


def _get_bot_instance(token: str) -> Bot:
    return Bot(token=token, parse_mode="HTML")


async def _start_pooling(dispatcher: Dispatcher, bot: Bot) -> None:
    await dispatcher.start_polling(bot)
