from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.config.statements.buttons.text import NEW_PROMO_COMMAND, INFO
from src.config.statements.texts import ADMIN_ADD_PROMO_INFO, ADMIN_COMMANDS_INFO
from src.filters.admin import AdminFilter
from src.utils.states import AdminAddPromocode

admin_commands_router = Router()
admin_commands_router.message.filter(AdminFilter())


@admin_commands_router.message(Command(NEW_PROMO_COMMAND))
async def add_promocode(message: Message, state: FSMContext):
    await state.set_state(AdminAddPromocode.entering_withdraw_amount)
    await message.reply(text=ADMIN_ADD_PROMO_INFO)


@admin_commands_router.message(Command(INFO))
async def admin_bot_info(message: Message):
    await message.reply(text=ADMIN_COMMANDS_INFO)
