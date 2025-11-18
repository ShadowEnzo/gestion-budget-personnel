from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QHBoxLayout, QLineEdit, QMessageBox
from PySide6 import QtWidgets, QtCore
from model.budget_model import Budget

class BudgetView(QWidget):
    def __init__(self, user_id=1):
        super().__init__()
        self.setWindowTitle("Gestion des Budgets")
        self.budget_model = Budget()
        self.user_id = user_id

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(18, 18, 18, 18)
        self.layout.setSpacing(10)
        self.setLayout(self.layout)

        title = QtWidgets.QPushButton("Gestion des budgets")
        title.setEnabled(False)
        title.setStyleSheet("""
            QPushButton {
                background: none;
                color: #4fc3f7;
                font-size: 22px;
                font-weight: bold;
                border: none;
                margin-bottom: 6px;
                letter-spacing: 0.7px;
                font-family: 'Segoe UI', 'Arial', sans-serif;
            }
        """)
        self.layout.addWidget(title)

        card = QtWidgets.QFrame()
        card.setObjectName("Card")
        card.setStyleSheet("""
            QFrame#Card {
                background: #232a36;
                border-radius: 18px;
                border: 1.5px solid #2d3547;
                box-shadow: 0 4px 24px 0 rgba(79,195,247,0.10);
                padding: 0 0 0 0;
            }
        """)
        card_layout = QtWidgets.QVBoxLayout(card)
        card_layout.setContentsMargins(24, 18, 24, 18)
        card_layout.setSpacing(8)

        # --- TABLEAU BUDGETS MODERNE ---
        self.budget_list = QtWidgets.QTableWidget()
        self.budget_list.setColumnCount(4)
        self.budget_list.setHorizontalHeaderLabels(["ID", "Montant", "Catégorie", "Utilisateur"])
        header = self.budget_list.horizontalHeader()
        header.setStretchLastSection(True)
        self.budget_list.setAlternatingRowColors(True)
        self.budget_list.setShowGrid(False)
        self.budget_list.setFocusPolicy(QtCore.Qt.NoFocus)
        self.budget_list.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.budget_list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.budget_list.verticalHeader().setVisible(False)
        self.budget_list.setStyleSheet('''
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
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Interactive)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Interactive)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Interactive)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        self.budget_list.setColumnWidth(0, 60)   # ID
        self.budget_list.setColumnWidth(1, 110)  # Montant
        self.budget_list.setColumnWidth(2, 140)  # Catégorie
        self.budget_list.setColumnWidth(3, 110)  # Utilisateur
        card_layout.addWidget(self.budget_list)


        # Formulaire moderne avec labels alignés et Card
        form = QtWidgets.QFormLayout()
        form.setLabelAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        form.setFormAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        form.setHorizontalSpacing(14)
        form.setVerticalSpacing(8)
        form.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)

        label_style = "color:#4fc3f7;font-weight:600;min-width:110px;max-width:140px;text-align:right;"
        field_style = """
            QLineEdit {
                background: #232a36;
                color: #eaeaea;
                border: 1.5px solid #2d3547;
                border-radius: 12px;
                padding: 8px 14px;
                font-size: 15px;
                font-family: 'Segoe UI', 'Arial', sans-serif;
                margin-bottom: 0px;
                transition: border 0.18s, box-shadow 0.18s;
            }
            QLineEdit:focus {
                border: 2px solid #4fc3f7;
                background: #232e3a;
                box-shadow: 0 0 0 2px #4fc3f733;
            }
            QLineEdit::placeholder {
                color: #8fa1b3;
                font-style: italic;
            }
        """
        self.amount_input = QtWidgets.QLineEdit()
        self.amount_input.setPlaceholderText("Montant")
        self.amount_input.setStyleSheet(field_style)
        form.addRow(f"<span style='{label_style}'>Montant :</span>", self.amount_input)

        self.category_input = QtWidgets.QLineEdit()
        self.category_input.setPlaceholderText("ID Catégorie")
        self.category_input.setStyleSheet(field_style)
        form.addRow(f"<span style='{label_style}'>Catégorie :</span>", self.category_input)

        self.add_button = QtWidgets.QPushButton("Ajouter")
        self.add_button.setCursor(QtCore.Qt.PointingHandCursor)
        self.add_button.setMinimumHeight(36)
        self.add_button.setMaximumWidth(140)
        self.add_button.setStyleSheet("""
            QPushButton {
                background: #4fc3f7;
                color: #232a36;
                font-weight: 700;
                font-size: 15px;
                border-radius: 12px;
                padding: 8px 0;
                margin-top: 8px;
                border: none;
                min-width: 120px;
                box-shadow: none;
                letter-spacing: 0.2px;
                transition: background 0.18s, color 0.18s, box-shadow 0.18s, outline 0.18s;
                outline: none;
            }
            QPushButton:hover {
                background: #43e97b;
                color: #232a36;
                box-shadow: 0 2px 10px 0 rgba(67,233,123,0.10);
            }
            QPushButton:pressed {
                background: #039be5;
                color: #eaeaea;
            }
            QPushButton:focus {
                outline: 2.5px solid #4fc3f7;
                outline-offset: 2px;
            }
        """)
        self.add_button.clicked.connect(self.add_budget)
        form.addRow("", self.add_button)
        card_layout.addLayout(form)

        self.layout.addWidget(card)

        self.refresh_budgets()

    def refresh_budgets(self):
        from model.category_model import Category
        categories = Category().get_all_category()
        category_id_to_name = {cat[0]: cat[1] for cat in categories}
        self.budget_list.setRowCount(0)
        budgets = self.budget_model.get_budgets(self.user_id)
        for budget in budgets:
            # budget: (id, amount, category_id, user_id)
            if budget[3] is None or budget[3] == self.user_id:
                row = self.budget_list.rowCount()
                self.budget_list.insertRow(row)
                # ID
                item_id = QtWidgets.QTableWidgetItem(str(budget[0]))
                item_id.setTextAlignment(QtCore.Qt.AlignCenter)
                self.budget_list.setItem(row, 0, item_id)
                # Montant
                item_montant = QtWidgets.QTableWidgetItem(str(budget[1]))
                item_montant.setTextAlignment(QtCore.Qt.AlignCenter)
                self.budget_list.setItem(row, 1, item_montant)
                # Catégorie (affiche le nom, jamais l'id)
                cat_name = category_id_to_name.get(budget[2], "Catégorie inconnue")
                item_cat = QtWidgets.QTableWidgetItem(cat_name)
                item_cat.setTextAlignment(QtCore.Qt.AlignCenter)
                self.budget_list.setItem(row, 2, item_cat)
                # Utilisateur
                item_user = QtWidgets.QTableWidgetItem(str(budget[3]) if budget[3] is not None else "-")
                item_user.setTextAlignment(QtCore.Qt.AlignCenter)
                self.budget_list.setItem(row, 3, item_user)

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