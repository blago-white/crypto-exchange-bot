from aiogram.types import Message

from ..config.statements import templates
from ..config.statements import texts
from ..utils.keyboards import reply
from ..utils.transactions import Transaction


async def send_transaction_result_success(transaction: Transaction, admin_confirmation_message: Message) -> None:
    await _send_transaction_result(success=True,
                                   transaction=transaction,
                                   admin_confirmation_message=admin_confirmation_message)


async def send_transaction_result_cancel(transaction: Transaction, admin_confirmation_message: Message) -> None:
    await _send_transaction_result(success=False,
                                   transaction=transaction,
                                   admin_confirmation_message=admin_confirmation_message)


async def _send_transaction_result(success: bool, transaction: Transaction,
                                   admin_confirmation_message: Message) -> None:
    admin_message_template, client_message_template = (
        templates.REQUEST_FOR_REPLENISHMENT_CONFIRMED_TEMPLATE, texts.TRANSACTION_ACCEPTED) if success else (
        templates.REQUEST_FOR_REPLENISHMENT_CANCELED_TEMPLATE, texts.TRANSACTION_CANCELED
    )

    await admin_confirmation_message.edit_text(
        text=admin_message_template.format(
            request_number=transaction.id,
            username=transaction.client.username,
            date=transaction.initialization_time
        )
    )

    await admin_confirmation_message.bot.send_message(
        chat_id=transaction.client.id,
        text=client_message_template.format(amount=transaction.amount),
        reply_markup=reply.account_keyboard
    )
