from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel

class SignupView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inscription")
        self.setMinimumWidth(300)
        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nom d'utilisateur")
        layout.addWidget(QLabel("Nom d'utilisateur :"))
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Mot de passe")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel("Mot de passe :"))
        layout.addWidget(self.password_input)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirmer le mot de passe")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel("Confirmer le mot de passe :"))
        layout.addWidget(self.confirm_password_input)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        layout.addWidget(self.error_label)


        self.signup_btn = QPushButton("S'inscrire")
        layout.addWidget(self.signup_btn)

        self.login_btn = QPushButton("Se connecter")
        layout.addWidget(self.login_btn)

        self.setLayout(layout)