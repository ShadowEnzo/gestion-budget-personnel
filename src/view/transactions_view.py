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
        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)
        # Style moderne et épuré
        self.table.setStyleSheet('''
            QTableWidget {
                background: #20232a;
                color: #eaeaea;
                border: 1px solid #232a36;
                border-radius: 8px;
                font-size: 15px;
                gridline-color: #232a36;
            }
            QHeaderView::section {
                background: #232a36;
                color: #54a0ff;
                font-weight: bold;
                border: none;
                padding: 8px 0;
            }
            QTableWidget::item {
                padding: 6px 10px;
            }
            QTableCornerButton::section {
                background: #232a36;
                border: none;
            }
        ''')
        # Largeur automatique pour Catégorie et Libellé
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        # Largeur fixe pour ID, Montant, Date, Type
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)

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
        from model.category_model import Category
        categories = Category().get_all_category()
        category_id_to_name = {cat[0]: cat[1] for cat in categories}
        transactions = self.model.get_all_transactions()
        self.table.setRowCount(0)
        for t in transactions:
            if t[6] == self.user_id:  # Filtrer par utilisateur
                row = self.table.rowCount()
                self.table.insertRow(row)
                # ID
                item_id = QtWidgets.QTableWidgetItem(str(t[0]))
                item_id.setTextAlignment(QtCore.Qt.AlignCenter)
                self.table.setItem(row, 0, item_id)
                # Montant
                item_montant = QtWidgets.QTableWidgetItem(str(t[1]))
                item_montant.setTextAlignment(QtCore.Qt.AlignCenter)
                self.table.setItem(row, 1, item_montant)
                # Catégorie
                cat_name = category_id_to_name.get(t[2], str(t[2]))
                item_cat = QtWidgets.QTableWidgetItem(cat_name)
                item_cat.setTextAlignment(QtCore.Qt.AlignCenter)
                self.table.setItem(row, 2, item_cat)
                # Date
                item_date = QtWidgets.QTableWidgetItem(str(t[3]))
                item_date.setTextAlignment(QtCore.Qt.AlignCenter)
                self.table.setItem(row, 3, item_date)
                # Libellé (spécial : retour à la ligne, tooltip, alignement gauche)
                item_libelle = QtWidgets.QTableWidgetItem(str(t[4]))
                item_libelle.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
                item_libelle.setToolTip(str(t[4]))
                item_libelle.setFlags(item_libelle.flags() | QtCore.Qt.ItemIsEditable)
                self.table.setItem(row, 4, item_libelle)
                # Type
                item_type = QtWidgets.QTableWidgetItem(str(t[5]))
                item_type.setTextAlignment(QtCore.Qt.AlignCenter)
                self.table.setItem(row, 5, item_type)

    def delete_transaction(self):
        selected = self.table.currentRow()
        if selected >= 0:
            transaction_id = int(self.table.item(selected, 0).text())
            self.model.delete_transaction(transaction_id)
            self.load_transactions()