from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.config.statements.buttons.text import NEW_PROMO_COMMAND, INFO, ADMIN_END_ANSWERING_COMMAND, ADMIN_LIST_PROMOS
from src.config.statements.texts import ADMIN_ADD_PROMO_INFO, ADMIN_COMMANDS_INFO, ADMIN_ANSWERING_ENDED
from src.filters.admin import AdminFilter
from src.utils.states import AdminAddPromocode
from src.db.executor import Executor
from src.db.models import Promocode
from src.filters.message.database import BaseDBExecutorMessagesFilter
from src.utils import promocodes

admin_commands_router = Router()
admin_commands_router.message.filter(AdminFilter())


@admin_commands_router.message(Command(NEW_PROMO_COMMAND))
async def add_promocode(message: Message, state: FSMContext):
    await state.set_state(AdminAddPromocode.entering_withdraw_amount)
    await message.reply(text=ADMIN_ADD_PROMO_INFO)


@admin_commands_router.message(Command(INFO))
async def admin_bot_info(message: Message):
    await message.reply(text=ADMIN_COMMANDS_INFO)


@admin_commands_router.message(Command(ADMIN_END_ANSWERING_COMMAND))
async def end_answering_for_client(message: Message, state: FSMContext):
    await state.clear()
    await message.reply(text=ADMIN_ANSWERING_ENDED)


@admin_commands_router.message(Command(ADMIN_LIST_PROMOS), BaseDBExecutorMessagesFilter())
async def all_promocodes(message: Message, state: FSMContext, executor: Executor) -> None:
    promocodes_ = promocodes.get_promocodes_list(promocodes=Promocode.all(executor=executor))

    await message.answer(text=promocodes_)
