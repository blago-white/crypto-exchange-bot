import psycopg2

from src.config.config import DBConfig


class DBConnector:
    _DBCONFIG: DBConfig

    def __init__(self, dbconfig: DBConfig) -> None:
        self._DBCONFIG = dbconfig
        self._connection = self.get_new_connection()

    def get_new_connection(self):
        self._connection = psycopg2.connect(
                database=self._DBCONFIG.database,
                user=self._DBCONFIG.user,
                password=self._DBCONFIG.password
        )
        return self.get_connection()

    def get_connection(self):
        return self._connection

    def safe_close_connection(self):
        self._connection.commit()
        self._connection.close()
