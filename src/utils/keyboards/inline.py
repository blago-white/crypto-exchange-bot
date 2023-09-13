from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.config.settings import SUPPORTED_CURRENCIES
from src.config.statements.buttons import links, callback
from src.utils.pools import types as pooltypes

account_inline_keyboard = InlineKeyboardBuilder()
agreement_inline_keyboard = InlineKeyboardBuilder()
currencies_inline_keyboard = InlineKeyboardBuilder()
ecn_pool_types_inline_keyboard = InlineKeyboardBuilder()
ecn_pool_continue_inline_keyboard = InlineKeyboardBuilder()

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

ecn_pool_types_inline_keyboard.row(types.InlineKeyboardButton(
    text=callback.ECNPoolTypeSelectButton(pool_type=pooltypes.ECNPoolTypeUp).text,
    callback_data=callback.ECNPoolTypeSelectButton(pool_type=pooltypes.ECNPoolTypeUp).callback
))

ecn_pool_types_inline_keyboard.row(types.InlineKeyboardButton(
    text=callback.ECNPoolTypeSelectButton(pool_type=pooltypes.ECNPoolTypeDown).text,
    callback_data=callback.ECNPoolTypeSelectButton(pool_type=pooltypes.ECNPoolTypeDown).callback
))

ecn_pool_types_inline_keyboard.row(types.InlineKeyboardButton(
    text=callback.ECNPoolTypeSelectButton(pool_type=pooltypes.ECNPoolTypeSame).text,
    callback_data=callback.ECNPoolTypeSelectButton(pool_type=pooltypes.ECNPoolTypeSame).callback
))

ecn_pool_continue_inline_keyboard.row(
    types.InlineKeyboardButton(
        text=callback.ContinueTradingButton().text,
        callback_data=callback.ContinueTradingButton().callback
    ),
    types.InlineKeyboardButton(
        text=callback.StopTradingButton().text,
        callback_data=callback.StopTradingButton().callback
    )
)


def _fill_currencies_keyboard(keyboard: InlineKeyboardBuilder) -> None:
    buttons_row = list()

    for currency_idx, currency in enumerate(SUPPORTED_CURRENCIES):
        currency_button = callback.CurrencySelectButton(currency=currency)

        buttons_row.append(types.InlineKeyboardButton(
            text=currency_button.text,
            callback_data=currency_button.callback
        ))

        if currency_idx and not (currency_idx + 1) % 4 or currency_idx == len(SUPPORTED_CURRENCIES) - 1:
            keyboard.row(*buttons_row)
            buttons_row.clear()


account_inline_keyboard = account_inline_keyboard.as_markup()
agreement_inline_keyboard = agreement_inline_keyboard.as_markup()

_fill_currencies_keyboard(keyboard=currencies_inline_keyboard)
currencies_inline_keyboard = currencies_inline_keyboard.as_markup()

ecn_pool_types_inline_keyboard = ecn_pool_types_inline_keyboard.as_markup()

ecn_pool_continue_inline_keyboard = ecn_pool_continue_inline_keyboard.as_markup()
