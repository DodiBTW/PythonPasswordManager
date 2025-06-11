import sqlite3
import os

class DatabaseHandler:
    def __init__(self):
        self.db_path = os.path.dirname(os.path.abspath(__file__)) + "/database.db"

    def send_query(self, query, params=()):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            if query.strip().upper().startswith("SELECT"):
                result = cursor.fetchall()
            else:
                conn.commit()
                result = cursor.rowcount
        finally:
            cursor.close()
            conn.close()
        return result