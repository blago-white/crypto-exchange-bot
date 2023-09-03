from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.config.statements.buttons import callback


def get_transaction_confirmation_keyboard(client_id: int) -> InlineKeyboardButton:
    transaction_inline_keyboard = InlineKeyboardBuilder()

    transaction_inline_keyboard.row(InlineKeyboardButton(
        text=callback.AdminConfirmTransactionButton.text(),
        callback_data=callback.AdminConfirmTransactionButton.callback(add_callback_data=str(client_id))
    ))

    transaction_inline_keyboard.row(InlineKeyboardButton(
        text=callback.AdminCancelTransactionButton.text(),
        callback_data=callback.AdminCancelTransactionButton.callback(add_callback_data=str(client_id)),
    ))

    return transaction_inline_keyboard.as_markup()
