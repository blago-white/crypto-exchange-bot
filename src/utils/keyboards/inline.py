from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.config.settings import SUPPORTED_CURRENCIES
from src.config.statements.buttons import links, callback

account_inline_keyboard = InlineKeyboardBuilder()
agreement_inline_keyboard = InlineKeyboardBuilder()
currencies_inline_keyboard = InlineKeyboardBuilder()

account_inline_keyboard.row(types.InlineKeyboardButton(
    text=links.MainChannelLink.text(),
    url=links.MainChannelLink.url()
))
account_inline_keyboard.row(types.InlineKeyboardButton(
    text=links.SupportLink.text(),
    url=links.SupportLink.url()
))
account_inline_keyboard.row(types.InlineKeyboardButton(
    text=callback.InsertPromoButton().text,
    callback_data=callback.InsertPromoButton().callback
))

agreement_inline_keyboard.row(types.InlineKeyboardButton(
    text=links.UserAgreementLink.text(),
    url=links.UserAgreementLink.url()
))


def _fill_currencies_keyboard(keyboard: InlineKeyboardBuilder) -> None:
    buttons_row = list()

    for currency_idx, currency in enumerate(SUPPORTED_CURRENCIES):
        currency_button = callback.CurrencySelectButton(currency=currency)

        buttons_row.append(types.InlineKeyboardButton(
            text=currency_button.text,
            callback_data=currency_button.callback
        ))

        if currency_idx and not (currency_idx + 1) % 3:
            keyboard.row(*buttons_row)
            buttons_row.clear()


account_inline_keyboard = account_inline_keyboard.as_markup()
agreement_inline_keyboard = agreement_inline_keyboard.as_markup()

_fill_currencies_keyboard(keyboard=currencies_inline_keyboard)
currencies_inline_keyboard = currencies_inline_keyboard.as_markup()
