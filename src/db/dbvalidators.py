from src.config import settings


def promocode_percentage_valid(percentage: str | int) -> bool:
    return settings.MAX_PROMOCODE_DISCOUNT_PERCENTAGE >= int(percentage) >= settings.MIN_PROMOCODE_DISCOUNT_PERCENTAGE


def promocode_valid(promocode: str) -> bool:
    return len(promocode) == settings.PROMOCODE_LENGTH
