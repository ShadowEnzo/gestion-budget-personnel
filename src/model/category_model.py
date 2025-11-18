from .database import get_connection

class Category: 
    def __init__(self):
        self.conn = get_connection()

    def create_category(self, name, user_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO categories (name, user_id) VALUES (?, ?)
""", (name, user_id))
        self.conn.commit()
        cursor.close()

    def get_category_by_name(self, name, user_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM categories WHERE name = ? AND user_id = ?
""", (name, user_id))
        row = cursor.fetchone()
        cursor.close()
        return row
    
    def get_category_by_id(self, category_id, user_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM categories WHERE id = ? AND user_id = ?
""", (category_id, user_id))
        row = cursor.fetchone()
        cursor.close()
        return row
    
    def get_all_category(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM categories WHERE user_id = ? ORDER BY NAME
""", (user_id,))
        rows = cursor.fetchall()
        cursor.close()
        return rows
    
    def update_category(self, category_id, new_name, user_id):
        cursor = self.conn.cursor()
        cursor.execute("""
                UPDATE categories SET name = ? WHERE id = ? AND user_id = ?
""", (new_name, category_id, user_id))
        self.conn.commit()
        cursor.close()

    def delete_category(self, category_id, user_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            DELETE FROM categories WHERE id = ? AND user_id = ?
""", (category_id, user_id))
        self.conn.commit()
        cursor.close()




