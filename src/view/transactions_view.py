from PySide6 import QtWidgets, QtCore
from model.transactions_model import Transaction

class TransactionsView(QtWidgets.QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.setWindowTitle("Liste des transactions")
        self.model = Transaction()
        self.user_id = user_id
        self.setup_ui()
        self.load_transactions()

    def setup_ui(self):
        # Tableau des transactions
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Montant", "Catégorie", "Date", "Libellé", "Type"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)

        # Boutons d'action
        self.add_btn = QtWidgets.QPushButton("Ajouter")
        self.edit_btn = QtWidgets.QPushButton("Modifier")
        self.delete_btn = QtWidgets.QPushButton("Supprimer")
        self.refresh_btn = QtWidgets.QPushButton("Rafraîchir")

        # Layout des boutons
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.refresh_btn)

        # Layout principal
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.table)
        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)

        # Connexions
        self.refresh_btn.clicked.connect(self.load_transactions)
        self.delete_btn.clicked.connect(self.delete_transaction)
        # Les connexions pour ajouter/modifier peuvent pointer vers des dialogues/formulaires

    def load_transactions(self):
        transactions = self.model.get_all_transactions()
        self.table.setRowCount(0)
        for t in transactions:
            if t[6] == self.user_id:  # Filtrer par utilisateur
                row = self.table.rowCount()
                self.table.insertRow(row)
                for col, value in enumerate(t):
                    self.table.setItem(row, col, QtWidgets.QTableWidgetItem(str(value)))

    def delete_transaction(self):
        selected = self.table.currentRow()
        if selected >= 0:
            transaction_id = int(self.table.item(selected, 0).text())
            self.model.delete_transaction(transaction_id)
            self.load_transactions()