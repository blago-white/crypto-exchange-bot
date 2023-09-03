from src.config.settings import MIN_DEPOSIT_AMOUNT_RUB, MAX_DEPOSIT_AMOUNT_RUB

TO_ACCOUNT_COMMAND = "Портфель 💼"

ECN_OPEN_COMMAND = "Открыть ECN 💹"

SEND_MONEY_COMMAND = u"Пополнить \u2935"

RECEIVE_MONEY_COMMAND = u"Вывести \u2934"

INSERT_PROMO = "🎁 Промокод"

MAIN_CHANNEL = "Мы в телеграм 😎"

SUPPORT = "Поддержка 👨‍💻"

AGREEMENT = "Соглашение 📜"

REPLENISHMENT_REQUEST_AMOUNT_INFO = (f"💰 Введите сумму пополнения от <b>{MIN_DEPOSIT_AMOUNT_RUB} RUB</b> до <b>"
                                     f"{MAX_DEPOSIT_AMOUNT_RUB} RUB</b>")

USER_AGREEMENT = "<b><em>Открывая ECN Cчёт вы соглашаетесь с соглашением по ссылке!</em></b>"

NEED_REPLENISHMENT = "<b>Сначала пополните кошелек!</b>"

NOT_CORRECT_AMOUNT = (f"<b>Сумма пополнения должна быть числом и в интервале от "
                      f"{MIN_DEPOSIT_AMOUNT_RUB} до {MAX_DEPOSIT_AMOUNT_RUB} рублей! 😡</b>")

ACCEPT_TRANSACTION = "✅ Подтвердить"

CANCEL_TRANSACTION = "❌ Отмена"

TRANSACTION_ACCEPTED = "<b>Успешная оплата!</b> 🟢"

TRANSACTION_CANCELED = "<b>Отмена транзакции! свяжитесь с тех. поддержкой - @Binance_Trade_Support_bot</b> 🚩"

TRANSACTION_BROKEN = "<b>❌ Транзакция не удалась, истекло время подтверждения! ❌</b>"
