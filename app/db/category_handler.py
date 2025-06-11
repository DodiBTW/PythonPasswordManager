import app.db.database_handler as database_handler

class CategoryHandler:
    def __init__(self):
        self.db_handler = database_handler.DatabaseHandler()

    def add_category(self, name):
        query = "INSERT OR IGNORE INTO categories (name) VALUES (?)"
        return self.db_handler.send_query(query, (name,))

    def get_all_categories(self):
        query = "SELECT * FROM categories"
        return self.db_handler.send_query(query)

    def get_category_by_name(self, name):
        query = "SELECT id FROM categories WHERE name = ?"
        result = self.db_handler.send_query(query, (name,))
        return result[0][0] if result else None

    def assign_category_to_password(self, password_id, category_id):
        query = "INSERT OR IGNORE INTO passwords_categories (password_id, category_id) VALUES (?, ?)"
        return self.db_handler.send_query(query, (password_id, category_id))

    def get_categories_for_password(self, password_id):
        query = """
            SELECT c.id, c.name FROM categories c
            JOIN passwords_categories pc ON c.id = pc.category_id
            WHERE pc.password_id = ?
        """
        return self.db_handler.send_query(query, (password_id,))