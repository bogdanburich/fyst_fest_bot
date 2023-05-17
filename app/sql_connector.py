import sqlite3

from config import BD_FILE


class SqlConnector:
    def __init__(cls):
        pass

    @classmethod
    def insert_user_id(cls, user_id: int, state: str = ""):
        with sqlite3.connect(BD_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''INSERT
                           INTO users(user_id, state)
                           VALUES({user_id}, '{state}');''')
            conn.commit()
            cursor.close()

    @classmethod
    def get_user_id(cls, user_id: str):
        with sqlite3.connect(BD_FILE) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(f'''SELECT user_id, state
                            FROM users WHERE user_id = {user_id};''')
                return cursor.fetchone()
            finally:
                cursor.close()

    @classmethod
    def get_users_id(cls):
        with sqlite3.connect(BD_FILE) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''SELECT user_id FROM users;''')
                return cursor.fetchone()
            finally:
                cursor.close()
