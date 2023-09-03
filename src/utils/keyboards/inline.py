from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.config.statements.buttons import links, callback

account_inline_keyboard = InlineKeyboardBuilder()
agreement_inline_keyboard = InlineKeyboardBuilder()


account_inline_keyboard.row(types.InlineKeyboardButton(
    text=links.MainChannelLink.text(),
    url=links.MainChannelLink.url()
))
account_inline_keyboard.row(types.InlineKeyboardButton(
    text=links.SupportLink.text(),
    url=links.SupportLink.url()
))
account_inline_keyboard.row(types.InlineKeyboardButton(
    text=callback.InsertPromoButton.text(),
    callback_data=callback.InsertPromoButton.callback()
))

agreement_inline_keyboard.row(types.InlineKeyboardButton(
    text=links.UserAgreementLink.text(),
    url=links.UserAgreementLink.url()
))

account_inline_keyboard = account_inline_keyboard.as_markup()
agreement_inline_keyboard = agreement_inline_keyboard.as_markup()
