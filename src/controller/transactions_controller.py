
from PySide6.QtWidgets import QVBoxLayout
from PySide6 import QtCore
from model.transactions_model import Transaction
from view.transactions_view import TransactionsView

class TransactionsController:
    def __init__(self, user_id, view=None, budgets_view=None):
        self.model = Transaction()
        self.user_id = user_id
        # Vue principale des transactions
        if view is not None:
            self.view = view
        else:
            self.view = TransactionsView(user_id)
        # Vue budgets (pour rafraîchir dynamiquement)
        self.budgets_view = budgets_view

        # Connexions des boutons à leurs méthodes
        self.view.add_btn.clicked.connect(self.add_transaction)
        self.view.edit_btn.clicked.connect(self.edit_transaction)
        self.view.delete_btn.clicked.connect(self.delete_transaction)
        self.view.refresh_btn.clicked.connect(self.refresh_transactions)

    def add_transaction(self):
        from view.add_transaction_view import AddTransactionView
        from model.category_model import Category
        from PySide6.QtWidgets import QDialog
        categories = [cat[1] for cat in Category().get_all_category(self.user_id)]
        form = AddTransactionView(categories, user_id=self.user_id, parent=self.view)
        # On rend le formulaire modal
        dialog = QDialog(self.view)
        dialog.setWindowTitle("Ajouter une transaction")
        layout = QVBoxLayout()
        layout.addWidget(form)
        dialog.setLayout(layout)
        def on_submit():
            montant = form.amount_input.text()
            categorie = form.category_input.currentText()
            date = form.date_input.date().toString("yyyy-MM-dd")
            type_ = form.type_input.currentText().lower()
            description = form.desc_input.text()
            cat_model = Category()
            cat_row = cat_model.get_category_by_name(categorie, self.user_id)
            if cat_row:
                category_id = cat_row[0]
            else:
                form.show_error("Catégorie invalide")
                return
            try:
                montant_float = float(montant)
            except ValueError:
                form.show_error("Montant invalide")
                return
            # Vérifier si la transaction va dépasser le budget
            depense_excessive = False
            if type_ == "dépense":
                from model.budget_model import Budget
                budget_model = Budget()
                budgets = budget_model.get_budgets(self.user_id)
                budget_for_cat = next((b for b in budgets if b[2] == category_id), None)
                if budget_for_cat:
                    montant_budget = budget_for_cat[1]
                    from model.transactions_model import Transaction as TransactionModel
                    transaction_model = TransactionModel()
                    transactions = transaction_model.get_all_transactions(self.user_id)
                    montant_depense = sum(t[1] for t in transactions if t[2] == category_id and t[5] == "dépense")
                    if montant_depense + montant_float > montant_budget:
                        depense_excessive = True
            if depense_excessive:
                from PySide6.QtWidgets import QMessageBox
                reply = QMessageBox.question(
                    form,
                    "Dépassement de budget",
                    "Cette dépense va dépasser le budget de la catégorie. Êtes-vous sûr de vouloir continuer ?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply != QMessageBox.Yes:
                    return
            self.model.create_transaction(
                amount=montant_float,
                category_id=category_id,
                date=date,
                label=description,
                type=type_,
                user_id=self.user_id
            )
            # Rafraîchir la vue budget si elle existe
            if self.budgets_view is not None:
                self.budgets_view.load_budgets()
            form.show_success("Transaction ajoutée !")
            dialog.accept()
            self.refresh_transactions()
        form.submit_btn.clicked.disconnect()
        form.submit_btn.clicked.connect(on_submit)
        dialog.exec_()

    def edit_transaction(self):
        from view.add_transaction_view import AddTransactionView
        from model.category_model import Category
        from PySide6.QtWidgets import QDialog
        selected = self.view.table.currentRow()
        if selected < 0:
            return
        transaction_id = int(self.view.table.item(selected, 0).text())
        # Récupérer la transaction existante
        transaction = self.model.get_transaction(transaction_id)
        if not transaction:
            return
        # Préparer les catégories
        categories = [cat[1] for cat in Category().get_all_category(self.user_id)]
        form = AddTransactionView(categories, parent=self.view)
        # Pré-remplir le formulaire
        form.amount_input.setText(str(transaction[1]))
        # Sélectionner la bonne catégorie
        cat_model = Category()
        cat_row = cat_model.get_category_by_id(transaction[2], self.user_id)
        if cat_row:
            idx = form.category_input.findText(cat_row[1])
            if idx >= 0:
                form.category_input.setCurrentIndex(idx)
        form.date_input.setDate(QtCore.QDate.fromString(transaction[3], "yyyy-MM-dd"))
        form.desc_input.setText(str(transaction[4]))
        # Type (revenu/dépense)
        type_idx = form.type_input.findText(transaction[5].capitalize())
        if type_idx >= 0:
            form.type_input.setCurrentIndex(type_idx)
        form.submit_btn.setText("Enregistrer")
        # Dialog
        dialog = QDialog(self.view)
        dialog.setWindowTitle("Modifier la transaction")
        layout = QVBoxLayout()
        layout.addWidget(form)
        dialog.setLayout(layout)
        def on_submit():
            montant = form.amount_input.text()
            categorie = form.category_input.currentText()
            date = form.date_input.date().toString("yyyy-MM-dd")
            type_ = form.type_input.currentText().lower()
            description = form.desc_input.text()
            cat_row = cat_model.get_category_by_name(categorie, self.user_id)
            if cat_row:
                category_id = cat_row[0]
            else:
                form.show_error("Catégorie invalide")
                return
            try:
                montant_float = float(montant)
            except ValueError:
                form.show_error("Montant invalide")
                return
            self.model.update_transaction(
                transaction_id=transaction_id,
                amount=montant_float,
                category_id=category_id,
                date=date,
                label=description,
                type=type_,
                user_id=self.user_id
            )
            # Rafraîchir la vue budget si elle existe
            if hasattr(self, 'budgets_view') and self.budgets_view is not None:
                self.budgets_view.load_budgets()
            form.show_success("Transaction modifiée !")
            dialog.accept()
            self.refresh_transactions()
        try:
            form.submit_btn.clicked.disconnect()
        except Exception:
            pass
        form.submit_btn.clicked.connect(on_submit)
        dialog.exec_()

    def delete_transaction(self):
        self.view.delete_transaction()

    def refresh_transactions(self):
        self.view.load_transactions()