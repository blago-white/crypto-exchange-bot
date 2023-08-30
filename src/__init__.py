from aiogram import Bot, Dispatcher

from .config.settings import Config
from . import handlers


async def setup_bot(config: Config) -> None:
    await _start_pooling(dispatcher=_get_dispatcher(), bot=_get_bot_instance(token=config.bot.token))


def _get_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher()
    handlers.register_handlers(dispatcher=dispatcher)

    return dispatcher


def _get_bot_instance(token: str) -> Bot:
    return Bot(token=token, parse_mode="HTML")


async def _start_pooling(dispatcher: Dispatcher, bot: Bot) -> None:
    await dispatcher.start_polling(bot)
