
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QComboBox, QLineEdit, QMessageBox
from model.budget_model import Budget
from model.category_model import Category

class BudgetsView(QWidget):
    def __init__(self, user_id=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Budgets")
        self.user_id = user_id or 1
        self.budget_model = Budget()
        self.category_model = Category()
        self.setup_ui()
        self.load_budgets()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Table des budgets
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Montant", "Catégorie", "Utilisateur"])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        # Formulaire d'ajout/modif
        form_layout = QHBoxLayout()
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Montant")
        form_layout.addWidget(self.amount_input)

        self.category_input = QComboBox()
        self.refresh_categories()
        form_layout.addWidget(self.category_input)

        self.add_btn = QPushButton("Ajouter")
        self.add_btn.clicked.connect(self.add_budget)
        form_layout.addWidget(self.add_btn)

        self.update_btn = QPushButton("Modifier")
        self.update_btn.clicked.connect(self.update_budget)
        form_layout.addWidget(self.update_btn)

        self.delete_btn = QPushButton("Supprimer")
        self.delete_btn.clicked.connect(self.delete_budget)
        form_layout.addWidget(self.delete_btn)

        layout.addLayout(form_layout)
        self.setLayout(layout)

    def refresh_categories(self):
        self.category_input.clear()
        cats = self.category_model.get_all_category()
        for cat in cats:
            self.category_input.addItem(cat[1], cat[0])

    def load_budgets(self):
        budgets = self.budget_model.get_budgets()
        self.table.setRowCount(0)
        for b in budgets:
            # b = (id, amount, category_id, user_id)
            if b[3] == self.user_id:
                row = self.table.rowCount()
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(str(b[0])))  # ID
                self.table.setItem(row, 1, QTableWidgetItem(str(b[1])))  # Montant
                # Affiche le nom de la catégorie au lieu de l'ID
                cat_row = self.category_model.get_category_by_id(b[2])
                cat_name = cat_row[1] if cat_row else str(b[2])
                self.table.setItem(row, 2, QTableWidgetItem(cat_name))
                self.table.setItem(row, 3, QTableWidgetItem(str(b[3])))  # Utilisateur

    def add_budget(self):
        try:
            amount = float(self.amount_input.text())
        except ValueError:
            QMessageBox.warning(self, "Erreur", "Montant invalide")
            return
        category_id = self.category_input.currentData()
        self.budget_model.create_budget(amount, category_id, self.user_id)
        self.load_budgets()
        self.amount_input.clear()

    def update_budget(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Erreur", "Sélectionnez un budget à modifier")
            return
        budget_id = int(self.table.item(selected, 0).text())
        try:
            amount = float(self.amount_input.text())
        except ValueError:
            QMessageBox.warning(self, "Erreur", "Montant invalide")
            return
        category_id = self.category_input.currentData()
        self.budget_model.update_budget(budget_id, amount=amount, category_id=category_id, user_id=self.user_id)
        self.load_budgets()

    def delete_budget(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Erreur", "Sélectionnez un budget à supprimer")
            return
        budget_id = int(self.table.item(selected, 0).text())
        self.budget_model.delete_budget(budget_id)
        self.load_budgets()
