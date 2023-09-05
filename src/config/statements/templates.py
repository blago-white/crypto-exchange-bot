from ..settings import CARD_FOR_USERS_DEPOSITS_NUMBER, CARD_FOR_USERS_DEPOSITS_BANK, MIN_WITHDRAW_AMOUNT_RUB

USER_PROFILE_TEMPLATE = """
💹 Инвестиицонный портфель!
    
💸 Баланс: <b>{amount} RUB</b>
🆔 Пользовательский ID: {userid}
    
🌍 Активность за последние 10 минут - <em>{online} человек</em> 
"""

REPLENISHMENT_REQUEST_TEMPLATE = f"""
<b>Запрос на пополнение счета</b>
— — — — — — — — — — — —
💳 Реквизиты карты: 🇷🇺
<code>{CARD_FOR_USERS_DEPOSITS_NUMBER} {CARD_FOR_USERS_DEPOSITS_BANK}</code>
💸 Сумма пополнения: <b>{'{amount}'} RUB</b>
— — — — — — — — — — — —
‼ Важно пополнить сумму без дробных частей (копеек)

‼ У вас есть 15 минут на оплату, после чего платеж не будет зачислен. После оплаты прислать чек в формате PDF - 
@Binance_Trade_Support_bot
"""

USER_SEND_REQUEST_FOR_REPLENISHMENT_TEMPLATE = """
НОВЫЙ ЗАПРОС №{request_number} НА ПОПОЛНЕНИЕ ОТ @{username} OТ <code>{date}</code>
— — — — — — — — — — — —
Пользователь @{username} отправил запрос на пополнение на <b>{amount} RUB</b>
— — — — — — — — — — — —
<b>✅ Если сумма пришла и она равна запрошенной 
пользователем, подтвердите сделку

❌ Если сделка не состоялась отклоните</b>
"""

REQUEST_FOR_REPLENISHMENT_CANCELED_TEMPLATE = """
❌ ЗАПРОС №{request_number} НА ПОПОЛНЕНИЕ ОТ @{username} ОТ {date} ОТКЛОНЕН ❌
"""

REQUEST_FOR_REPLENISHMENT_CONFIRMED_TEMPLATE = """
✅ ЗАПРОС №{request_number} НА ПОПОЛНЕНИЕ ОТ @{username} ОТ {date} ПОДТВЕРЖДЕН ✅
"""

WITHDRAW_REQUEST_AMOUNT_INFO = f"""
✅ Минимальная сумма для вывода: <b>{MIN_WITHDRAW_AMOUNT_RUB} RUB</b> 
💸 Ваш баланс: {'{amount}'} RUB

💵 Введите сумму для вывода
"""

WITHDRAW_REQUEST_CARD_INFO = """
Сумма для вывода: <b>{amount} RUB</b>

💵 Введите реквизиты для вывода
"""
