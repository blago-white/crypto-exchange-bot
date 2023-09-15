from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.config.statements import templates
from src.config.statements import texts
from src.db.dbvalidators import promocode_percentage_valid
from src.db.executor import Executor
from src.db.models import Promocode
from src.filters.admin import AdminFilter
from src.filters.message.database import BaseDBExecutorMessagesFilter
from src.utils.promocodes import save_promocode as save_promocode_to_db
from src.utils import states

admin_states_router = Router()
admin_states_router.message.filter(AdminFilter())


@admin_states_router.message(states.AdminAddPromocode.entering_discount, BaseDBExecutorMessagesFilter())
async def save_promocode(message: Message, state: FSMContext, executor: Executor):
    if not promocode_percentage_valid(message.text):
        return await message.reply(text=texts.ADMIN_PROMO_NOT_CORRECT)

    promo_title = save_promocode_to_db(executor=executor, discount=int(message.text))

    await state.clear()

    await message.reply(
        text=templates.ADMIN_PROMO_SAVED.format(promo_title=promo_title, discount=message.text)
    )


@admin_states_router.message(states.AdminSupportChatAnswering.answering)
async def answer_for_client(message: Message, state: FSMContext):
    client_id = (await state.get_data()).get("client_id")

    await message.bot.send_message(
        chat_id=client_id,
        text=templates.ANSWER_FROM_SUPPORT_FOR_USER_TEMPLATE.format(adminanswer=message.text)
    )


@admin_states_router.message(states.AdminDeletePromocode.choosing_promocode, BaseDBExecutorMessagesFilter())
async def delete_promocode(message: Message, state: FSMContext, executor: Executor) -> None:
    promocode = Promocode(executor=executor, promocode=message.text)

    if not promocode.promocode_exists():
        return await message.reply(text=texts.PROMOCODE_DOES_NOT_EXISTS)

    promocode.delete()

    await state.set_state(state=None)
    await message.reply(text=texts.PROMOCODE_DELETED)
