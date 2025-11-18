import sqlite3

db_path = "gestion_budget_personnel.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE categories ADD COLUMN user_id INTEGER;")
    print("Colonne user_id ajoutée à categories.")
except sqlite3.OperationalError as e:
    print("Erreur ou colonne déjà existante :", e)

conn.commit()
conn.close()