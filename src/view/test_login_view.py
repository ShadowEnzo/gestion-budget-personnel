from PySide6.QtWidgets import QApplication
from login_view import LoginView
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginView()
    window.show()
    sys.exit(app.exec())
