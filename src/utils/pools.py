from abc import ABCMeta

from src.config.statements.buttons.text import ECN_POOL_UP, ECN_POOL_DOWN, ECN_POOL_SAME
from src.db.models import UserWallet


class AbstractECNPoolType(metaclass=ABCMeta):
    text: str
    callback: str
    icon: str


class ECNPoolTypeUp(AbstractECNPoolType):
    text = ECN_POOL_UP
    callback = "poolup"
    icon = "🔼"


class ECNPoolTypeDown(AbstractECNPoolType):
    text = ECN_POOL_DOWN
    callback = "pooldown"
    icon = "🔽"


class ECNPoolTypeSame(AbstractECNPoolType):
    text = ECN_POOL_SAME
    callback = "poolsame"
    icon = "⏸"


def pool_is_successfully(pool_type: AbstractECNPoolType, currency_rate_delta: float) -> bool:
    return ((pool_type == ECNPoolTypeDown and currency_rate_delta < 0) or
            (pool_type == ECNPoolTypeUp and currency_rate_delta > 0) or
            (pool_type == ECNPoolTypeSame and currency_rate_delta == 0))


def get_pool_result_description(pool_currency_rate_delta: float) -> str:
    return "выросла" if (pool_currency_rate_delta > 0) else (
        "упала" if (pool_currency_rate_delta < 0) else "не изменилась"
    )


def get_pool_type_by_code(code: str) -> AbstractECNPoolType:
    return dict(
        poolup=ECNPoolTypeUp,
        pooldown=ECNPoolTypeDown,
        poolsame=ECNPoolTypeSame
    )[code]


def apply_pool_result_to_wallet(pool_status: bool, pool_value: float, user_wallet: UserWallet) -> None:
    if pool_status:
        return user_wallet + abs(pool_value)

    user_wallet - abs(pool_value)
