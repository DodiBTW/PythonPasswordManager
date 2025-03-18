import app.db.logs_handler as logs_handler
import app.db.database_handler as database_handler
from datetime import datetime
from cryptography.fernet import Fernet

class PasswordsHandler:
    def __init__(self, key):
        self.db_handler = database_handler.DatabaseHandler()
        self.logs_handler = logs_handler.LogsHandler()
        self.key = key
    def password_exists(self, user_id, site):
        query = f"SELECT * FROM passwords WHERE user_id = {user_id} AND site = '{site}'"
        return len(self.db_handler.send_query(query)) > 0
    def get_passwords(self, user_id):
        query = f"SELECT * FROM passwords WHERE user_id = {user_id}"
        return self.db_handler.send_query(query)
    def get_password(self, user_id, site):
        query = f"SELECT password FROM passwords WHERE user_id = {user_id} AND site = '{site}'"
        return self.db_handler.send_query(query)
    def add_password(self, user_id, username, site, password):
        self.logs_handler.add_log(user_id, site, 'Added password')
        query = "INSERT INTO passwords (user_id, username, site, password) VALUES (?,?,?,?)"
        params = (user_id, username, site, password)
        return self.db_handler.send_query(query, params)
    def modify_site(self, user_id, username,site, password):
        query = f"UPDATE passwords SET username = '{username}', password = '{password}' WHERE user_id = {user_id} AND site = '{site}'"
        self.logs_handler.add_log(user_id, site, 'Modified site')
        return self.db_handler.send_query(query)
    def delete_password(self, user_id, site):
        query = f"DELETE FROM passwords WHERE user_id = {user_id} AND site = '{site}'"
        self.logs_handler.add_log(user_id, site, 'Deleted password')
        return self.db_handler.send_query(query)
    def delete_passwords(self, user_id):
        query = f"DELETE FROM passwords WHERE user_id = {user_id}"
        return self.db_handler.send_query(query)