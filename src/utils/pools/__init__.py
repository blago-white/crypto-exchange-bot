from dataclasses import dataclass

from .types import AbstractECNPoolType


@dataclass(frozen=True)
class ECNPool:
    pool_type: AbstractECNPoolType
    pool_currency: str
    pool_amount: int
