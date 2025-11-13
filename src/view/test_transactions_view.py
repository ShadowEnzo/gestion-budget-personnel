import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PySide6.QtWidgets import QApplication
from transactions_view import TransactionsView

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TransactionsView(user_id=1)
    window.show()
    sys.exit(app.exec())