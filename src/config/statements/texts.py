from src.config import settings
from .buttons.text import NEW_PROMO_COMMAND

REPLENISHMENT_REQUEST_AMOUNT_INFO = (
    f"💰 Введите сумму пополнения от <b>{settings.MIN_DEPOSIT_AMOUNT_RUB} RUB</b> до "
    f"<b>{settings.MAX_DEPOSIT_AMOUNT_RUB} RUB</b>"
)

USER_AGREEMENT = "<b><em>Открывая ECN Cчёт вы соглашаетесь с соглашением по ссылке!</em></b>"

NEED_REPLENISHMENT = (
    f"<b>Сначала пополните кошелек! Сумма на счете должны быть больше {settings.MIN_DEPOSIT_AMOUNT_RUB} RUB</b>"
)

NOT_CORRECT_REPLENISHMENT_AMOUNT = (
    f"<b>Сумма пополнения должна быть числом и в интервале "
    f"от {settings.MIN_DEPOSIT_AMOUNT_RUB} до {settings.MAX_DEPOSIT_AMOUNT_RUB} рублей!</b>"
)

NOT_CORRECT_WITHDRAW_AMOUNT = (f"<b>Сумма для вывода должна быть числом меньше суммы вашего счета в интервале от "
                               f"{settings.MIN_WITHDRAW_AMOUNT_RUB} до {settings.MAX_WITHDRAW_AMOUNT_RUB} рублей!</b>")

NOT_CORRECT_CARD_REQUISITES = "⚠ <b>Вы ввели несуществующий номер карты!</b>"

TRANSACTION_ACCEPTED = "<b>Вы пополнили счет на {amount} RUB!</b> 🟢"

TRANSACTION_CANCELED = ("<b>Отмена транзакции на {amount} RUB! свяжитесь с тех. поддержкой - "
                        f"@{settings.SUPPORT_BOT_TAG}</b> 🚩")

TRANSACTION_BROKEN = "<b>❌ Транзакция не удалась, истекло время подтверждения! ❌</b>"

WITHDRAW_REQUEST_SAVED = """
<em>Заявка успешна создана✅
Ожидайте оплату в течение, 24 часов с момента получения этого сообщения</em>
"""

ADMIN_ADD_PROMO_INFO = """
✅<em> Укажите процент скидки на пополнение для нового промокода</em>
"""

ADMIN_PROMO_NOT_CORRECT = f"""
❌<em> Неверный процент скидки, он должен быть 
не меньше <b>{settings.MIN_PROMOCODE_DISCOUNT_PERCENTAGE}%</b> и 
не больше <b>{settings.MAX_PROMOCODE_DISCOUNT_PERCENTAGE}%</b></em>
"""

ADMIN_COMMANDS_INFO = f"""
❓ <em>С помощью этого бота вы можете добавить промокод используя</em> /{NEW_PROMO_COMMAND}
"""

PROMOCODE_NOT_CORRECT = "❌ Введен <b>неверный промокод!</b>"

PROMOCODE_NOT_EXISTS = "❌ Введенный промокод <b>не существует!</b>"

POOL_VALUE_SMALL = f"❌ Минимальная сумма пула - {settings.MIN_ECN_POOL_VALUE} RUB"

NOT_ENOUGH_MONEY = "⛔ Недостаточно средств на счету!"
