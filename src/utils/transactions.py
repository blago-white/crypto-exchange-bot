import datetime
import itertools
from dataclasses import dataclass, field


@dataclass(frozen=True)
class TransactionClient:
    id: int
    username: str


@dataclass(frozen=True)
class Transaction:
    client: TransactionClient
    amount: int
    id: int = field(default_factory=itertools.count().__next__, init=False)
    initialization_time: int = field(default=datetime.datetime.now(), init=False)
