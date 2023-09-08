from abc import ABCMeta, abstractmethod

from src.config.settings import CUSTOM_CALLBACK_QUERIES_SEPARATOR
from . import text


class _BaseCallbackButton(metaclass=ABCMeta):
    @abstractmethod
    def text(self) -> str:
        pass

    @abstractmethod
    def callback(self) -> str:
        pass


class _BaseCustomCallbackButton(metaclass=ABCMeta):
    CALLBACK_DATA_PREFIX: str
    CALLBACK_DATA: str

    def __init__(self, extra_callback_data: str):
        self.CALLBACK_DATA = CUSTOM_CALLBACK_QUERIES_SEPARATOR.join(
            (self.CALLBACK_DATA_PREFIX, extra_callback_data)
        )

    @abstractmethod
    def text(self) -> str:
        pass

    @abstractmethod
    def callback(self) -> str:
        pass


class InsertPromoButton(_BaseCallbackButton):
    @property
    def text(self) -> str:
        return text.INSERT_PROMO

    @property
    def callback(self) -> str:
        return "insert_promo"


class AdminConfirmTransactionButton(_BaseCustomCallbackButton):
    CALLBACK_DATA_PREFIX = "confirm_transaction" + CUSTOM_CALLBACK_QUERIES_SEPARATOR

    @property
    def text(self) -> str:
        return text.ACCEPT_TRANSACTION

    @property
    def callback(self) -> str:
        return self.CALLBACK_DATA


class AdminCancelTransactionButton(_BaseCustomCallbackButton):
    CALLBACK_DATA_PREFIX = "cancel_transaction" + CUSTOM_CALLBACK_QUERIES_SEPARATOR

    @property
    def text(self) -> str:
        return text.CANCEL_TRANSACTION

    @property
    def callback(self) -> str:
        return self.CALLBACK_DATA


class CurrencySelectButton(_BaseCustomCallbackButton):
    CALLBACK_DATA_PREFIX = "currency" + CUSTOM_CALLBACK_QUERIES_SEPARATOR

    _CURRENCY: str

    def __init__(self, currency: str):
        self._CURRENCY = currency
        super().__init__(extra_callback_data=self._CURRENCY.lower())

    @property
    def text(self) -> str:
        return f"🔸 {self._CURRENCY.capitalize()}"

    @property
    def callback(self) -> str:
        return self.CALLBACK_DATA
