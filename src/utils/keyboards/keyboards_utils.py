from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from src.config.statements.buttons import callback


def get_transaction_confirmation_keyboard(client_id: int) -> InlineKeyboardMarkup:
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


def get_wallet_verification_confirmation_keyboard(client_id: int) -> InlineKeyboardMarkup:
    verification_inline_keyboard = InlineKeyboardBuilder()

    verification_inline_keyboard.row(InlineKeyboardButton(
        text=callback.VerifyUserWalletButton(extra_callback_data=str(client_id)).text,
        callback_data=callback.VerifyUserWalletButton(extra_callback_data=str(client_id)).callback
    ))

    return verification_inline_keyboard.as_markup()


def get_support_answering_keyboard(client_id: int) -> InlineKeyboardMarkup:
    support_answering_keyboard = InlineKeyboardBuilder()

    support_answering_keyboard.row(InlineKeyboardButton(
        text=callback.AdminSupportAnsweringButton(extra_callback_data=str(client_id)).text,
        callback_data=callback.AdminSupportAnsweringButton(extra_callback_data=str(client_id)).callback
    ))

    return support_answering_keyboard.as_markup()
