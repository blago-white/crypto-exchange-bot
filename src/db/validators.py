from src.config.settings import PROMOCODE_ALLOWED_SYMBOLS, MAX_PROMOCODE_LENGTH


def promocode_valid(promocode: str) -> bool:
    return len(
        set(promocode) & PROMOCODE_ALLOWED_SYMBOLS
    ) == len(promocode) and len(promocode) <= MAX_PROMOCODE_LENGTH
