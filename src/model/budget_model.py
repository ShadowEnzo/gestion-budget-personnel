from database import get_connection

class Budget:
    def __init__(self):
        self.conn = get_connection()

    def create_budget(self, amount, category_id, user_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO budgets (amount, category_id, user_id) VALUES (?, ?, ?)
""",(amount, category_id, user_id))
        self.conn.commit()

    def get_budgets(self): 
        cursor = self.conn.cursor()
        cursor.execute("""
SELECT * FROM budgets
""")
        return cursor.fetchall()
    
    def update_budget(self, budget_id, amount = None, category_id=None, user_id=None):
        cursor = self.conn.cursor()
        query = "UPDATE budgets SET "
        params = []
        if amount is not None:
            query += "amount = ?, "
            params.append(amount)
        if category_id is not None:
            query += "category_id = ?, "
            params.append(category_id)
        if user_id is not None:
            query += "user_id = ?, "
            params.append(user_id)
        query = query.rstrip(", ") + " WHERE id = ?"
        params.append(budget_id)
        cursor.execute(query, tuple(params))
        self.conn.commit()

    def delete_budget(self, budget_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            DELETE FROM budgets WHERE id = ?
""", (budget_id, ))
        self.conn.commit()