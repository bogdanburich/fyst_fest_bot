import sqlite3

from config import FYST_FEST_DB


class SqlConnector:

    @classmethod
    def __insert_methos(cls, query):
        with sqlite3.connect(FYST_FEST_DB) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            cursor.close()

    @classmethod
    def __select_method(cls, query):
        with sqlite3.connect(FYST_FEST_DB) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query)
                return cursor.fetchone()
            finally:
                cursor.close()

    @classmethod
    def create_database(cls, data_base: str, script_file: str) -> None:
        with sqlite3.connect(data_base) as conn:
            cursor = conn.cursor()
            with open(script_file, "r") as f:
                script = f.read()
                cursor.executescript(script)
                conn.commit()
                cursor.close()

    @classmethod
    def insert_user_id(cls, user_id: int, state: str = "") -> None:
        print(user_id)
        query = f'''INSERT INTO users(user_id, state)
                 VALUES({user_id}, '{state}');'''
        cls.__insert_methos(query)

    @classmethod
    def get_user_id(cls, user_id: str) -> tuple:
        query = f'''SELECT user_id, state
                    FROM users WHERE user_id = {user_id};'''
        return cls.__select_method(query)

    @classmethod
    def get_users_id(cls) -> tuple:
        query = '''SELECT user_id FROM users;'''
        return cls.__select_method(query)

    @classmethod
    def set_user_state(cls, user_id: int, state: bool):
        query = f'''UPDATE users SET state = {state}
                    WHERE user_id = {user_id};'''
        cls.__insert_methos(query)
