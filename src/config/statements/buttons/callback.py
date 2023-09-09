from abc import ABCMeta, abstractmethod

from src.config.settings import CUSTOM_CALLBACK_QUERIES_SEPARATOR
from src.utils import pools
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


class ECNPoolTypeSelectButton(_BaseCallbackButton):
    _POOL_TYPE: pools.AbstractECNPoolType

    def __init__(self, pool_type: pools.AbstractECNPoolType):
        if type(pool_type) is pools.AbstractECNPoolType:
            raise "The use of the abstract class is prohibited"

        self._POOL_TYPE = pool_type

    @property
    def text(self) -> str:
        return self._POOL_TYPE.text

    @property
    def callback(self) -> str:
        return self._POOL_TYPE.callback


class ContinueTradingButton(_BaseCallbackButton):
    @property
    def text(self) -> str:
        return text.YES

    @property
    def callback(self) -> str:
        return "ecncontinue"


class StopTradingButton(_BaseCallbackButton):
    @property
    def text(self) -> str:
        return text.NO

    @property
    def callback(self) -> str:
        return "ecnstop"

