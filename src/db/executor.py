from ._connection import DBConnector
from ..config import settings


class Executor:
    def __init__(self):
        self._CONNECTOR = DBConnector(dbconfig=settings.AppConfig().db)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        connection = self._CONNECTOR.get_connection()
        connection.commit()
        connection.close()

    def fetchall(self, sql: str, *params) -> list[tuple]:
        cursor = self._execute(*params, sql=sql)

        data = cursor.fetchall()
        cursor.close()

        return data

    def fetch(self, sql: str, *params) -> list[tuple]:
        cursor = self._execute(*params, sql=sql)

        data = cursor.fetchone()
        cursor.close()

        return data

    def insert(self, sql: str, *params) -> None:
        self._execute(*params, sql=sql).close()

    def _execute(self, sql: str, *params):
        cursor = self._CONNECTOR.get_new_connection().cursor()

        cursor.execute(sql.format(*params))

        return cursor
