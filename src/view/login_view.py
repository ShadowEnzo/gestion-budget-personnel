
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QStackedWidget, QFrame
from PySide6 import QtCore

class LoginView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Authentification")
        self.setMinimumWidth(420)
        self.setStyleSheet("""
            QWidget {
                background-color: #181c24;
            }
            QLabel, QLineEdit, QPushButton {
                font-size: 15px;
            }
            QLineEdit {
                background: #232a36;
                color: #fff;
                border: 1px solid #232a36;
                border-radius: 7px;
                padding: 8px 12px;
            }
            QLineEdit:focus {
                border: 1.5px solid #54a0ff;
            }
            QPushButton {
                padding: 8px 0;
                font-weight: 500;
                border-radius: 8px;
            }
            QPushButton#loginBtn {
                background: transparent;
                color: #54a0ff;
                border: 1px solid #54a0ff;
            }
            QPushButton#signupBtn {
                background-color: #232a36;
                color: #54a0ff;
                border: 1px solid #54a0ff;
            }
            QPushButton#switchBtn {
                background: transparent;
                color: #888;
                border: none;
                font-size: 13px;
                margin-top: 8px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(QtCore.Qt.AlignCenter)
        layout.addStretch(1)
        login_widget = self._build_login()
        layout.addWidget(login_widget, alignment=QtCore.Qt.AlignCenter)
        layout.addStretch(1)

    def _build_login(self):
        widget = QFrame()
        widget.setFrameShape(QFrame.StyledPanel)
        widget.setMaximumWidth(370)
        layout = QVBoxLayout(widget)
        layout.setSpacing(18)
        layout.setContentsMargins(36, 36, 36, 36)

        title = QLabel("Connexion à votre compte")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #54a0ff;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nom d'utilisateur")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Mot de passe")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #e74c3c; font-size: 14px;")
        self.error_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.error_label)

        self.login_btn = QPushButton("Se connecter")
        self.login_btn.setObjectName("loginBtn")
        layout.addWidget(self.login_btn)

        switch_btn = QPushButton("Pas de compte ? S'inscrire")
        switch_btn.setObjectName("switchBtn")
        # Ce signal sera connecté dans MainWindow pour afficher la vraie page d'inscription
        self.switch_to_signup = switch_btn.clicked
        layout.addWidget(switch_btn)

        return widget



