from database import get_connection

class Category: 
    def __init__(self):
        self.conn = get_connection()

    def create_category(self, name):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO categories (name) VALUES (?)
""",(name,))
        self.conn.commit()
        cursor.close()

    def get_category_by_name(self, name):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM categories WHERE name = ?
""", (name,)
        )
        row = cursor.fetchone()
        cursor.close()
        return row
    
    def get_category_by_id(self, category_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM categories WHERE id = ?
""", (category_id,)
        )
        rows = cursor.fetchone()
        cursor.close()
        return rows
    
    def get_all_category(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM categories ORDER BY NAME
"""
        )
        rows = cursor.fetchall()
        cursor.close()
        return rows
    
    def update_category(self, category_id, new_name):
        cursor = self.conn.cursor()
        cursor.execute("""
                UPDATE categories SET name = ? WHERE id = ?

""", (new_name, category_id))
        self.conn.commit()
        cursor.close()

    def delete_category(self, category_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            DELETE FROM categories WHERE id = ?
""", (category_id,))
        self.conn.commit()
        cursor.close()




