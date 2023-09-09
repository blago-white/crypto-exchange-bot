import string

from aiogram.fsm.storage.memory import MemoryStorage

CONFIG_FILE = "botconfig.ini"

PROMOCODE_ALLOWED_SYMBOLS = set(string.ascii_letters+string.digits)

PROMOCODE_LENGTH = 16

MAX_PROMOCODE_DISCOUNT_PERCENTAGE = 50

MIN_PROMOCODE_DISCOUNT_PERCENTAGE = 5

ACCOUNT_IMAGE_ID = "AgACAgIAAxkBAAPQZPCqzEphUKVFQUbCcBSJSz9nOZgAAu7LMRv1wIFLaKxZBiAQs9UBAAMCAANzAAMwBA"

MIN_DEPOSIT_AMOUNT_RUB = 1500

MIN_WITHDRAW_AMOUNT_RUB = 1000

MAX_DEPOSIT_AMOUNT_RUB = 1000000

MAX_WITHDRAW_AMOUNT_RUB = MAX_DEPOSIT_AMOUNT_RUB

CARD_FOR_USERS_DEPOSITS_NUMBER = 2200700898861363

CARD_FOR_USERS_DEPOSITS_BANK = "Tinkoff Bank"

ADMIN_CHAN_ID = -1001989686982

SUPPORT_BOT_TAG = "binance_support_trade_bot"

TRANSACTION_COMLETION_TIME_SECONDS = 900

ADMINS = (
    935570478,
)

BOT_ID = 6432965544

CUSTOM_CALLBACK_QUERIES_SEPARATOR = "@"

STATES_STORAGE = MemoryStorage

SUPPORTED_CURRENCIES = (
    "Bitcoin", "Ripple", "Doge", "Ethereum", "BinanceCoin", "Litecoin", "Euro"
)

ALTERNATIVE_CURRENCY = "USD"

USD_RUB_RATE = 98.2

MIN_ECN_POOL_VALUE = 100

CURRENCIES_RATES_UPDATING_COOLDOWN = 5

POOL_DURATION = 30
