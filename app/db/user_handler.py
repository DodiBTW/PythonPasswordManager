import app.db.database_handler as database_handler
import app.db.logs_handler as logs_handler
import app.db.passwords_handler as passwords_handler
import bcrypt
from datetime import datetime

class UserHandler:
    def __init__(self):
        self.db_handler = database_handler.DatabaseHandler()
        self.logs_handler = logs_handler.LogsHandler()
    def user_exists(self, username):
        query = f"SELECT * FROM users WHERE username = '{username}'"
        return len(self.db_handler.send_query(query)) > 0
    def register(self, user_id, password, key):
        query = "INSERT INTO users (username, password, key_hash) VALUES (?, ?, ?)"
        return self.db_handler.send_query(query, (user_id, password, key))
    def login(self, user_id, password):
        query = f"SELECT * FROM users WHERE id = '{user_id}'"
        result = self.db_handler.send_query(query)
        if result:
            encrypted_password = result[0][2]
            if not bcrypt.checkpw(password.encode(), encrypted_password.encode('utf-8')):
                return False
            self.logs_handler.add_log(user_id, 'Login', 'Logged in')
        else:
            self.logs_handler.add_log(user_id, 'Login', 'Failed login')
        return result
    def get_user_id(self, username):
        query = f"SELECT id FROM users WHERE username = '{username}'"
        return self.db_handler.send_query(query)[0][0]
    def delete_user(self, user_id):
        # Delete all passwords and logs associated with the user
        user_id = self.get_user_id(user_id)
        self.logs_handler.delete_logs(user_id)
        self.passwords_handler.delete_passwords(user_id)
        query = f"DELETE FROM users WHERE id = '{user_id}'"
        return self.db_handler.send_query(query)
    def get_password(self, user_id):
        query = f"SELECT password FROM users WHERE id = '{user_id}'"
        return self.db_handler.send_query(query)[0][0]
    def change_password(self, user_id, password):
        query = f"UPDATE users SET password = '{password}' WHERE id = '{user_id}'"
        return self.db_handler.send_query(query)
    def get_crypted_key(self, user_id):
        query = f"SELECT key_hash FROM users WHERE id = '{user_id}'"
        return self.db_handler.send_query(query)[0][0]