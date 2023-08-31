from .executor import Executor


class UserWallet:
    _EXECUTOR: Executor
    _USERID: int

    _authorized: bool = None

    def __init__(self, executor: Executor, userid: int):
        self._EXECUTOR = executor
        self._USERID = int(userid)

    @property
    def amout(self) -> int:
        return self._EXECUTOR.fetch(sql=f"SELECT amount FROM wallets WHERE userid={self._USERID};")[0] or 0

    @property
    def authorized(self) -> bool:
        self._authorized = self._EXECUTOR.fetch(
            f"SELECT EXISTS (SELECT userid FROM wallets WHERE userid={self._USERID})"
        )[0]

        return self._authorized

    def save_to_db(self):
        if (self._authorized is None) or self.authorized:
            return

        self._EXECUTOR.insert(sql=f"INSERT INTO wallets VALUES ({self._USERID})")
