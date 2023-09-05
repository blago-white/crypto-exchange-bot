from src.config.settings import (MIN_DEPOSIT_AMOUNT_RUB,
                                 MAX_DEPOSIT_AMOUNT_RUB,
                                 MIN_WITHDRAW_AMOUNT_RUB,
                                 MAX_WITHDRAW_AMOUNT_RUB)

REPLENISHMENT_REQUEST_AMOUNT_INFO = (f"💰 Введите сумму пополнения от <b>{MIN_DEPOSIT_AMOUNT_RUB} RUB</b> до <b>"
                                     f"{MAX_DEPOSIT_AMOUNT_RUB} RUB</b>")

USER_AGREEMENT = "<b><em>Открывая ECN Cчёт вы соглашаетесь с соглашением по ссылке!</em></b>"

NEED_REPLENISHMENT = f"<b>Сначала пополните кошелек! Сумма на счете должны быть больше {MIN_DEPOSIT_AMOUNT_RUB} RUB</b>"

NOT_CORRECT_REPLENISHMENT_AMOUNT = (f"<b>Сумма пополнения должна быть числом и в интервале от "
                                    f"{MIN_DEPOSIT_AMOUNT_RUB} до {MAX_DEPOSIT_AMOUNT_RUB} рублей!</b>")

NOT_CORRECT_WITHDRAW_AMOUNT = (f"<b>Сумма для вывода должна быть числом меньше суммы вашего счета в интервале от "
                               f"{MIN_WITHDRAW_AMOUNT_RUB} до {MAX_WITHDRAW_AMOUNT_RUB} рублей!</b>")

NOT_CORRECT_CARD_REQUISITES = "⚠ <b>Вы ввели несуществующий номер карты!</b>"

TRANSACTION_ACCEPTED = "<b>Вы пополнили счет на {amount} RUB!</b> 🟢"

TRANSACTION_CANCELED = ("<b>Отмена транзакции на {amount} RUB! свяжитесь с тех. поддержкой - "
                        "@Binance_Trade_Support_bot</b> 🚩")

TRANSACTION_BROKEN = "<b>❌ Транзакция не удалась, истекло время подтверждения! ❌</b>"

WITHDRAW_REQUEST_SAVED = """
<em>Заявка успешна создана✅
Ожидайте оплату в течение, 24 часов с момента получения этого сообщения.</em>
"""

