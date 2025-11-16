from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PySide6 import QtCore

class LoginView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Connexion")
        self.setMinimumWidth(400)
        self.setStyleSheet("QLabel { color: #fff; font-size: 16px; } QLineEdit, QPushButton { font-size: 15px; }")

        # Centrage vertical et horizontal
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(QtCore.Qt.AlignCenter)

        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setSpacing(18)
        form_layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel("Connexion à votre compte")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #54a0ff;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        form_layout.addWidget(title)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nom d'utilisateur")
        self.username_input.setMinimumHeight(32)
        form_layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Mot de passe")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(32)
        form_layout.addWidget(self.password_input)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #e74c3c; font-size: 14px;")
        self.error_label.setAlignment(QtCore.Qt.AlignCenter)
        form_layout.addWidget(self.error_label)

        self.login_btn = QPushButton("Se connecter")
        self.login_btn.setMinimumHeight(36)
        self.login_btn.setStyleSheet("background-color: #54a0ff; color: white; border-radius: 8px;")
        form_layout.addWidget(self.login_btn)

        self.signup_btn = QPushButton("S'inscrire")
        self.signup_btn.setMinimumHeight(36)
        self.signup_btn.setStyleSheet("background-color: #222f3e; color: #fff; border-radius: 8px;")
        form_layout.addWidget(self.signup_btn)

        main_layout.addStretch(1)
        main_layout.addWidget(form_widget, alignment=QtCore.Qt.AlignCenter)
        main_layout.addStretch(1)



