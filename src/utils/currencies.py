from src.config.settings import USD_RUB_RATE
from src.db.executor import Executor
from src.db.models import Currencies


def get_current_currencies_rates(executor: Executor) -> dict[str, float]:
    currencies = Currencies(executor=executor).currencies

    return {currency.lower(): currencies[currency] for currency in currencies}


def convert_currencies_rates_to_rubles(currencies: dict[str, float]):
    return {currency.lower() + "rubrate": currencies[currency] * USD_RUB_RATE for currency in currencies}


def convert_rub_to_usd(amount: int | float) -> float:
    return round(amount / USD_RUB_RATE, 2)


def convert_usd_to_rub(amount: int | float) -> float:
    return round(amount * USD_RUB_RATE, 2)
