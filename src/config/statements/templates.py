from ..settings import (CARD_FOR_USERS_DEPOSITS_NUMBER,
                        CARD_FOR_USERS_DEPOSITS_BANK,
                        MIN_WITHDRAW_AMOUNT_RUB,
                        ALTERNATIVE_CURRENCY,
                        SUPPORTED_CURRENCIES)

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

ADMIN_PROMO_SAVED = """
✅<b> Новый промокод с названием <code>{promo_title}</code> на скидку {discount}% создан успешно!</b>✅
"""

PROMOCODE_APPLIED = "✅ <em>Промокод успешно применен, для вас действует скидка <b>{discount}%</b> на пополнение</em>"

PROMOCODE_WILL_BE_USED = ("✨ При пополнении будет использован промокод, <em>вы получите на {discount} процентов "
                          "больше чем положили</em>")

ECN_CURRENCIES_RATE = f"""
<b>Выберите актив 👇</b>

"""

for currency in SUPPORTED_CURRENCIES:
    ECN_CURRENCIES_RATE += (f"🔸 {currency.capitalize()}/{ALTERNATIVE_CURRENCY} - "
                            f"<b>{'{' + currency.lower() + '}'} {ALTERNATIVE_CURRENCY}</b> "
                            f"(~ <em>{'{' + currency.lower() + 'rubrate}'} RUB</em>)\n")

ECN_CURRENCIES_RATE += "\n<em>Данные о криптовалюте представлены - Coinbase, о валюте Morningstar</em>"

ECN_POOL_VOLUME_INPUT_INFO = f"""
🔸 <b>{'{currency}'} / {ALTERNATIVE_CURRENCY}</b>
💸 Баланс: <b>{'{user_wallet_amount}'}</b>

<em>Введите сумму пула</em>
"""
