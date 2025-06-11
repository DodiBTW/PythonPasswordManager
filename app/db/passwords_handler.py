import app.db.logs_handler as logs_handler
import app.db.database_handler as database_handler

class PasswordsHandler:
    def __init__(self, key):
        self.db_handler = database_handler.DatabaseHandler()
        self.logs_handler = logs_handler.LogsHandler()
        self.key = key
    def password_exists(self, user_id, site):
        query = "SELECT * FROM passwords WHERE user_id = ? AND site = ?"
        params = (user_id, site)
        return len(self.db_handler.send_query(query, params)) > 0
    def get_passwords(self, user_id):
        query = "SELECT * FROM passwords WHERE user_id = ?"
        params = (user_id,)
        return self.db_handler.send_query(query, params)
    def get_password(self, user_id, site):
        query = "SELECT password FROM passwords WHERE user_id = ? AND site = ?"
        params = (user_id, site)
        return self.db_handler.send_query(query, params)
    def add_password(self, user_id, username, site, password):
        self.logs_handler.add_log(user_id, site, 'Added password')
        query = "INSERT INTO passwords (user_id, username, site, password) VALUES (?,?,?,?)"
        params = (user_id, username, site, password)
        return self.db_handler.send_query(query, params)
    def modify_site(self, user_id, username, site, password):
        query = "UPDATE passwords SET username = ?, password = ? WHERE user_id = ? AND site = ?"
        params = (username, password, user_id, site)
        self.logs_handler.add_log(user_id, site, 'Modified site')
        return self.db_handler.send_query(query, params)
    def delete_password(self, user_id, site):
        query = "DELETE FROM passwords WHERE user_id = ? AND site = ?"
        params = (user_id, site)
        self.logs_handler.add_log(user_id, site, 'Deleted password')
        return self.db_handler.send_query(query, params)
    def delete_passwords(self, user_id):
        query = "DELETE FROM passwords WHERE user_id = ?"
        params = (user_id,)
        return self.db_handler.send_query(query, params)