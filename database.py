import sqlite3

class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                phone_number TEXT,
                vpn_period TEXT
            )
        ''')
        self.conn.commit()

    def add_user(self, user_id, username, first_name, last_name, phone_number, vpn_period=None):
        self.cursor.execute('''
            INSERT OR REPLACE INTO users (id, username, first_name, last_name, phone_number, vpn_period)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, username, first_name, last_name, phone_number, vpn_period))
        self.conn.commit()

    def close(self):
        self.conn.close()
