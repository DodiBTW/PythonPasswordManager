from app.db.database_handler import DatabaseHandler
from datetime import datetime

class LogsHandler:
    def __init__(self ):
        self.db_handler = DatabaseHandler()
    def get_logs(self, user_id):
        query = f"SELECT * FROM logs WHERE user_id = {user_id} ORDER BY date DESC"
        return self.db_handler.send_query(query)
    def get_log(self, user_id, log_id):
        query = f"SELECT * FROM logs WHERE user_id = {user_id} AND id = {log_id}"
        return self.db_handler.send_query(query)
    def get_logs_by_site(self, user_id, site):
        query = f"SELECT * FROM logs WHERE user_id = {user_id} AND site = '{site}'"
        return self.db_handler.send_query(query)
    def add_log(self, user_id, site, log_type):
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = f"INSERT INTO logs (user_id, site, date, type) VALUES ({user_id}, '{site}', '{date}', '{log_type}')"
        return self.db_handler.send_query(query)
    def delete_log(self, user_id, log_id):
        query = f"DELETE FROM logs WHERE user_id = {user_id} AND id = {log_id}"
        return self.db_handler.send_query(query)
    def delete_logs(self, user_id):
        query = f"DELETE FROM logs WHERE user_id = {user_id}"
        return self.db_handler.send_query(query)