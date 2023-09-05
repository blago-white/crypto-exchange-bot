from .executor import Executor


class UserWallet:
    _EXECUTOR: Executor
    _USERID: int

    _authorized: bool = None

    def __init__(self, executor: Executor, userid: int):
        self._EXECUTOR = executor
        self._USERID = int(userid)

    @property
    def amount(self) -> int:
        amount = self._EXECUTOR.fetch(sql=f"SELECT amount FROM wallets WHERE userid={self._USERID};")
        if amount is None:
            self._authorized = False
            return 0

        return amount[0]

    def deposit(self, amount: int):
        if amount <= 0:
            raise ValueError("Atempt to top up your account with a negative number")

        if not (self._authorized or self.authorized):
            return

        self._EXECUTOR.insert(
            sql=f"UPDATE wallets SET amount = amount + {int(amount)} WHERE userid={self._USERID}"
        )

    def withdraw(self, amount: int):
        if amount <= 0:
            raise ValueError("Atempt to top up your account with a negative number")

        if self._EXECUTOR.fetch(sql=f"SELECT amount FROM wallets WHERE userid={self._USERID}")[0] < amount:
            raise ValueError("Negative amount of the user's account")

        self._EXECUTOR.insert(
            sql=f"UPDATE wallets SET amount = amount - {int(amount)} WHERE userid={self._USERID}"
        )

    @property
    def authorized(self) -> bool:
        if self._authorized is None:
            self._authorized = self._EXECUTOR.fetch(
                f"SELECT EXISTS (SELECT userid FROM wallets WHERE userid={self._USERID})"
            )[0]

        return self._authorized

    def save_to_db(self):
        if (self._authorized is None) or self.authorized:
            return

        self._EXECUTOR.insert(sql=f"INSERT INTO wallets VALUES ({self._USERID})")
