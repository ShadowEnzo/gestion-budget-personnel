import sqlite3 as sq
conn = sq.connect("gestion_budget_personnel.db")
c = conn.cursor()
c.execute("""CREATE TABLE if not exists users (
          id INTEGER PRIMARY kEY AUTOINCREMENT,
          username TEXT UNIQUE NOT NULL,
          password TEXT NOT NULL
)""")

# c.execute("""INSERT INTO users (username, password) VALUES (
#         "Enzo", "enzo123"
# )""")

c.execute("""CREATE TABLE if not exists categories (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT UNIQUE NOT NULL
)""")

c.execute("""CREATE TABLE if not exists transactions (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          amount REAL NOT NULL,
          category_id INTEGER,
          date TEXT NOT NULL,
          label TEXT,
          type TEXT NOT NULL,
          user_id INTEGER,
          FOREIGN KEY (category_id) REFERENCEs categories(id),
          FOREIGN KEY (user_id) REFERENCES users(id)
)""")

c.execute("""CREATE TABLE if not exists budgets(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          amount REAL NOT NULL,
          category_id INTEGER,
          user_id INTEGER,
          FOREIGN KEY (category_id) REFERENCES categories(id),
          FOREIGN KEY (user_id) REFERENCES users(id)
)""")
# inserer les données dans la base de donnée
conn.commit()
conn.close()

def get_connection():
    return sq.connect("gestion_budget_personnel.db")