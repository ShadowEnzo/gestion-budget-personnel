import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PySide6.QtWidgets import QApplication
from dashboard_view import DashboardView

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DashboardView(user_id=1)
    window.show()
    sys.exit(app.exec())