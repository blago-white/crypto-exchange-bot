from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.db.models import UserWallet
from . import ECNPool
from .types import AbstractECNPoolType, ECNPoolTypeUp, ECNPoolTypeDown, ECNPoolTypeSame


def pool_is_successfully(pool_type: AbstractECNPoolType, currency_rate_delta: float) -> bool:
    return ((pool_type == ECNPoolTypeDown and currency_rate_delta < 0) or
            (pool_type == ECNPoolTypeUp and currency_rate_delta > 0) or
            (pool_type == ECNPoolTypeSame and currency_rate_delta == 0))


async def get_pool(callback: CallbackQuery, user_state: FSMContext) -> ECNPool:
    pool_type, pool_data = get_pool_type_by_code(callback.data), await user_state.get_data()

    pool_currency, pool_amount_rub = (str(pool_data.get("currency")),
                                      calc_winning_amount(float(pool_data.get("amount_rub")), pool_type))

    return ECNPool(pool_type=pool_type, pool_currency=pool_currency, pool_amount=pool_amount_rub)


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


def replenish_pool_winning_amount(pool_value: float, user_wallet: UserWallet) -> None:
    if pool_status:
        return user_wallet + abs(pool_value)


def calc_winning_amount(pool_value: float, pool_type: ECNPoolTypeUp) -> float:
    return pool_value * pool_type.winning_ratio
