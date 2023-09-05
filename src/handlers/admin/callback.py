from aiogram import Router, F
from aiogram.types import CallbackQuery

from src.config.statements.buttons import callback as callback_buttons
from src.db.executor import Executor
from src.db.models import UserWallet
from src.filters.admin import AdminCallbackFilter
from src.filters.database import BaseDBExecutorMessagesFilter
from src.middlewares.callback.transaction_middlewares import TransactionCallbackDataMiddleware
from src.utils import messages
from src.utils.transactions import Transaction

callback_transaction_router = Router()
callback_transaction_router.callback_query.middleware(TransactionCallbackDataMiddleware())
callback_transaction_router.callback_query.filter(AdminCallbackFilter())


@callback_transaction_router.callback_query(
    F.data[:len(callback_buttons.AdminConfirmTransactionButton.CALLBACK_DATA_PREFIX)] ==
    callback_buttons.AdminConfirmTransactionButton.CALLBACK_DATA_PREFIX,
    BaseDBExecutorMessagesFilter()
)
async def confirm_transaction(callback: CallbackQuery, transaction: Transaction, executor: Executor):
    await callback.answer()

    user_wallet = UserWallet(executor=executor, userid=transaction.client.id)
    user_wallet += transaction.amount + (transaction.amount * transaction.discount / 100)

    await messages.send_transaction_result_success(transaction=transaction,
                                                   admin_confirmation_message=callback.message)


@callback_transaction_router.callback_query(
    F.data[:len(callback_buttons.AdminCancelTransactionButton.CALLBACK_DATA_PREFIX)] ==
    callback_buttons.AdminCancelTransactionButton.CALLBACK_DATA_PREFIX,
)
async def cancel_transaction(callback: CallbackQuery, transaction: Transaction):
    await callback.answer()

    await messages.send_transaction_result_cancel(transaction=transaction,
                                                  admin_confirmation_message=callback.message)
