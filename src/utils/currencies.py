import random

from src.db.models import Currencies
from src.db.executor import Executor
from src.config.settings import SUPPORTED_CURRENCIES, USD_RUB_RATE


def get_current_currencies_rates(executor: Executor) -> dict[str, float]:
    currencies = Currencies(executor=executor).currencies

    return {currency.lower(): currencies[currency] for currency in currencies}


def convert_currencies_rates_to_rubles(currencies: dict[str, float]):
    return {currency.lower()+"rubrate": currencies[currency]*USD_RUB_RATE for currency in currencies}
