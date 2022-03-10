import sqlite3


class SqliteQueryUtils:
    database_path = 'test.db'

    def __init__(self):
        self._create_user_history_database()

    def _execute_query(self, query_string):
        conn = sqlite3.connect(self.database_path)
        conn.execute(query_string)
        conn.close()

    def _create_user_history_database(self):
        self._execute_query("""
        CREATE TABLE USER_HISTORY
        (ID INT PRIMARY KEY NOT NULL,
        USERNAME TEXT NOT NULL,
        USAGE INT DEFAULT 0 NOT NULL""")
