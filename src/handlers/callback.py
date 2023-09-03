from aiogram import Router, F
from aiogram.types import CallbackQuery

from ..config.statements.buttons import callback as callback_buttons
from ..db.executor import Executor
from ..db.models import UserWallet
from ..filters.admin import AdminFilter
from ..middlewares.dbmiddlewares import BaseDBMiddleware
from ..middlewares.transaction_middlewares import TransactionCallbackDataMiddleware
from ..utils import messages
from ..utils.transactions import Transaction

callback_router = Router()
callback_transaction_router = Router()
callback_transaction_router.callback_query.middleware(TransactionCallbackDataMiddleware())
callback_transaction_router.callback_query.middleware(BaseDBMiddleware())
callback_router.include_router(callback_transaction_router)


@callback_router.callback_query(F.data == callback_buttons.InsertPromoButton.callback())
async def promocode(callback: CallbackQuery):
    await callback.message.answer("insert promo please!")
    await callback.answer()


@callback_transaction_router.callback_query(
    F.data[:len(callback_buttons.AdminConfirmTransactionButton.CALLBACK_DATA_PREFIX)] ==
    callback_buttons.AdminConfirmTransactionButton.CALLBACK_DATA_PREFIX,
    AdminFilter()
)
async def confirm_transaction(callback: CallbackQuery, transaction: Transaction, executor: Executor):
    await callback.answer()

    user_wallet = UserWallet(executor=executor, userid=transaction.client.id)
    user_wallet.amount += transaction.amount

    await messages.send_transaction_result_success(transaction=transaction,
                                                   admin_confirmation_message=callback.message)


@callback_transaction_router.callback_query(
    F.data[:len(callback_buttons.AdminCancelTransactionButton.CALLBACK_DATA_PREFIX)] ==
    callback_buttons.AdminCancelTransactionButton.CALLBACK_DATA_PREFIX,
    AdminFilter()
)
async def cancel_transaction(callback: CallbackQuery, transaction: Transaction, executor: Executor):
    await callback.answer()

    await messages.send_transaction_result_cancel(transaction=transaction,
                                                  admin_confirmation_message=callback.message)
