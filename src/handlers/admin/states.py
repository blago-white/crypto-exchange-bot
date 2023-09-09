from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.config.statements import templates
from src.config.statements.texts import ADMIN_PROMO_NOT_CORRECT
from src.db.dbvalidators import promocode_percentage_valid
from src.db.executor import Executor
from src.filters.admin import AdminFilter
from src.filters.database import BaseDBExecutorMessagesFilter
from src.utils.promocodes import save_promocode as save_promocode_to_db
from src.utils.states import AdminAddPromocode

admin_states_router = Router()
admin_states_router.message.filter(AdminFilter())


@admin_states_router.message(AdminAddPromocode.entering_withdraw_amount, BaseDBExecutorMessagesFilter())
async def save_promocode(message: Message, state: FSMContext, executor: Executor):
    if not promocode_percentage_valid(message.text):
        return await message.reply(text=ADMIN_PROMO_NOT_CORRECT)

    promo_title = save_promocode_to_db(executor=executor, discount=int(message.text))

    await state.clear()

    await message.reply(
        text=templates.ADMIN_PROMO_SAVED.format(promo_title=promo_title, discount=message.text)
    )
