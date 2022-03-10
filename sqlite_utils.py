import sqlite3

from constants import UserState


class SqliteQueryUtils:
    database_path = 'test.db'

    def __init__(self):
        try:
            self._create_user_history_database()
        except Exception as e:
            print(e)

    def _create_user_history_database(self):
        with sqlite3.connect(self.database_path) as conn:
            conn.execute("""
            CREATE TABLE USER_HISTORY
            (username TEXT PRIMARY KEY  NOT NULL,
            usage INT DEFAULT 0 NOT NULL,
            state INT DEFAULT 1 NOT NULL,
            pdf_file_ids TEXT DEFAULT '' Not NULL
            )""")  # pdf file ids are comma separated

    def increment_user_usage(self, username):
        with sqlite3.connect(self.database_path) as conn:
            user = conn.execute(f"""SELECT username, usage from USER_HISTORY where username='{username}'""")
            user = list(user)
            if len(user) == 1:
                usage = user[0][1]
                conn.execute(f"""UPDATE USER_HISTORY set usage={usage + 1} WHERE username='{username}'""")
            elif len(user) == 0:
                conn.execute(f"""INSERT INTO USER_HISTORY (username, usage) \
                      VALUES ('{username}', {1})""")
            else:
                raise Exception("Multiple user found with this username!")

    def add_file_id_for_merge(self, username, file_id):
        with sqlite3.connect(self.database_path) as conn:
            user = conn.execute(f"""SELECT username, pdf_file_ids from USER_HISTORY where username='{username}'""")
            user = list(user)
            if len(user) == 1:
                file_ids = user[0][1].split(",")
                if "" in file_ids:
                    file_ids.remove("")
                file_ids.append(file_id)
                file_ids = ",".join(file_ids)
                conn.execute(f"""UPDATE USER_HISTORY set pdf_file_ids='{file_ids}' WHERE username='{username}'""")
            elif len(user) == 0:
                file_ids = [file_id]
                file_ids = ",".join(file_ids)
                conn.execute(f"""INSERT INTO USER_HISTORY (username, pdf_file_ids) \
                      VALUES ('{username}', '{file_ids}')""")
            else:
                raise Exception("Multiple user found with this username!")

    def change_user_state(self, username, state):
        with sqlite3.connect(self.database_path) as conn:
            user = conn.execute(f"""SELECT username from USER_HISTORY where username='{username}'""")
            user = list(user)
            if len(user) == 1:
                conn.execute(f"""UPDATE USER_HISTORY set state={state}, pdf_file_ids='' WHERE username='{username}'""")
            elif len(user) == 0:
                conn.execute(f"""INSERT INTO USER_HISTORY (username) VALUES ('{username}')""")
            else:
                raise Exception("Multiple user found with this username!")

    def get_user_pdf_file_ids(self, username):
        with sqlite3.connect(self.database_path) as conn:
            user = conn.execute(f"""SELECT username, pdf_file_ids from USER_HISTORY where username='{username}'""")
            user = list(user)
            if len(user) == 1:
                return user[0][1].split(",")
            elif len(user) == 0:
                raise Exception("No user found!")
            else:
                raise Exception("Multiple user found with this username!")


if __name__ == '__main__':
    # tests
    database = SqliteQueryUtils()
    database.increment_user_usage("hello")
    database.add_file_id_for_merge("hello", "11245sdkgmksrmg")
    database.add_file_id_for_merge("hello", "sg1s5h1g5dth1")
    print(database.get_user_pdf_file_ids("hello"))
    database.change_user_state("hello", UserState.DONE.value)
    print(database.get_user_pdf_file_ids("hello"))
