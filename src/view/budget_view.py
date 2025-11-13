from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QHBoxLayout, QLineEdit, QMessageBox
from model.budget_model import Budget

class BudgetView(QWidget):
    def __init__(self, user_id=1):
        super().__init__()
        self.setWindowTitle("Gestion des Budgets")
        self.budget_model = Budget()
        self.user_id = user_id

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.title = QLabel("Budgets")
        self.layout.addWidget(self.title)

        self.budget_list = QListWidget()
        self.layout.addWidget(self.budget_list)

        # Formulaire d'ajout de budget
        form_layout = QHBoxLayout()
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Montant")
        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("ID Catégorie")
        self.add_button = QPushButton("Ajouter")
        self.add_button.clicked.connect(self.add_budget)
        form_layout.addWidget(self.amount_input)
        form_layout.addWidget(self.category_input)
        form_layout.addWidget(self.add_button)
        self.layout.addLayout(form_layout)

        self.refresh_budgets()

    def refresh_budgets(self):
        self.budget_list.clear()
        budgets = self.budget_model.get_budgets()
        for budget in budgets:
            # budget: (id, amount, category_id, user_id)
            if budget[3] is None or budget[3] == self.user_id:
                self.budget_list.addItem(f"Montant: {budget[1]} | Catégorie: {budget[2]}")

    def add_budget(self):
        try:
            amount = float(self.amount_input.text())
            category_id = int(self.category_input.text())
            self.budget_model.create_budget(amount, category_id, self.user_id)
            self.refresh_budgets()
            self.amount_input.clear()
            self.category_input.clear()
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Ajout impossible : {e}")