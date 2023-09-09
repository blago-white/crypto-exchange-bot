import random
import time
from abc import ABCMeta

from . import exceptions
from .dbvalidators import promocode_valid, promocode_percentage_valid
from .executor import Executor
from ..config.settings import CURRENCIES_RATES_UPDATING_COOLDOWN


class _BaseModel(metaclass=ABCMeta):
    _EXECUTOR: Executor

    def __init__(self, executor: Executor = None):
        self._EXECUTOR = executor


class _BaseWalletModel(_BaseModel, metaclass=ABCMeta):
    _EXECUTOR: Executor

    _authorized: bool = None

    @property
    def authorized(self) -> bool:
        if self._authorized is None:
            self._authorized = self._EXECUTOR.fetch(
                f"SELECT EXISTS (SELECT userid FROM wallets WHERE userid={self._USERID})"
            )[0]

        return self._authorized

    @staticmethod
    def _amount_change_args_validator(function):
        def wrapp(*args, **kwargs):
            amount = args[-1] if len(args) > 1 else kwargs["amount"]

            if amount < 0:
                raise ValueError("Attempt to change the invoice amount to a negative number")

            return function(*args, **kwargs)

        return wrapp

    @staticmethod
    def _model_auth_required(function):
        def wrapp(*args, **kwargs):
            instance: _BaseWalletModel = args[0]

            if not (instance._authorized or instance.authorized):
                raise PermissionError("Wallet not authorized")

            return function(*args, **kwargs)

        return wrapp


class Currencies(_BaseModel):
    _EXECUTOR: Executor
    _last_rates_update: float
    _currencies: dict[str, float]

    def __new__(cls, executor: Executor = None):
        if not hasattr(cls, "instance"):
            cls.instance = super(Currencies, cls).__new__(cls)

            if not executor:
                raise ValueError("There is not a single instance, a executor is needed!")

            cls.instance.__init__(executor=executor)
            cls.instance._update_currencies_rates()

        return cls.instance

    @staticmethod
    def _rate_updater(method):
        def wrapp(*args, **kwargs):
            currencies_model: Currencies = args[0]

            if time.time() - currencies_model._last_rates_update > CURRENCIES_RATES_UPDATING_COOLDOWN:
                currencies_model._update_currencies_rates()

            return method(*args, **kwargs)

        return wrapp

    @property
    @_rate_updater
    def currencies(self) -> dict[str, float]:
        return self._currencies

    @_rate_updater
    def get_rate(self, currency) -> float:
        return self._currencies[currency]

    def _update_currencies_rates(self):
        if ("_last_rates_update" in self.__dict__
                and self._get_time_after_updating() < CURRENCIES_RATES_UPDATING_COOLDOWN):
            return

        if "_currencies" in self.__dict__:
            for currency in self._currencies:
                new_rate = self._currencies[currency]
                new_rate += self._get_random_currency_incrementer(currency_rate=new_rate)

                self._EXECUTOR.insert(sql=f"UPDATE currencies SET rate={new_rate} WHERE currency='{currency}'")

        self._currencies = {
            currency: float(rate)
            for currency, rate in self._EXECUTOR.fetchall(sql="SELECT * FROM currencies;")
        }
        self._last_rates_update = time.time()

    def _get_time_after_updating(self):
        return time.time() - self._last_rates_update

    @staticmethod
    def _get_random_currency_incrementer(currency_rate: float) -> float:
        incrementer = random.uniform(-currency_rate / 100, currency_rate / 100)

        if currency_rate <= abs(incrementer):
            incrementer = -incrementer

        return incrementer


class UserWallet(_BaseWalletModel):
    _USERID: int

    _used_promocode: str = None

    def __init__(self, executor: Executor, userid: int):
        self._USERID = int(userid)
        super().__init__(executor=executor)

    @_BaseWalletModel._model_auth_required
    @_BaseWalletModel._amount_change_args_validator
    def __add__(self, amount: int):
        self._EXECUTOR.insert(
            sql=f"UPDATE wallets SET amount = amount + {int(amount)} WHERE userid={self._USERID}"
        )

    @_BaseWalletModel._model_auth_required
    @_BaseWalletModel._amount_change_args_validator
    def __sub__(self, amount: int):
        if self._EXECUTOR.fetch(sql=f"SELECT amount FROM wallets WHERE userid={self._USERID}")[0] < amount:
            raise ValueError("Negative amount of the user's account")

        self._EXECUTOR.insert(
            sql=f"UPDATE wallets SET amount = amount - {int(amount)} WHERE userid={self._USERID}"
        )

    @property
    @_BaseWalletModel._model_auth_required
    def promocode(self) -> int | None:
        promocode = (self._used_promocode or self._get_user_promocode())

        if promocode is None:
            return

        discount = self._EXECUTOR.fetch(sql=f"SELECT discount FROM promocodes WHERE promocode='{promocode}'")

        if discount is not None:
            return discount[0]

    @promocode.setter
    @_BaseWalletModel._model_auth_required
    def promocode(self, promocode: str) -> None:
        self._EXECUTOR.insert(sql=f"UPDATE wallets SET used_promo='{str(promocode)}' WHERE userid={self._USERID}")
        self._used_promocode = str(promocode)

    @property
    def amount(self) -> int:
        amount = self._EXECUTOR.fetch(sql=f"SELECT amount FROM wallets WHERE userid={self._USERID};")
        if amount is None:
            self._authorized = False
            return 0

        return amount[0]

    @property
    @_BaseWalletModel._model_auth_required
    def verifed(self) -> bool:
        return self._EXECUTOR.fetch(sql=f"SELECT verified FROM wallets WHERE userid={self._USERID}")[0]

    @verifed.setter
    @_BaseWalletModel._model_auth_required
    def verifed(self, _) -> None:
        self._EXECUTOR.insert(sql=f"UPDATE wallets SET verified=true WHERE userid={self._USERID}")

    def save(self):
        if (self._authorized is None) or self.authorized:
            return

        self._EXECUTOR.insert(sql=f"INSERT INTO wallets VALUES ({self._USERID})")

    def _get_user_promocode(self) -> str | None:
        promocode = self._EXECUTOR.fetch(f"SELECT used_promo FROM wallets WHERE userid={self._USERID}")

        if promocode is not None:
            return promocode[0]


class Promocode:
    def __init__(self, executor: Executor, promocode: str):
        self._EXECUTOR = executor
        self._PROMOCODE = promocode

    @property
    def title(self):
        return self._PROMOCODE

    def save_promocode(self, discount: int) -> None:
        if not promocode_valid(promocode=self._PROMOCODE) or not promocode_percentage_valid(percentage=discount):
            raise exceptions.PromocodeNotCorrectError()

        if self.promocode_exists():
            raise exceptions.PromocodeAlreadyExistsError()

        self._EXECUTOR.insert(sql=f"INSERT INTO promocodes VALUES ('{self._PROMOCODE}', {discount})")

    def promocode_exists(self) -> bool:
        return self._EXECUTOR.fetch(
            sql=f"SELECT EXISTS (SELECT * FROM promocodes WHERE promocode='{self._PROMOCODE}')"
        )[0]

    def get_promocode_discount(self) -> int:
        return self._EXECUTOR.fetch(sql=f"SELECT discount FROM promocodes WHERE promocode='{self._PROMOCODE}'")[0]
