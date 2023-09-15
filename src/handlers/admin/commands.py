from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.config.statements.buttons import text
from src.config.statements import texts
from src.filters.admin import AdminFilter
from src.utils.states import AdminAddPromocode, AdminDeletePromocode, AdminSupportChatAnswering
from src.db.executor import Executor
from src.db.models import Promocode
from src.filters.message.database import BaseDBExecutorMessagesFilter
from src.utils import promocodes

admin_commands_router = Router()
admin_commands_router.message.filter(AdminFilter())


@admin_commands_router.message(Command(text.ADMIN_NEW_PROMO))
async def add_promocode(message: Message, state: FSMContext):
    await state.set_state(AdminAddPromocode.entering_discount)
    await message.reply(text=texts.ADMIN_ADD_PROMO_INFO)


@admin_commands_router.message(Command(text.INFO))
async def admin_bot_info(message: Message):
    await message.reply(text=texts.ADMIN_COMMANDS_INFO)


@admin_commands_router.message(Command(text.ADMIN_END_ANSWERING_COMMAND), AdminSupportChatAnswering.answering)
async def end_answering_for_client(message: Message, state: FSMContext):
    await state.clear()
    await message.reply(text=texts.ADMIN_ANSWERING_ENDED)


@admin_commands_router.message(Command(text.ADMIN_LIST_PROMOS), BaseDBExecutorMessagesFilter())
async def all_promocodes(message: Message, state: FSMContext, executor: Executor) -> None:
    await message.answer(text=promocodes.get_promocodes_list(promocodes=Promocode.all(executor=executor)))


@admin_commands_router.message(Command(text.ADMIN_DEL_PROMO))
async def delete_promocode(message: Message, state: FSMContext) -> None:
    await state.set_state(state=AdminDeletePromocode.choosing_promocode)

    await message.reply(text=texts.CHOOSE_PROMOCODE)
