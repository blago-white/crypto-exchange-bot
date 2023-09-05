from src.config import settings


def card_number_valid(card: str | int) -> bool:
    return len(str(card)) == 16 and str(card).isdigit()


def replenishment_amount_number_valid(replenishment_amount_text: str) -> bool:
    return (replenishment_amount_text.isdigit() and
            (settings.MAX_DEPOSIT_AMOUNT_RUB >= int(replenishment_amount_text) >= settings.MIN_DEPOSIT_AMOUNT_RUB))


def withdraw_amount_number_valid(withdraw_amount_text: str, wallet_amount: int) -> bool:
    return (withdraw_amount_text.isdigit() and
            (settings.MAX_WITHDRAW_AMOUNT_RUB >= int(withdraw_amount_text) >= settings.MIN_WITHDRAW_AMOUNT_RUB) and
            int(withdraw_amount_text) <= wallet_amount)
