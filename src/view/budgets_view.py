
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QComboBox, QLineEdit, QMessageBox
from PySide6.QtWidgets import QHeaderView
from PySide6 import QtCore
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
        # Remplit le formulaire lors de la sélection d'une ligne
        self.table.itemSelectionChanged.connect(self.fill_form_from_selection)

    def fill_form_from_selection(self):
        selected = self.table.currentRow()
        if selected < 0:
            return
        # Remplit le champ montant
        montant = self.table.item(selected, 1).text()
        self.amount_input.setText(montant)
        # Remplit la catégorie (par nom affiché)
        cat_name = self.table.item(selected, 2).text()
        idx = self.category_input.findText(cat_name)
        if idx >= 0:
            self.category_input.setCurrentIndex(idx)
    def setup_ui(self):
        layout = QVBoxLayout()

        # Table des budgets
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Montant", "Montant Dépensé", "% Dépense", "Catégorie", "Utilisateur"])
        header = self.table.horizontalHeader()
        # Largeur et espacement optimisés pour chaque colonne
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)   # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)   # Montant
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)   # Montant Dépense
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)   # Montant Dépasse
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)   # % Montant Dépense
        header.setSectionResizeMode(5, QHeaderView.Stretch)            # Catégorie (prend l'espace restant)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)   # Utilisateur
        self.table.setHorizontalScrollMode(QTableWidget.ScrollPerPixel)
        self.table.setVerticalScrollMode(QTableWidget.ScrollPerPixel)
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
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
        # Largeur fixe pour ID, même largeur pour les autres colonnes
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        for col in [1, 2, 3]:
            header.setSectionResizeMode(col, QHeaderView.Stretch)
        layout.addWidget(self.table)

        # Formulaire d'ajout/modif
        form_layout = QHBoxLayout()
        form_layout.setSpacing(12)
        form_layout.setContentsMargins(0, 8, 0, 0)

        field_style = """
            QLineEdit, QComboBox {
                background: #26324a;
                color: #eaeaea;
                border: 1.5px solid #2d3547;
                border-radius: 12px;
                padding: 8px 14px;
                font-size: 15px;
                font-family: 'Segoe UI', 'Arial', sans-serif;
                margin-bottom: 0px;
                transition: border 0.18s, box-shadow 0.18s, background 0.18s;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #4fc3f7;
                background: #232e3a;
                color: #4fc3f7;
                box-shadow: 0 0 0 2px #4fc3f733;
            }
            QLineEdit:hover, QComboBox:hover {
                background: #2d3547;
                color: #81d4fa;
            }
            QLineEdit::placeholder {
                color: #8fa1b3;
                font-style: italic;
            }
        """

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Montant")
        self.amount_input.setStyleSheet(field_style)
        self.amount_input.setMinimumWidth(120)
        form_layout.addWidget(self.amount_input)

        self.category_input = QComboBox()
        self.refresh_categories()
        self.category_input.setStyleSheet(field_style)
        self.category_input.setMinimumWidth(140)
        form_layout.addWidget(self.category_input)

        btn_style = """
            QPushButton {
                background: #26324a;
                color: #eaeaea;
                font-weight: 700;
                font-size: 15px;
                border-radius: 12px;
                padding: 8px 24px;
                border: none;
                min-width: 90px;
                margin-left: 4px;
                margin-right: 0;
                transition: background 0.18s, color 0.18s, outline 0.18s;
                outline: none;
            }
            QPushButton:hover {
                background: #4fc3f7;
                color: #232a36;
            }
            QPushButton:pressed {
                background: #039be5;
                color: #eaeaea;
            }
            QPushButton:focus {
                outline: 2.5px solid #4fc3f7;
                outline-offset: 2px;
            }
        """

        self.add_btn = QPushButton("Ajouter")
        self.add_btn.setStyleSheet(btn_style)
        self.add_btn.setCursor(QtCore.Qt.PointingHandCursor)
        self.add_btn.clicked.connect(self.add_budget)
        form_layout.addWidget(self.add_btn)

        self.update_btn = QPushButton("Modifier")
        self.update_btn.setStyleSheet(btn_style)
        self.update_btn.setCursor(QtCore.Qt.PointingHandCursor)
        self.update_btn.clicked.connect(self.update_budget)
        form_layout.addWidget(self.update_btn)

        self.delete_btn = QPushButton("Supprimer")
        self.delete_btn.setStyleSheet(btn_style)
        self.delete_btn.setCursor(QtCore.Qt.PointingHandCursor)
        self.delete_btn.clicked.connect(self.delete_budget)
        form_layout.addWidget(self.delete_btn)

        layout.addLayout(form_layout)
        self.setLayout(layout)

    def refresh_categories(self):
        self.category_input.clear()
        cats = self.category_model.get_all_category(self.user_id)
        for cat in cats:
            self.category_input.addItem(cat[1], cat[0])

    def load_budgets(self):
        budgets = self.budget_model.get_budgets(self.user_id)
        self.table.setRowCount(0)
        from model.user_model import User
        from model.transactions_model import Transaction
        user_model = User()
        transaction_model = Transaction()
        # Récupère tous les utilisateurs (id -> username)
        cursor = user_model.conn.cursor()
        cursor.execute("SELECT id, username FROM users")
        user_map = {row[0]: row[1] for row in cursor.fetchall()}
        alert_triggered = False
        for b in budgets:
            # b = (id, amount, category_id, user_id)
            if b[3] == self.user_id:
                row = self.table.rowCount()
                self.table.insertRow(row)
                # ID
                item_id = QTableWidgetItem(str(b[0]))
                item_id.setTextAlignment(QtCore.Qt.AlignCenter)
                self.table.setItem(row, 0, item_id)
                # Montant
                montant_budget = b[1]
                item_montant = QTableWidgetItem(str(montant_budget))
                item_montant.setTextAlignment(QtCore.Qt.AlignCenter)
                self.table.setItem(row, 1, item_montant)
                # Montant Dépensé (somme des transactions de type 'dépense' pour cette catégorie et cet utilisateur)
                transactions = transaction_model.get_all_transactions(self.user_id)
                montant_depense = sum(t[1] for t in transactions if t[2] == b[2] and t[5] == "dépense")
                item_montant_depense = QTableWidgetItem(str(montant_depense))
                item_montant_depense.setTextAlignment(QtCore.Qt.AlignCenter)
                self.table.setItem(row, 2, item_montant_depense)
                # % Dépense (dépense / budget * 100)
                pourcentage = (montant_depense / montant_budget * 100) if montant_budget else 0
                item_pourcentage = QTableWidgetItem(f"{pourcentage:.1f}%")
                item_pourcentage.setTextAlignment(QtCore.Qt.AlignCenter)
                if pourcentage > 100:
                    item_pourcentage.setBackground(QtCore.Qt.red)
                    alert_triggered = True
                self.table.setItem(row, 3, item_pourcentage)
                # Catégorie
                cat_row = self.category_model.get_category_by_id(b[2], self.user_id)
                cat_name = cat_row[1] if cat_row else "Catégorie inconnue"
                item_cat = QTableWidgetItem(cat_name)
                item_cat.setToolTip(cat_name)
                item_cat.setTextAlignment(QtCore.Qt.AlignCenter)
                self.table.setItem(row, 4, item_cat)
                # Utilisateur
                username = user_map.get(b[3], str(b[3]))
                item_user = QTableWidgetItem(username)
                item_user.setTextAlignment(QtCore.Qt.AlignCenter)
                self.table.setItem(row, 5, item_user)
        # Affiche une alerte si au moins un budget est dépassé
        if alert_triggered:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Alerte budget", "Alerte : vous avez dépassé votre budget !")

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
