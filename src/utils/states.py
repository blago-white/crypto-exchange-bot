from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.base import StorageKey

from src.config.settings import BOT_ID


class Replenishment(StatesGroup):
    choosing_payment_amount = State()
    wait_payment_confirmation = State()


class Withdraw(StatesGroup):
    choosing_withdraw_amount = State()
    choosing_withdraw_card = State()


def get_user_stortage_key(userid: int) -> StorageKey:
    return StorageKey(bot_id=BOT_ID, chat_id=userid, user_id=userid)
