from src.config import settings


def promocode_valid(promocode: str) -> bool:
    return len(
        set(promocode) & settings.PROMOCODE_ALLOWED_SYMBOLS
    ) == len(promocode) and len(promocode) <= settings.MAX_PROMOCODE_LENGTH
