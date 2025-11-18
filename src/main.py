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
# from PySide6.QtWidgets import QApplication
# from view.dashboard_view import DashboardView
# import sys

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = DashboardView(user_id=1)  # Remplace 1 par l'ID utilisateur voulu
#     window.show()
#     sys.exit(app.exec())



import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from controller.dashboard_controller import DashboardController
from view.login_view import LoginView
from view.signup_view import SignupView
from model.user_model import User

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion Budget Personnel")
        self.resize(1200, 800)
        self.user_model = User()
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.signup_view = SignupView()
        self.login_view = LoginView()
        self.dashboard_controller = None
        self.dashboard_view = None

        self.stack.addWidget(self.signup_view)   # index 0
        self.stack.addWidget(self.login_view)    # index 1
        # Dashboard sera ajouté dynamiquement

        self.signup_view.signup_btn.clicked.connect(self.handle_signup)
        self.signup_view.login_btn.clicked.connect(self.show_login)
        self.login_view.login_btn.clicked.connect(self.handle_login)
        # Connecte le bouton 'S'inscrire' de LoginView à show_signup
        if hasattr(self.login_view, 'switch_to_signup'):
            self.login_view.switch_to_signup.connect(self.show_signup)

        if self.any_user_exists():
            self.show_login()
        else:
            self.show_signup()

    def any_user_exists(self):
        cursor = self.user_model.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        return count > 0

    def show_signup(self):
        self.signup_view.error_label.setText("")
        self.stack.setCurrentWidget(self.signup_view)

    def show_login(self):
        self.login_view.error_label.setText("")
        self.stack.setCurrentWidget(self.login_view)

    def handle_signup(self):
        username = self.signup_view.username_input.text()
        password = self.signup_view.password_input.text()
        confirm = self.signup_view.confirm_password_input.text()
        if not username or not password or not confirm:
            self.signup_view.error_label.setText("Veuillez remplir tous les champs.")
            return
        if password != confirm:
            self.signup_view.error_label.setText("Les mots de passe ne correspondent pas.")
            return
        if self.user_model.read_user(username):
            self.signup_view.error_label.setText("Ce nom d'utilisateur existe déjà.")
            return
        self.user_model.create_user(username, password)
        user = self.user_model.read_user(username)
        self.open_dashboard(user[0])

    def handle_login(self):
        username = self.login_view.username_input.text()
        password = self.login_view.password_input.text()
        if not username or not password:
            self.login_view.error_label.setText("Veuillez remplir tous les champs.")
            return
        user = self.user_model.verify_password(username, password)
        if user:
            self.login_view.error_label.setText("")
            self.open_dashboard(user[0])
        else:
            self.login_view.error_label.setText("Nom d'utilisateur ou mot de passe incorrect.")

    def open_dashboard(self, user_id):
        # Retirer l'ancien dashboard si existant
        if self.dashboard_view:
            self.stack.removeWidget(self.dashboard_view)
            self.dashboard_view.deleteLater()
        self.dashboard_controller = DashboardController(user_id=user_id, main_window=self)
        self.dashboard_view = self.dashboard_controller.view
        self.stack.addWidget(self.dashboard_view)
        self.stack.setCurrentWidget(self.dashboard_view)

    def return_to_login(self):
        # Vider tous les champs de login
        self.login_view.username_input.clear()
        self.login_view.password_input.clear()
        self.login_view.error_label.setText("")
        # Vider tous les champs de signup
        self.signup_view.username_input.clear()
        self.signup_view.password_input.clear()
        self.signup_view.confirm_password_input.clear()
        self.signup_view.error_label.setText("")
        self.show_login()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Feuille de style globale pour un thème sombre et moderne
    app.setStyleSheet('''
        QWidget {
            background-color: #191b1f;
            color: #eaeaea;
            font-family: Arial, sans-serif;
            font-size: 15px;
        }
        QLineEdit, QComboBox, QTableWidget, QListWidget {
            background-color: #232323;
            color: #eaeaea;
            border: 1px solid #333;
            border-radius: 6px;
            padding: 6px;
        }
        QLineEdit:focus, QComboBox:focus {
            border: 1.5px solid #54a0ff;
        }
        QPushButton {
            background-color: #222f3e;
            color: #fff;
            border-radius: 8px;
            padding: 10px 0px;
            margin: 8px 8px 8px 8px;
            min-width: 120px;
        }
        QPushButton:hover {
            background-color: #54a0ff;
            color: #fff;
        }
        QPushButton:pressed {
            background-color: #2e86de;
        }
        QTableWidget {
            gridline-color: #333;
            selection-background-color: #54a0ff;
            selection-color: #fff;
            border-radius: 8px;
            alternate-background-color: #232a34;
            margin: 16px;
        }
        QTableWidget::item {
            padding: 6px;
        }
        QTableWidget::item:selected {
            background: #54a0ff;
            color: #fff;
        }
        QHeaderView::section {
            background-color: #232323;
            color: #eaeaea;
            border: 1px solid #333;
            font-weight: bold;
            padding: 6px;
        }
        QListWidget {
            background: #232323;
            border-radius: 8px;
        }
        QListWidget::item {
            padding: 8px 0px;
        }
        QListWidget::item:selected {
            background: #54a0ff;
            color: #fff;
            border-radius: 6px;
        }
        QLabel {
            color: #eaeaea;
        }
    ''')
    window = MainWindow()
    window.show()
    sys.exit(app.exec())