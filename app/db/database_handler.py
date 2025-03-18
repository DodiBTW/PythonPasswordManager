import sqlite3
from app.db import database_config

class DatabaseHandler:
    def __init__(self):
        self.db_path = database_config.DATABASE

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def send_query(self, query, params=None):
        if params:
            connection = self.get_connection()
            cursor = connection.cursor()
            result = cursor.execute(query, params)
            connection.commit()
            connection.close()
            return result
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        connection.close()
        return result