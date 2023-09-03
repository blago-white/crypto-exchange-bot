from abc import ABCMeta, abstractmethod

from src.config.settings import CUSTOM_CALLBACK_QUERIES_SEPARATOR
from . import text


class _BaseCallbackButton(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def text() -> str:
        pass

    @staticmethod
    @abstractmethod
    def callback() -> str:
        pass


class _BaseCustomCallbackButton(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def text() -> str:
        pass

    @staticmethod
    @abstractmethod
    def callback(add_callback_data: str) -> str:
        pass


class InsertPromoButton(_BaseCallbackButton):
    @staticmethod
    def text() -> str:
        return text.INSERT_PROMO

    @staticmethod
    def callback() -> str:
        return "insert_promo"


class AdminConfirmTransactionButton(_BaseCustomCallbackButton):
    CALLBACK_DATA_PREFIX = "confirm_transaction" + CUSTOM_CALLBACK_QUERIES_SEPARATOR

    @staticmethod
    def text() -> str:
        return text.ACCEPT_TRANSACTION

    @staticmethod
    def callback(add_callback_data: str) -> str:
        return AdminConfirmTransactionButton.CALLBACK_DATA_PREFIX + add_callback_data


class AdminCancelTransactionButton(_BaseCustomCallbackButton):
    CALLBACK_DATA_PREFIX = "cancel_transaction" + CUSTOM_CALLBACK_QUERIES_SEPARATOR

    @staticmethod
    def text() -> str:
        return text.CANCEL_TRANSACTION

    @staticmethod
    def callback(add_callback_data: str) -> str:
        return AdminCancelTransactionButton.CALLBACK_DATA_PREFIX + add_callback_data
