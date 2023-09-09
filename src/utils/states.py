from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.base import StorageKey

from src.config.settings import BOT_ID


class Replenishment(StatesGroup):
    choosing_payment_amount = State()
    wait_payment_confirmation = State()


class Withdraw(StatesGroup):
    choosing_withdraw_amount = State()
    choosing_withdraw_card = State()


class EnteringPromocode(StatesGroup):
    entering_promocode = State()


class CurrencyPool(StatesGroup):
    pool_volume_input = State()
    pool_type_input = State()


class WalletVerification(StatesGroup):
    wait_for_confirmation = State()


class AdminAddPromocode(StatesGroup):
    entering_withdraw_amount = State()


def get_user_stortage_key(userid: int) -> StorageKey:
    return StorageKey(bot_id=BOT_ID, chat_id=userid, user_id=userid)
