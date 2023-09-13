from abc import ABCMeta

from src.config import settings
from src.config.statements.buttons.text import ECN_POOL_UP, ECN_POOL_DOWN, ECN_POOL_SAME


class AbstractECNPoolType(metaclass=ABCMeta):
    text: str
    callback: str
    icon: str
    winning_ratio: int


class ECNPoolTypeUp(AbstractECNPoolType):
    text = ECN_POOL_UP
    callback = "poolup"
    icon = "🔼"
    winning_ratio = settings.POOL_UP_RATIO


class ECNPoolTypeDown(AbstractECNPoolType):
    text = ECN_POOL_DOWN
    callback = "pooldown"
    icon = "🔽"
    winning_ratio = settings.POOL_DOWN_RATIO


class ECNPoolTypeSame(AbstractECNPoolType):
    text = ECN_POOL_SAME
    callback = "poolsame"
    icon = "⏸"
    winning_ratio = settings.POOL_SAME_RATIO
