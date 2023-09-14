from src.config import settings
from .buttons import text

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

TRANSACTION_CANCELED = "<b>Отмена транзакции на {amount} RUB! свяжитесь с тех. поддержкой</b> 🚩"

TRANSACTION_BROKEN = "<b>❌ Транзакция не удалась, истекло время подтверждения или пользователь ее отменил! ❌</b>"

WITHDRAW_REQUEST_SAVED = """
<em>Заявка успешна создана✅
Ожидайте оплату в течение, 24 часов с момента получения этого сообщения</em>
"""

ENTER_PROMO = "🎁 Введите ваш промокод!"

ADMIN_ADD_PROMO_INFO = """
✅<em> Укажите процент скидки на пополнение для нового промокода</em>
"""

ADMIN_PROMO_NOT_CORRECT = f"""
❌<em> Неверный процент скидки, он должен быть 
не меньше <b>{settings.MIN_PROMOCODE_DISCOUNT_PERCENTAGE}%</b> и 
не больше <b>{settings.MAX_PROMOCODE_DISCOUNT_PERCENTAGE}%</b></em>
"""

ADMIN_COMMANDS_INFO = f"""
❓ С помощью этого бота вы можете добавить промокод используя /{text.NEW_PROMO_COMMAND}
Просмотр всех промокодов - /{text.ADMIN_LIST_PROMOS}
"""

PROMOCODE_NOT_CORRECT = "❌ Введен <b>неверный промокод!</b>"

PROMOCODE_NOT_EXISTS = "❌ Введенный промокод <b>не существует!</b>"

POOL_VALUE_SMALL = f"❌ Минимальная сумма пула - {settings.MIN_ECN_POOL_VALUE} RUB"

NOT_ENOUGH_MONEY = "⛔ Недостаточно средств на счету!"

POOL_CURRENCY_DOES_NOT_EXISTS = "❌ <b>Неверно введена валюта, попробуйте еще раз!</b>"

TRADING_ENDED = "✅ <b>Спасибо, что торгуете с нами!</b>"

USER_VERIFY_SELF_WALLET = "✅ Ваш кошелек верифицирован!"

USER_VERIFICATION_PAYMENT_WAIT = "⚠ <em>Оператор уведомлен, вы можете отправлять чек в поддержку!</em>"

BOT_INFO = "❓ С помошью этого бота вы можете <b>зарабатывать на криптовалютах</b>"

SUPPORT_CHAT_OPENING_INFO = ("💬 Теперь вы можете отправить вопрос, "
                             "и/или файл, <b>сообщение увидят администраторы</b>\n\n"
                             "Вы можете использовать любые комманды этого бота, <b>они не будут отправлены</b>")

ADMIN_ANSWERING_ENDED = "✅ Вы закончили ответ клиенту"

TRANSACTION_CANCELED_BY_USER = "<b>Вы отменили транзакцию на пополнение счета</b> 🚩"
