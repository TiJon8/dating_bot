import sqlite3


class DatabaseAPI():

    def __init__(self, db_name: str):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
    
    def check_table(self):
        with self.connection:  
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER,
                                type_of_subscribe STRING NULL,
                                time_subscribe INTEGER NULL,
                                idempotence_key STRING

            )''')

    def isinstancedb(self, user_id: int):
        with self.connection: 
            return self.cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchone()



db_API = DatabaseAPI('subscribe.db')