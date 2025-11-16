
from .database import get_connection
import bcrypt

class User:
    def __init__(self):
        self.conn = get_connection()

# Verifier la connexion à la base de donnée
# if __name__ == "__main__":
#     try:
#         user = User()
#         cursor = user.conn.cursor()
#         cursor.execute("SELECT sqlite_version();")
#         version = cursor.fetchone()
#         print("Connexion réussie à SQLite)
#         user.conn.close()
#     except Exception as e:
#         print("Erreur de connexion :", e)

    def create_user(self, username, password):
        cursor = self.conn.cursor()
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute("""
            INSERT INTO users (username, password) VALUES (?, ?)
        """, (username, hashed))
        self.conn.commit()
          
# if __name__ == "__main__":
#     user = User()
#     username = "testuser"
#     password = "testpass"
#     try:
#         user.create_user(username, password)
#         print("Utilisateur créé avec succès.")
#     except Exception as e:
#         print("Erreur lors de la création de l'utilisateur :", e)

    def read_user(self, username):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM users  WHERE username = ?
        """, (username,))
        return cursor.fetchone()

    def verify_password(self, username, password):
        user = self.read_user(username)
        if user:
            hashed = user[2]
            if bcrypt.checkpw(password.encode('utf-8'), hashed):
                return user
        return None
    
# if __name__ == "__main__":
#     user = User()
#     username = "tesrtuse"
#     result = user.read_user(username)
#     if result:
#         print("Utilisateur trouvé :", result)
#     else:
#         print("Aucun utilisateur trouvé.")

    def update_user(self, user_id, new_username, new_password):
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE users SET username = ?, password = ? WHERE id = ?
""", (new_username, new_password, user_id))
        self.conn.commit()
        


    def delete_user(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            DELETE FROM users WHERE id = ?
""",(user_id,))
        self.conn.commit()
