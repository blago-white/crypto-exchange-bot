from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.config import settings
from src.config.statements import templates
from src.config.statements.buttons import callback as callback_buttons
from src.db.executor import Executor
from src.db.models import UserWallet
from src.filters.admin import AdminCallbackFilter
from src.filters.message.database import BaseDBExecutorMessagesFilter
from src.middlewares.callback.autoanswer import AutoAnswerCallbackMiddleware
from src.middlewares.callback.transaction import TransactionCallbackDataMiddleware
from src.utils import messages, states
from src.utils.transactions import Transaction

admin_callback_router = Router()

_callback_transaction_router = Router()
_callback_transaction_router.callback_query.middleware(TransactionCallbackDataMiddleware())
_callback_transaction_router.callback_query.filter(AdminCallbackFilter())

admin_callback_router.include_router(_callback_transaction_router)
admin_callback_router.callback_query.middleware(AutoAnswerCallbackMiddleware())


@_callback_transaction_router.callback_query(
    F.data.startswith(callback_buttons.AdminConfirmTransactionButton.CALLBACK_DATA_PREFIX),
    BaseDBExecutorMessagesFilter()
)
async def confirm_transaction(callback: CallbackQuery, transaction: Transaction, executor: Executor):
    user_wallet = UserWallet(executor=executor, userid=transaction.client.id)
    user_wallet += transaction.amount + (transaction.amount * transaction.discount / 100)

    await messages.send_transaction_result_success(transaction=transaction,
                                                   admin_confirmation_message=callback.message)


@_callback_transaction_router.callback_query(
    F.data.startswith(callback_buttons.AdminCancelTransactionButton.CALLBACK_DATA_PREFIX)
)
async def cancel_transaction(callback: CallbackQuery, transaction: Transaction):
    await messages.send_transaction_result_cancel(transaction=transaction,
                                                  admin_confirmation_message=callback.message)


@admin_callback_router.callback_query(
    F.data.startswith(callback_buttons.AdminSupportAnsweringButton.CALLBACK_DATA_PREFIX)
)
async def support_answer_for_client(callback: CallbackQuery, state: FSMContext):
    client_id = int(callback.data.split(settings.CUSTOM_CALLBACK_QUERIES_SEPARATOR)[-1])

    await state.set_data(data=dict(client_id=client_id))
    await state.set_state(state=states.AdminSupportChatAnswering.answering)

    await callback.message.reply(
        text=templates.ADMIN_READY_FOR_ANSWERING_FOR_CLIENT.format(adminname=callback.from_user.username)
    )
