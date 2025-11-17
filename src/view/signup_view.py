from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QFrame
from PySide6 import QtCore

class SignupView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inscription")
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
            QPushButton#signupBtn {
                background: transparent;
                color: #54a0ff;
                border: 1px solid #54a0ff;
            }
            QPushButton#loginBtn {
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

        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setMaximumWidth(370)
        layout = QVBoxLayout(frame)
        layout.setSpacing(18)
        layout.setContentsMargins(36, 36, 36, 36)

        title = QLabel("Créer un compte")
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

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirmer le mot de passe")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.confirm_password_input)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #e74c3c; font-size: 14px;")
        self.error_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.error_label)

        self.signup_btn = QPushButton("S'inscrire")
        self.signup_btn.setObjectName("signupBtn")
        layout.addWidget(self.signup_btn)

        self.login_btn = QPushButton("Déjà un compte ? Se connecter")
        self.login_btn.setObjectName("switchBtn")
        layout.addWidget(self.login_btn)

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addStretch(1)
        main_layout.addWidget(frame, alignment=QtCore.Qt.AlignCenter)
        main_layout.addStretch(1)