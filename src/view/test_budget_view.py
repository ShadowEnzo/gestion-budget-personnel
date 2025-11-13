import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Ajoute src au chemin

from PySide6.QtWidgets import QApplication
from view.budget_view import BudgetView  # Import avec le préfixe view

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BudgetView(user_id=1)
    window.show()
    sys.exit(app.exec())