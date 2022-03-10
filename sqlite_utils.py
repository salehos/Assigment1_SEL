import sqlite3


class SqliteQueryUtils:
    database_path = 'test.db'

    def __init__(self):
        try:
            self._create_user_history_database()
        except:
            pass

    def _create_user_history_database(self):
        with sqlite3.connect(self.database_path) as conn:
            conn.execute("""
            CREATE TABLE USER_HISTORY
            (username TEXT PRIMARY KEY  NOT NULL,
            usage INT DEFAULT 0 NOT NULL)""")

    def increment_user_usage(self, username):
        with sqlite3.connect(self.database_path) as conn:
            user = conn.execute(f"""SELECT * from USER_HISTORY where username='{username}'""")
            user = list(user)
            if len(user) == 1:
                usage = user[0][1]
                conn.execute(f"""UPDATE USER_HISTORY set usage={usage + 1} WHERE username='{username}'""")
            elif len(user) == 0:
                conn.execute(f"""INSERT INTO USER_HISTORY (username, usage) \
                      VALUES ('{username}', {1})""")
            else:
                raise Exception("Multiple user found with this username!")


if __name__ == '__main__':
    database = SqliteQueryUtils()
    database.increment_user_usage("hello")
