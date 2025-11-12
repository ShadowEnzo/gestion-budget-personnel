# import sys
# from PySide6.QtWidgets import QApplication
# from model.dashboard_model import DashboardModel
# from view.dashboard_view import DashboardView
# from controller.dashboard_controller import DashboardController

# if __name__ == "__main__":
#     app = QApplication([])
#     # app.setStyleSheet("""
#     #     QWidget {
#     #         background-color: #f5f6fa;
#     #         font-family: Arial;
#     #         font-size: 15px;
#     #     }
#     #     QLabel {
#     #         color: #222f3e;
#     #         font-weight: bold;
#     #     }
#     #     QPushButton {
#     #         background-color: #54a0ff;
#     #         color: white;
#     #         border-radius: 8px;
#     #         padding: 8px 16px;
#     #     }
#     #     QPushButton:hover {
#     #         background-color: #2e86de;
#     #     }
#     #     QListWidget {
#     #         background: #fff;
#     #         border: 1px solid #dfe4ea;
#     #         border-radius: 6px;
#     #     }
#     # """)
#     model = DashboardModel()
#     view = DashboardView()
#     controller = DashboardController(model, view)
#     view.resize(800, 600)
#     view.show()
#     sys.exit(app.exec())

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