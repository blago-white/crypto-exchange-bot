from .executor import Executor


def promo_code_exists(executor: Executor, promocode: str) -> bool:
    return executor.fetch(sql=f"SELECT EXIST (SELECT * FROM promocodes WHERE promocode='{promocode}'")
