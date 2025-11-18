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
        # Style moderne, pro, contrasté et lisible
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table.setFocusPolicy(QtCore.Qt.NoFocus)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setStyleSheet('''
            QTableWidget {
                background: #232a36;
                color: #eaeaea;
                border: 2px solid #232a36;
                border-radius: 14px;
                font-size: 16px;
                font-family: 'Segoe UI', 'Arial', sans-serif;
                gridline-color: #2d3547;
                selection-background-color: #26324a;
                selection-color: #4fc3f7;
                outline: none;
                alternate-background-color: #20232a;
            }
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #26324a, stop:1 #232a36);
                color: #4fc3f7;
                font-weight: bold;
                font-size: 16px;
                border: none;
                padding: 14px 0 14px 0;
                border-bottom: 3px solid #4fc3f7;
                letter-spacing: 0.5px;
            }
            QTableWidget::item {
                padding: 10px 18px;
                border: none;
                font-size: 15px;
                background: transparent;
            }
            QTableWidget::item:alternate {
                background: #20232a;
            }
            QTableWidget::item:selected {
                background: #26324a;
                color: #4fc3f7;
            }
            QTableWidget::item:hover {
                background: #292d36;
                color: #81d4fa;
            }
            QTableCornerButton::section {
                background: #232a36;
                border: none;
            }
        ''')
        # Colonnes aérées et hiérarchisées
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Interactive)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Interactive)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Interactive)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Interactive)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.Interactive)
        self.table.setColumnWidth(0, 60)   # ID
        self.table.setColumnWidth(1, 110)  # Montant
        self.table.setColumnWidth(2, 160)  # Catégorie (plus large)
        self.table.setColumnWidth(3, 160)  # Date (encore plus large)
        self.table.setColumnWidth(5, 100)  # Type (plus large)
        # Empêcher la coupure de texte dans toutes les colonnes
        self.table.setWordWrap(True)
        self.table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)

        # Boutons d'action
        # Boutons ergonomiques avec icônes, taille, style
        self.add_btn = QtWidgets.QPushButton("Ajouter")
        self.add_btn.setCursor(QtCore.Qt.PointingHandCursor)
        self.add_btn.setMinimumHeight(38)
        self.add_btn.setStyleSheet('''
            QPushButton {
                background: transparent;
                color: #4fc3f7;
                border-radius: 8px;
                font-weight: 600;
                font-size: 15px;
                padding: 8px 22px;
                border: none;
                transition: background 0.2s, color 0.2s;
            }
            QPushButton:hover {
                background: #4fc3f7;
                color: #232a36;
            }
            QPushButton:pressed {
                background: #039be5;
                color: #eaeaea;
            }
        ''')
        self.edit_btn = QtWidgets.QPushButton("Modifier")
        self.edit_btn.setCursor(QtCore.Qt.PointingHandCursor)
        self.edit_btn.setMinimumHeight(38)
        self.edit_btn.setStyleSheet(self.add_btn.styleSheet())
        self.delete_btn = QtWidgets.QPushButton("Supprimer")
        self.delete_btn.setCursor(QtCore.Qt.PointingHandCursor)
        self.delete_btn.setMinimumHeight(38)
        self.delete_btn.setStyleSheet('''
            QPushButton {
                background: transparent;
                color: #e57373;
                border-radius: 8px;
                font-weight: 600;
                font-size: 15px;
                padding: 8px 22px;
                border: none;
                transition: background 0.2s, color 0.2s;
            }
            QPushButton:hover {
                background: #e57373;
                color: #fff;
            }
            QPushButton:pressed {
                background: #b71c1c;
                color: #fff;
            }
        ''')
        self.refresh_btn = QtWidgets.QPushButton("Rafraîchir")
        self.refresh_btn.setCursor(QtCore.Qt.PointingHandCursor)
        self.refresh_btn.setMinimumHeight(38)
        self.refresh_btn.setStyleSheet(self.add_btn.styleSheet())

        # Layout des boutons
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.setSpacing(18)
        btn_layout.setContentsMargins(0, 16, 0, 8)
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.refresh_btn)

        # Layout principal
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setSpacing(22)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.addWidget(self.table)
        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)

        # Connexions
        self.refresh_btn.clicked.connect(self.load_transactions)
        self.delete_btn.clicked.connect(self.delete_transaction)
        # Les connexions pour ajouter/modifier peuvent pointer vers des dialogues/formulaires

    def load_transactions(self):
        from model.category_model import Category
        categories = Category().get_all_category(self.user_id)
        category_id_to_name = {cat[0]: cat[1] for cat in categories}
        transactions = self.model.get_all_transactions(self.user_id)
        self.table.setRowCount(0)
        for t in transactions:
            if t[6] == self.user_id:  # Filtrer par utilisateur
                row = self.table.rowCount()
                self.table.insertRow(row)
                # ID
                item_id = QtWidgets.QTableWidgetItem(str(t[0]))
                item_id.setTextAlignment(QtCore.Qt.AlignCenter)
                item_id.setToolTip(str(t[0]))
                item_id.setFlags(item_id.flags() & ~QtCore.Qt.ItemIsEditable)
                self.table.setItem(row, 0, item_id)
                # Montant
                item_montant = QtWidgets.QTableWidgetItem(str(t[1]))
                item_montant.setTextAlignment(QtCore.Qt.AlignCenter)
                item_montant.setToolTip(str(t[1]))
                item_montant.setFlags(item_montant.flags() & ~QtCore.Qt.ItemIsEditable)
                self.table.setItem(row, 1, item_montant)
                # Catégorie (affiche le nom, jamais l'id)
                cat_name = category_id_to_name.get(t[2], "Catégorie inconnue")
                item_cat = QtWidgets.QTableWidgetItem(cat_name)
                item_cat.setTextAlignment(QtCore.Qt.AlignCenter)
                item_cat.setToolTip(cat_name)
                item_cat.setFlags(item_cat.flags() & ~QtCore.Qt.ItemIsEditable)
                self.table.setItem(row, 2, item_cat)
                # Date
                item_date = QtWidgets.QTableWidgetItem(str(t[3]))
                item_date.setTextAlignment(QtCore.Qt.AlignCenter)
                item_date.setToolTip(str(t[3]))
                item_date.setFlags(item_date.flags() & ~QtCore.Qt.ItemIsEditable)
                item_date.setText(str(t[3]))
                item_date.setData(QtCore.Qt.TextWrapAnywhere, False)  # Désactive le word wrap pour la date
                self.table.setItem(row, 3, item_date)
                # Libellé (retour à la ligne, tooltip, alignement gauche, non éditable)
                item_libelle = QtWidgets.QTableWidgetItem(str(t[4]))
                item_libelle.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
                item_libelle.setToolTip(str(t[4]))
                item_libelle.setFlags(item_libelle.flags() & ~QtCore.Qt.ItemIsEditable)
                self.table.setItem(row, 4, item_libelle)
                # Type
                item_type = QtWidgets.QTableWidgetItem(str(t[5]))
                item_type.setTextAlignment(QtCore.Qt.AlignCenter)
                item_type.setToolTip(str(t[5]))
                item_type.setFlags(item_type.flags() & ~QtCore.Qt.ItemIsEditable)
                self.table.setItem(row, 5, item_type)

    def delete_transaction(self):
        selected = self.table.currentRow()
        if selected >= 0:
            transaction_id = int(self.table.item(selected, 0).text())
            self.model.delete_transaction(transaction_id)
            self.load_transactions()