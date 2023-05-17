import sqlite3

from config import BD_FILE


class SqlConnector:
    def __init__(self):
        pass

    @classmethod
    def insert_user_id(self, user_id: int, state: str = ""):
        with sqlite3.connect(BD_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''INSERT
                           INTO users(user_id, state)
                           VALUES({user_id}, '{state}');''')
            conn.commit()
            cursor.close()

    @classmethod
    def get_user_id(self, user_id: str):
        with sqlite3.connect(BD_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''SELECT user_id, state
                           FROM users WHERE user_id = {user_id};''')
            user_info = cursor.fetchone()
            cursor.close()
        return user_info

    @classmethod
    def get_users_id(self):
        with sqlite3.connect(BD_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT user_id FROM users;''')
            user_info = cursor.fetchone()
            cursor.close()
        return user_info
