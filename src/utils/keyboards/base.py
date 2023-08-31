from aiogram import types

from src.config.statements.buttons import text

account_keyboard = types.ReplyKeyboardMarkup(keyboard=[
    [types.KeyboardButton(text=text.TO_ACCOUNT_COMMAND)],
    [types.KeyboardButton(text=text.ECN_OPEN_COMMAND)],
    [types.KeyboardButton(text=text.SEND_MONEY_COMMAND), types.KeyboardButton(text=text.RECEIVE_MONEY_COMMAND)]
], resize_keyboard=True)
