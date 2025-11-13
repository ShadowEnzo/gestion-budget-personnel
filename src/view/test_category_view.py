import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PySide6.QtWidgets import QApplication
from category_view import CategoryView

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CategoryView()
    window.show()
    sys.exit(app.exec())