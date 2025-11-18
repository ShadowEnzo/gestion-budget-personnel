from PySide6 import QtWidgets, QtCore
from model.dashboard_model import DashboardModel
from view.transactions_view import TransactionsView

class DashboardView(QtWidgets.QWidget):
    def set_page(self, index):
        self.stacked_widget.setCurrentIndex(index)
    def __init__(self, user_id):
        super().__init__()
        self.setWindowTitle("Dashboard Budget Personnel")
        self.model = DashboardModel(user_id)
        self.user_id = user_id
        self.setup_ui()
        self.refresh_view()

    def setup_ui(self):
        # Sidebar (menu latéral)
        sidebar_container = QtWidgets.QWidget()
        sidebar_layout = QtWidgets.QVBoxLayout(sidebar_container)
        sidebar_layout.setContentsMargins(12, 32, 12, 32)
        sidebar_layout.setSpacing(18)
        sidebar_container.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #181c22, stop:1 #232a36);
            border-right: 1.5px solid #232a36;
        """)

        self.sidebar = QtWidgets.QListWidget()
        self.sidebar.setStyleSheet("""
QListWidget {
    background: transparent;
    border: none;
    color: #eaeaea;
    font-size: 17px;
    font-family: 'Segoe UI', 'Arial', sans-serif;
    padding: 0;
    outline: none;
}
QListWidget::item {
    padding: 18px 0 18px 36px;
    border-radius: 8px;
    margin-bottom: 4px;
    transition: background 0.2s;
}
QListWidget::item:selected {
    background: #2d3547;
    color: #4fc3f7;
    border-left: 4px solid #4fc3f7;
    font-weight: bold;
}
QListWidget::item:hover {
    background: #232a36;
    color: #81d4fa;
}
""")
        self.sidebar.setSpacing(4)
        self.sidebar.setMinimumWidth(220)
        self.sidebar.setMaximumWidth(260)
        self.sidebar.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.sidebar.addItem("🏠  Dashboard")
        self.sidebar.addItem("💸  Transactions")
        self.sidebar.addItem("➕  Ajouter une transaction")
        self.sidebar.addItem("📊  Budgets")
        self.sidebar.addItem("📁  Catégories")
        # Ajout direct du bouton de déconnexion juste après les items principaux
        logout_item = QtWidgets.QListWidgetItem("⏻  Se déconnecter")
        font = logout_item.font()
        font.setBold(True)
        logout_item.setFont(font)
        self.sidebar.addItem(logout_item)
        self.sidebar.setCurrentRow(0)
        sidebar_layout.addWidget(self.sidebar)


        # --- PAGE DASHBOARD ---
        # --- TITRES ET LABELS ---
        self.label_balance = QtWidgets.QLabel()
        self.label_balance.setStyleSheet("font-size: 28px; font-weight: 700; color: #4fc3f7; margin-bottom: 8px; font-family: 'Segoe UI', 'Arial', sans-serif;")
        self.label_income = QtWidgets.QLabel()
        self.label_income.setStyleSheet("font-size: 18px; color: #fff; font-weight: 500; font-family: 'Segoe UI', 'Arial', sans-serif;")
        self.label_income.setTextFormat(QtCore.Qt.RichText)
        self.label_expense = QtWidgets.QLabel()
        self.label_expense.setStyleSheet("font-size: 18px; color: #fff; font-weight: 500; font-family: 'Segoe UI', 'Arial', sans-serif;")
        self.label_expense.setTextFormat(QtCore.Qt.RichText)

        # --- TABLEAU TRANSACTIONS ---
        self.transactions_table = QtWidgets.QTableWidget()
        self.transactions_table.setColumnCount(5)
        self.transactions_table.setHorizontalHeaderLabels(["Montant", "Catégorie", "Date", "Libellé", "Type"])
        header = self.transactions_table.horizontalHeader()
        header.setStretchLastSection(True)
        self.transactions_table.setAlternatingRowColors(True)
        self.transactions_table.setStyleSheet('''
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
        self.transactions_table.verticalHeader().setVisible(False)
        self.transactions_table.setShowGrid(False)
        self.transactions_table.setFocusPolicy(QtCore.Qt.NoFocus)
        self.transactions_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.transactions_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        # Largeur automatique pour Catégorie et Libellé
        # Colonnes plus aérées : largeur minimale et padding augmenté
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Interactive)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Interactive)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Interactive)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Interactive)
        self.transactions_table.setColumnWidth(0, 110)  # Montant
        self.transactions_table.setColumnWidth(1, 140)  # Catégorie
        self.transactions_table.setColumnWidth(2, 160)  # Date
        self.transactions_table.setColumnWidth(4, 110)  # Type
        # Le libellé (3) reste stretch
        # Padding augmenté dans le style (déjà présent)

        # --- LISTE DES CATEGORIES ---
        self.category_list = QtWidgets.QListWidget()
        self.category_list.setStyleSheet('''
            QListWidget {
                background: #232a36;
                color: #eaeaea;
                border: 1.5px solid #2d3547;
                border-radius: 14px;
                font-size: 15px;
                font-family: 'Segoe UI', 'Arial', sans-serif;
                padding: 8px 0;
            }
            QListWidget::item {
                padding: 8px 16px;
            }
        ''')
        self.category_list.setMinimumHeight(48)
        self.category_list.setMaximumHeight(90)
        self.category_info_label = QtWidgets.QLabel()
        self.category_info_label.setStyleSheet("color: #888; font-size: 15px; font-style: italic; margin: 8px 0 0 0;")
        self.category_info_label.setAlignment(QtCore.Qt.AlignLeft)

        # --- BOUTON REFRESH ---
        self.refresh_btn = QtWidgets.QPushButton("⟳ Rafraîchir")
        self.refresh_btn.setCursor(QtCore.Qt.PointingHandCursor)
        self.refresh_btn.setStyleSheet('''
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4fc3f7, stop:1 #232a36);
                color: #181c22;
                font-weight: 600;
                font-size: 16px;
                border-radius: 16px;
                padding: 12px 32px;
                margin-top: 10px;
                margin-bottom: 6px;
                border: none;
                box-shadow: 0 2px 12px 0 rgba(79,195,247,0.10);
                letter-spacing: 0.5px;
                transition: background 0.2s, color 0.2s, box-shadow 0.2s;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #43e97b, stop:1 #4fc3f7);
                color: #232a36;
                box-shadow: 0 4px 18px 0 rgba(67,233,123,0.18);
            }
            QPushButton:pressed {
                background: #232a36;
                color: #4fc3f7;
                box-shadow: 0 1px 4px 0 rgba(79,195,247,0.10);
            }
            QPushButton:focus {
                outline: 2px solid #4fc3f7;
                outline-offset: 2px;
            }
        ''')
        self.refresh_btn.clicked.connect(self.refresh_view)

        # --- LAYOUT DASHBOARD ---
        dashboard_layout = QtWidgets.QVBoxLayout()
        dashboard_layout.setContentsMargins(40, 40, 40, 40)
        dashboard_layout.setSpacing(22)
        dashboard_layout.addWidget(self.label_balance)
        row_income_expense = QtWidgets.QHBoxLayout()
        row_income_expense.addWidget(self.label_income)
        row_income_expense.addSpacing(16)
        row_income_expense.addWidget(self.label_expense)
        dashboard_layout.addLayout(row_income_expense)
        dashboard_layout.addSpacing(8)
        title_cat = QtWidgets.QLabel("Répartition des dépenses par catégorie :")
        title_cat.setStyleSheet("font-size: 16px; color: #4fc3f7; font-weight: 600; margin-top: 8px; font-family: 'Segoe UI', 'Arial', sans-serif;")
        dashboard_layout.addWidget(title_cat)
        dashboard_layout.addWidget(self.category_list)
        dashboard_layout.addWidget(self.category_info_label)
        dashboard_layout.addSpacing(8)
        title_tx = QtWidgets.QLabel("Dernières transactions :")
        title_tx.setStyleSheet("font-size: 16px; color: #4fc3f7; font-weight: 600; margin-top: 8px; font-family: 'Segoe UI', 'Arial', sans-serif;")
        dashboard_layout.addWidget(title_tx)
        self.transactions_table.setMinimumHeight(200)
        dashboard_layout.addWidget(self.transactions_table)
        dashboard_layout.addSpacing(8)
        dashboard_layout.addWidget(self.refresh_btn, alignment=QtCore.Qt.AlignRight)

        self.dashboard_page = QtWidgets.QWidget()
        self.dashboard_page.setLayout(dashboard_layout)

        # --- PAGE TRANSACTIONS ---
        self.transactions_page = TransactionsView(self.user_id)

        # --- PAGE AJOUT TRANSACTION ---
        from view.add_transaction_view import AddTransactionView
        from model.category_model import Category
        # Récupère les catégories pour le formulaire
        categories = [cat[1] for cat in Category().get_all_category(self.user_id)]
        self.add_transaction_page = AddTransactionView(categories)

        # --- PAGE BUDGETS ---
        from view.budgets_view import BudgetsView
        self.budgets_page = BudgetsView(user_id=self.user_id)

        # --- PAGE CATEGORIES ---
        from view.category_view import CategoryView
        self.categories_page = CategoryView(self.user_id)
        # Connecte le signal pour rafraîchir les catégories dans budgets_page et add_transaction_page
        self.categories_page.category_added.connect(self.budgets_page.refresh_categories)
        self.categories_page.category_added.connect(self.add_transaction_page.refresh_categories)

        # --- STACKED WIDGET ---
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.stacked_widget.addWidget(self.dashboard_page)         # index 0
        self.stacked_widget.addWidget(self.transactions_page)      # index 1
        self.stacked_widget.addWidget(self.add_transaction_page)   # index 2
        self.stacked_widget.addWidget(self.budgets_page)           # index 3
        self.stacked_widget.addWidget(self.categories_page)        # index 4

        # --- LAYOUT PRINCIPAL ---
        main_layout = QtWidgets.QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(sidebar_container)
        main_layout.addSpacing(0)
        main_layout.addWidget(self.stacked_widget, stretch=1)
        self.setLayout(main_layout)

    def refresh_view(self):
        self.model.refresh_data()
        self.label_income.setText(f"Total revenus : <span style='color:#43e97b;'>{self.model.income:.2f} Ar</span>")
        self.label_expense.setText(f"Total dépenses : <span style='color:#ff6b6b;'>{self.model.expense:.2f} Ar</span>")
        self.label_balance.setText(f"Solde actuel : {self.model.net_worth['today']:.2f} Ar")
        self.category_list.clear()
        total_expense = sum(tag['amount'] for tag in self.model.expense_tags)
        if total_expense > 0:
            self.category_list.setVisible(True)
            self.category_info_label.setVisible(False)
            for tag in self.model.expense_tags:
                self.category_list.addItem(f"{tag['tag']} : {tag['amount']:.2f} Ar ({tag['percent']}%)")
        else:
            self.category_list.setVisible(False)
            self.category_info_label.setText("Ajoutez une dépense pour afficher la répartition par catégories.")
            self.category_info_label.setVisible(True)

        # Création d'un mapping id -> nom de catégorie
        categories = self.model.category_model.get_all_category(self.user_id)
        category_id_to_name = {cat[0]: cat[1] for cat in categories}

        transactions = self.model.transaction_model.get_all_transactions(self.user_id)
        # Filtrer pour n'afficher que les transactions du user_id courant
        user_transactions = [t for t in transactions if t[6] == self.user_id]
        self.transactions_table.setRowCount(0)
        for t in user_transactions[-10:][::-1]:
            row = self.transactions_table.rowCount()
            self.transactions_table.insertRow(row)
            # Montant (aligné à droite)
            item_montant = QtWidgets.QTableWidgetItem(str(t[1]))
            item_montant.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            self.transactions_table.setItem(row, 0, item_montant)
            # Catégorie (centré)
            cat_name = category_id_to_name.get(t[2], str(t[2]))
            item_cat = QtWidgets.QTableWidgetItem(cat_name)
            item_cat.setTextAlignment(QtCore.Qt.AlignCenter)
            self.transactions_table.setItem(row, 1, item_cat)
            # Date (centré)
            item_date = QtWidgets.QTableWidgetItem(str(t[3]))
            item_date.setTextAlignment(QtCore.Qt.AlignCenter)
            self.transactions_table.setItem(row, 2, item_date)
            # Libellé (aligné à gauche)
            item_libelle = QtWidgets.QTableWidgetItem(str(t[4]))
            item_libelle.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
            item_libelle.setToolTip(str(t[4]))
            item_libelle.setFlags(item_libelle.flags() | QtCore.Qt.ItemIsEditable)
            self.transactions_table.setItem(row, 3, item_libelle)
            # Type (centré)
            item_type = QtWidgets.QTableWidgetItem(str(t[5]))
            item_type.setTextAlignment(QtCore.Qt.AlignCenter)
            self.transactions_table.setItem(row, 4, item_type)