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
        self.budget_list.setMinimumWidth(350)  # Largeur plus grande pour éviter la coupure
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
        from model.category_model import Category
        categories = Category().get_all_category()
        category_id_to_name = {cat[0]: cat[1] for cat in categories}
        self.budget_list.clear()
        budgets = self.budget_model.get_budgets()
        for budget in budgets:
            # budget: (id, amount, category_id, user_id)
            if budget[3] is None or budget[3] == self.user_id:
                cat_name = category_id_to_name.get(budget[2], str(budget[2]))
                text = f"Montant: {budget[1]} | Catégorie: {cat_name}"
                item = self.budget_list.addItem(text)
                # Ajoute un tooltip pour voir le texte complet si coupé
                self.budget_list.item(self.budget_list.count()-1).setToolTip(text)

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