from abc import ABCMeta, abstractmethod

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
        return "https://www.google.com/"


class SupportLink(_BaseLinkButton):
    @staticmethod
    def text() -> str:
        return text.SUPPORT

    @staticmethod
    def url() -> str:
        return "https://www.google.com/"
