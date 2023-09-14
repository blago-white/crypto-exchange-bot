import random
import string

from src.config.settings import PROMOCODE_LENGTH
from src.config.statements import templates
from src.db import models
from src.db.executor import Executor


def generate_promocode_title() -> str:
    return ''.join(random.sample(string.ascii_letters + string.digits, PROMOCODE_LENGTH))


def save_promocode(executor: Executor, discount: int) -> str:
    promo_title = generate_promocode_title()
    models.Promocode(
        executor=executor, promocode=promo_title
    ).save_promocode(discount=int(discount))

    return promo_title


def get_promocodes_list(promocodes: list[tuple[str, int]]) -> str:
    return templates.PROMOS_LIST_TEMPLATE.format(
        promocodes="".join([templates.PROMO_LIST_ITEM_TEMPLATE.format(
            promocode=promocode, discount=discount
        ) for promocode, discount in promocodes])
    )
