from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.config.statements.buttons import callback


def get_transaction_confirmation_keyboard(client_id: int) -> InlineKeyboardButton:
    transaction_inline_keyboard = InlineKeyboardBuilder()

    transaction_inline_keyboard.row(InlineKeyboardButton(
        text=callback.AdminConfirmTransactionButton(extra_callback_data=str(client_id)).text,
        callback_data=callback.AdminConfirmTransactionButton(extra_callback_data=str(client_id)).callback
    ))

    transaction_inline_keyboard.row(InlineKeyboardButton(
        text=callback.AdminCancelTransactionButton(extra_callback_data=str(client_id)).text,
        callback_data=callback.AdminCancelTransactionButton(extra_callback_data=str(client_id)).callback
    ))

    return transaction_inline_keyboard.as_markup()
