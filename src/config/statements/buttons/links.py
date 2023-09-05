from abc import ABCMeta, abstractmethod

from src.config.settings import SUPPORT_BOT_TAG
from . import text


class _BaseLinkButton(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def text() -> str:
        pass

    @staticmethod
    @abstractmethod
    def url() -> str:
        pass


class MainChannelLink(_BaseLinkButton):
    @staticmethod
    def text() -> str:
        return text.MAIN_CHANNEL

    @staticmethod
    def url() -> str:
        return "https://t.me/binance_ru"


class SupportLink(_BaseLinkButton):
    @staticmethod
    def text() -> str:
        return text.SUPPORT

    @staticmethod
    def url() -> str:
        return f"https://t.me/{SUPPORT_BOT_TAG}"


class UserAgreementLink(_BaseLinkButton):
    @staticmethod
    def text() -> str:
        return text.AGREEMENT

    @staticmethod
    def url() -> str:
        return "https://telegra.ph/Soglashenie-dlya-otkrytiya-ECN-07-21"
