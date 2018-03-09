import psycopg2
from psycopg2.extras import DictCursor


class PostgresDb:

    def __init__(self, connection_str, adapter=None):
        if not adapter:
            self.adapter = psycopg2
        else:
            self.adapter = adapter
        self.connection_str = connection_str
        self.db_connection = None
        self._connected = False

    def execute_query(self, query, params=None, disconnect=True, dict_cursor=False):
        params = params or ()
        if not self._connected:
            self._connect()
        try:
            if dict_cursor:
                cursor = self.db_connection.cursor(cursor_factory=DictCursor)
            else:
                cursor = self.db_connection.cursor()
            with self.db_connection:
                cursor.execute(query, params)
                return cursor.fetchall()
        finally:
            if cursor:
                cursor.close()
            if disconnect:
                self._disconnect()

    def execute_non_query(self, query, params=None, disconnect=True):
        params = params or ()
        if not self._connected:
            self._connect()
        try:
            cursor = self.db_connection.cursor()
            with self.db_connection:
                cursor.execute(query, params)
        finally:
            if cursor:
                cursor.close()
            if disconnect:
                self._disconnect()

    def run_scalar(self, query, params=None, disconnect=True):
        results = self.execute_query(query, params, disconnect)
        return results[0][0]

    def _connect(self):
        self.db_connection = self.adapter.connect(self.connection_str)
        self._connected = True

    def _disconnect(self):
        self.db_connection.close()
        self._connected = False
