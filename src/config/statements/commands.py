__all__ = ["START_COMMAND_TEXT"]

_PROFILE_TEMPLATE = """
💹Инвестиицонный портфель!
    
💸Баланс: <b>{amount} RUB</b>
🆔Пользовательский ID: {userid}
    
🌍Активность за последние 10 минут - <em>{online} человек</em> 
"""

START_COMMAND_TEXT = _PROFILE_TEMPLATE.format(amount=0, userid="{userid}", online="{online}")
