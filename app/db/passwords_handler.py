import app.db.logs_handler as logs_handler
import app.db.database_handler as database_handler
from app.db.category_handler import CategoryHandler

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
        self.logs_handler.add_log(user_id, site, 'Ajout mot de passe')
        query = "INSERT INTO passwords (user_id, username, site, password) VALUES (?,?,?,?)"
        params = (user_id, username, site, password)
        return self.db_handler.send_query(query, params)  # Now returns new password's ID
    def modify_site(self, user_id, username, site, password):
        query = "UPDATE passwords SET username = ?, password = ? WHERE user_id = ? AND site = ?"
        params = (username, password, user_id, site)
        self.logs_handler.add_log(user_id, site, 'Modification de site')
        return self.db_handler.send_query(query, params)
    def delete_password(self, user_id, site):
        query = "DELETE FROM passwords WHERE user_id = ? AND site = ?"
        params = (user_id, site)
        self.logs_handler.add_log(user_id, site, 'Suppression de mot de passe')
        return self.db_handler.send_query(query, params)
    def delete_passwords(self, user_id):
        query = "DELETE FROM passwords WHERE user_id = ?"
        params = (user_id,)
        return self.db_handler.send_query(query, params)
    def add_password_with_category(self, user_id, username, site, password, category_name):
        password_id = self.add_password(user_id, username, site, password)
        category_handler = CategoryHandler()
        category_handler.add_category(category_name)
        category_id = category_handler.get_category_by_name(category_name)
        category_handler.assign_category_to_password(password_id, category_id)
        return password_id