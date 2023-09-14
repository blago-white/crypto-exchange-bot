from .buttons import text
from .. import settings

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
<code>{settings.CARD_FOR_USERS_DEPOSITS_NUMBER} {settings.CARD_FOR_USERS_DEPOSITS_BANK}</code>
💸 Сумма пополнения: <b>{'{amount}'} RUB</b>
— — — — — — — — — — — —
‼ Важно пополнить сумму без дробных частей (копеек)

‼ У вас есть 15 минут на оплату, после чего платеж не будет зачислен. После оплаты прислать чек в формате PDF, 
или фотографией в поддержку (<b>прямо в этот чат!</b>).
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
✅ Минимальная сумма для вывода: <b>{settings.MIN_WITHDRAW_AMOUNT_RUB} RUB</b> 
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

for currency in settings.SUPPORTED_CURRENCIES:
    ECN_CURRENCIES_RATE += (f"🔸 {currency.capitalize()}/{settings.ALTERNATIVE_CURRENCY} - "
                            f"<b>{'{' + currency.lower() + '}'} {settings.ALTERNATIVE_CURRENCY}</b> "
                            f"(~ <em>{'{' + currency.lower() + 'rubrate}'} RUB</em>)\n")

ECN_CURRENCIES_RATE += "\n<em>Данные о криптовалюте представлены - Coinbase, о валюте Morningstar</em>"

ECN_POOL_VOLUME_INPUT_INFO = f"""
🔸 <b>{'{currency}'} / {settings.ALTERNATIVE_CURRENCY}</b>
💸 Баланс: <b>{'{user_wallet_amount}'}</b>

<em>Введите сумму пула</em>
"""

ECN_POOL_TYPE_SELECT = f"""
🔸 <b>{'{currency}'}/{settings.ALTERNATIVE_CURRENCY}</b>
💸 Стоимость: <b>{'{currency_rate}'} {settings.ALTERNATIVE_CURRENCY} ~</b> <em>({'{currency_rate_rub}'} RUB)</em>

Повышение x2
Не изменится x10
Понижение x2
"""

POOL_STARTED = f"💹 <b>Пул на {'{pool_amount_rub}'} RUB начат!</b>\n\n⏰ <b>{'{elapsed_time}'}/30 секунд</b>"

POOL_ENDED_INFO = f"""
{'{pool_type}'}

💱 Валюта: <b>{'{currency}'}</b>
💰 Сумма пула: <b>{'{pool_amount_rub}'} RUB</b>

💸 Начальная цена: <b>{'{start_currency_rate_usd}'} {settings.ALTERNATIVE_CURRENCY}</b> 
<em>(~ {'{start_currency_rate_rub}'} RUB)</em>

💵 Цена сейчас: <b>{'{end_currency_rate_usd}'} {settings.ALTERNATIVE_CURRENCY}</b> 
<em>(~ {'{end_currency_rate_rub}'} RUB)</em>

⏰ Время: <em><b>{settings.POOL_DURATION}/{settings.POOL_DURATION} Секунд</b></em>
"""

POOL_ENDED_SUCCESSFULLY = f"""
{'{pool_type_icon}'} За {settings.POOL_DURATION} секунд цена {'{pool_result}'}!
 
✅ Ваш пул удачный, <b>+{'{pool_amount_rub}'} RUB</b>
💸 Баланс: <b>{'{wallet_amount}'} RUB</b>
"""

POOL_ENDED_UNSUCCESSFULLY = f"""
{'{pool_type_icon}'} За {settings.POOL_DURATION} секунд цена {'{pool_result}'}!
 
❌ Ваш пул неудачный, <b>-{'{pool_amount_rub}'} RUB</b>
💸 Баланс: <b>{'{wallet_amount}'} RUB</b>
"""

WALLET_VERIFICATION_REQUIRED = f"""
{'{firstname}'}, для вывода средств, Вам потребуется пройти процедуру верификации на нашей платформe.

📄 Верификация - подтверждение личности, для проверки на живого человека. Это сделано после многочисленных атак от хакеров из различных мировых преступных группировок.

🪪 Для того чтобы пройти верификацию, достаточно сделать следующее:
1) Сообщить оператору, отправив сюда /{text.VERIFY_COMMAND} если вы готовы пройти верификацию.
2) Совершить депозит в размере 3.000₽
3) Приложить screenshot об совершении депозита в поддержку

👤 После всех выше действий, ожидать дальнейшей инструкции от оператора.
"""

WAIT_FOR_PAYMENT_VERIFICATION = ("⚡ Пользователь <b>@{usertag}</b> (<code>{userid}</code>) запросил верификацию счета, "
                                 "если он пополнит счет на <b>3000 рублей</b>, подтвердите")

ADMIN_USER_WALLET_VERIFIED = "✅ Вы верифицировали кошелек пользователя <code>{userid}</code>!"

ADMIN_READY_FOR_ANSWERING_FOR_CLIENT = ("💬 <em>@{adminname}, теперь вы можете ответить пользователю,</em> "
                                        f"а когда закончите отправьте /{text.ADMIN_END_ANSWERING_COMMAND}")

SUPPORT_CHAT_TEXT_MESSAGE_CREDENTIALS_TEMPLATE = ("<b>Пользователь @{username} отправил в поддержку:</b>\n"
                                                  "<code>{usermessage}</code>")

SUPPORT_CHAT_MEDIA_MESSAGE_CREDENTIALS_TEMPLATE = "<b>Пользователь @{username} отправил в поддержку файл</b>"

ANSWER_FROM_SUPPORT_FOR_USER_TEMPLATE = "‼ <b>Вам ответил администратор:</b>\n{adminanswer}"

PROMOS_LIST_TEMPLATE = """
💯 Созданные промокоды:
{promocodes}
"""

PROMO_LIST_ITEM_TEMPLATE = "🔸 <code>{promocode}</code> - <b>{discount}%</b>\n"
