# fichier: d:\gestion bugdet personnel\src\view\test_add_transaction_view.py
from PySide6.QtWidgets import QApplication
from add_transaction_view import AddTransactionView
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    categories = ["Alimentation", "Transport", "Loisirs"]  # Exemple de catégories
    window = AddTransactionView(categories)
    window.show()
    sys.exit(app.exec())