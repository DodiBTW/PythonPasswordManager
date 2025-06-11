import app.db.logs_handler as logs_handler
import app.db.database_handler as database_handler
from datetime import datetime
from cryptography.fernet import Fernet

class PasswordShareHandler:
    def __init__(self, key):
        self.db_handler = database_handler.DatabaseHandler()
        self.logs_handler = logs_handler.LogsHandler()

    def share_password(self, site, username, password, hash,valid_until, user_id=None):
        query = "INSERT INTO password_share (site, username, password, valid_until, hash) VALUES (?, ?, ?, ?, ?)"
        params = (site, username, password, valid_until, hash)
        if user_id is not None:
            self.logs_handler.add_log(user_id, "Partage", "Partage de mot de passe")
        return self.db_handler.send_query(query, params)
    def get_shared_password(self, hash):
        query = f"SELECT * FROM password_share WHERE hash = '{hash}'"
        result = self.db_handler.send_query(query)
        if result:
            print("HELLO WORLD")
            date = datetime.strptime(result[0][4], '%Y-%m-%d %H:%M:%S.%f')
            if date < datetime.now():
                return None
            return result[0]
        return None
    def get_all_shared_passwords(self, hash):
        query = "SELECT * FROM password_share WHERE hash = ?"
        return self.db_handler.send_query(query, (hash,))