from abc import ABCMeta, abstractmethod

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


class InsertPromoButton(_BaseCallbackButton):
    @staticmethod
    def text() -> str:
        return text.INSERT_PROMO

    @staticmethod
    def callback() -> str:
        return "insert_promo"
