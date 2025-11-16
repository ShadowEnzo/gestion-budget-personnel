
from PySide6.QtWidgets import QVBoxLayout
from model.transactions_model import Transaction
from view.transactions_view import TransactionsView

class TransactionsController:
    def __init__(self, user_id, view=None):
        self.model = Transaction()
        self.user_id = user_id
        # Utilise la vue passée ou crée une nouvelle si besoin (fallback)
        if view is not None:
            self.view = view
        else:
            self.view = TransactionsView(user_id)

        # Connexions des boutons à leurs méthodes
        self.view.add_btn.clicked.connect(self.add_transaction)
        self.view.edit_btn.clicked.connect(self.edit_transaction)
        self.view.delete_btn.clicked.connect(self.delete_transaction)
        self.view.refresh_btn.clicked.connect(self.refresh_transactions)

    def add_transaction(self):
        from view.add_transaction_view import AddTransactionView
        from model.category_model import Category
        from PySide6.QtWidgets import QDialog
        categories = [cat[1] for cat in Category().get_all_category()]
        form = AddTransactionView(categories, parent=self.view)
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
            cat_row = cat_model.get_category_by_name(categorie)
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
            self.model.create_transaction(
                amount=montant_float,
                category_id=category_id,
                date=date,
                label=description,
                type=type_,
                user_id=self.user_id
            )
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
        categories = [cat[1] for cat in Category().get_all_category()]
        form = AddTransactionView(categories, parent=self.view)
        # Pré-remplir le formulaire
        form.amount_input.setText(str(transaction[1]))
        # Sélectionner la bonne catégorie
        cat_model = Category()
        cat_row = cat_model.get_category_by_id(transaction[2])
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
            cat_row = cat_model.get_category_by_name(categorie)
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