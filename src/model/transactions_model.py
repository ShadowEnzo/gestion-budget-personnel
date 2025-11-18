from .database import get_connection

class Transaction: 
    def __init__(self):
        self.conn = get_connection()

    def create_transaction(self, amount, category_id, date, label, type, user_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO transactions (amount, category_id, date, label, type, user_id) VALUES (?, ?, ?, ?, ?, ?)
""",(amount, category_id, date, label, type, user_id))
        self.conn.commit()
        return cursor.lastrowid
        
    def get_transaction(self, transaction_id,):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM transactions WHERE id = ?
""", (transaction_id,))
        return cursor.fetchone()
    
    def get_all_transactions(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM transactions WHERE user_id = ?
""", (user_id,))
        return cursor.fetchall()

    def update_transaction(self, transaction_id, amount, category_id, date, label, type, user_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE transactions SET amount = ?, category_id = ?, date = ?, label = ?, type = ?, user_id = ? WHERE id = ?
""",(amount, category_id, date, label, type, user_id, transaction_id))
        self.conn.commit()
        return cursor.rowcount
    
    def delete_transaction(self, transaction_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            DELETE FROM transactions WHERE id = ?
""", (transaction_id,))
        self.conn.commit()
        return cursor.rowcount



    