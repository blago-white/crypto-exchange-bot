from src.config.settings import PROMOCODE_ALLOWED_SYMBOLS, MAX_PROMOCODE_LENGTH, MIN_DEPOSIT_AMOUNT_RUB, MAX_DEPOSIT_AMOUNT_RUB


def promocode_valid(promocode: str) -> bool:
    return len(
        set(promocode) & PROMOCODE_ALLOWED_SYMBOLS
    ) == len(promocode) and len(promocode) <= MAX_PROMOCODE_LENGTH


def replenishment_amount_number_valid(replenishment_amount_text: str) -> bool:
    return (replenishment_amount_text.isdigit() and
            (MAX_DEPOSIT_AMOUNT_RUB >= int(replenishment_amount_text) >= MIN_DEPOSIT_AMOUNT_RUB))
