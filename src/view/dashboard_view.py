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
        sidebar_layout.setContentsMargins(8, 24, 8, 24)
        sidebar_layout.setSpacing(12)
        sidebar_container.setStyleSheet("")

        self.sidebar = QtWidgets.QListWidget()
        self.sidebar.setStyleSheet("""
QListWidget {
    background: #191b1f;
    border: none;
    color: #eaeaea;
    font-size: 16px;
    padding: 0;
}
QListWidget::item {
    padding: 16px 0 16px 32px;
    border: none;
}
QListWidget::item:selected {
    background: #232a36;
    color: #54a0ff;
    border-left: 4px solid #54a0ff;
}
QListWidget::item:hover {
    background: #232a36;
}
""")
        self.sidebar.setSpacing(2)
        self.sidebar.setMinimumWidth(200)
        self.sidebar.setMaximumWidth(240)
        self.sidebar.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.sidebar.addItem("Dashboard")
        self.sidebar.addItem("Transactions")
        self.sidebar.addItem("Ajouter une transaction")
        self.sidebar.addItem("Budgets")
        self.sidebar.addItem("Catégories")
        # Ajout direct du bouton de déconnexion juste après les items principaux
        logout_item = QtWidgets.QListWidgetItem("\u23FB  Se déconnecter")
        font = logout_item.font()
        font.setBold(True)
        logout_item.setFont(font)
        self.sidebar.addItem(logout_item)
        self.sidebar.setCurrentRow(0)
        sidebar_layout.addWidget(self.sidebar)


        # --- PAGE DASHBOARD ---
        self.label_income = QtWidgets.QLabel()
        self.label_expense = QtWidgets.QLabel()
        self.label_balance = QtWidgets.QLabel()
        self.transactions_table = QtWidgets.QTableWidget()
        self.transactions_table.setColumnCount(5)
        self.transactions_table.setHorizontalHeaderLabels(["Montant", "Catégorie", "Date", "Libellé", "Type"])
        header = self.transactions_table.horizontalHeader()
        header.setStretchLastSection(True)
        # Style moderne et épuré
        self.transactions_table.setStyleSheet('''
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
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        # Largeur fixe pour Montant, Date, Type
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        self.category_list = QtWidgets.QListWidget()
        self.refresh_btn = QtWidgets.QPushButton("Rafraîchir")
        self.refresh_btn.clicked.connect(self.refresh_view)

        dashboard_layout = QtWidgets.QVBoxLayout()
        dashboard_layout.setContentsMargins(30, 30, 30, 30)
        dashboard_layout.setSpacing(18)
        dashboard_layout.addWidget(self.label_balance)
        dashboard_layout.addWidget(self.label_income)
        dashboard_layout.addWidget(self.label_expense)
        dashboard_layout.addSpacing(10)
        dashboard_layout.addWidget(QtWidgets.QLabel("Répartition des dépenses par catégorie :"))
        self.category_list.setMinimumHeight(80)
        dashboard_layout.addWidget(self.category_list)
        dashboard_layout.addSpacing(10)
        dashboard_layout.addWidget(QtWidgets.QLabel("Dernières transactions :"))
        self.transactions_table.setMinimumHeight(180)
        dashboard_layout.addWidget(self.transactions_table)
        dashboard_layout.addSpacing(10)
        dashboard_layout.addWidget(self.refresh_btn)

        self.dashboard_page = QtWidgets.QWidget()
        self.dashboard_page.setLayout(dashboard_layout)

        # --- PAGE TRANSACTIONS ---
        self.transactions_page = TransactionsView(self.user_id)

        # --- PAGE AJOUT TRANSACTION ---
        from view.add_transaction_view import AddTransactionView
        from model.category_model import Category
        # Récupère les catégories pour le formulaire
        categories = [cat[1] for cat in Category().get_all_category()]
        self.add_transaction_page = AddTransactionView(categories)

        # --- PAGE BUDGETS ---
        from view.budgets_view import BudgetsView
        self.budgets_page = BudgetsView(user_id=self.user_id)

        # --- PAGE CATEGORIES ---
        from view.category_view import CategoryView
        self.categories_page = CategoryView()
        # Connecte le signal pour rafraîchir les catégories dans budgets_page
        self.categories_page.category_added.connect(self.budgets_page.refresh_categories)

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
        self.label_income.setText(f"Total revenus : {self.model.income:.2f} €")
        self.label_expense.setText(f"Total dépenses : {self.model.expense:.2f} €")
        self.label_balance.setText(f"Solde actuel : {self.model.net_worth['today']:.2f} €")
        self.category_list.clear()
        for tag in self.model.expense_tags:
            self.category_list.addItem(f"{tag['tag']} : {tag['amount']:.2f} € ({tag['percent']}%)")

        # Création d'un mapping id -> nom de catégorie
        categories = self.model.category_model.get_all_category()
        category_id_to_name = {cat[0]: cat[1] for cat in categories}

        transactions = self.model.transaction_model.get_all_transactions()
        # Filtrer pour n'afficher que les transactions du user_id courant
        user_transactions = [t for t in transactions if t[6] == self.user_id]
        self.transactions_table.setRowCount(0)
        for t in user_transactions[-10:][::-1]:
            row = self.transactions_table.rowCount()
            self.transactions_table.insertRow(row)
            # Montant
            item_montant = QtWidgets.QTableWidgetItem(str(t[1]))
            item_montant.setTextAlignment(QtCore.Qt.AlignCenter)
            self.transactions_table.setItem(row, 0, item_montant)
            # Catégorie
            cat_name = category_id_to_name.get(t[2], str(t[2]))
            item_cat = QtWidgets.QTableWidgetItem(cat_name)
            item_cat.setTextAlignment(QtCore.Qt.AlignCenter)
            self.transactions_table.setItem(row, 1, item_cat)
            # Date
            item_date = QtWidgets.QTableWidgetItem(str(t[3]))
            item_date.setTextAlignment(QtCore.Qt.AlignCenter)
            self.transactions_table.setItem(row, 2, item_date)
            # Libellé (spécial : retour à la ligne, tooltip, alignement gauche)
            item_libelle = QtWidgets.QTableWidgetItem(str(t[4]))
            item_libelle.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
            item_libelle.setToolTip(str(t[4]))
            item_libelle.setFlags(item_libelle.flags() | QtCore.Qt.ItemIsEditable)
            self.transactions_table.setItem(row, 3, item_libelle)
            # Type
            item_type = QtWidgets.QTableWidgetItem(str(t[5]))
            item_type.setTextAlignment(QtCore.Qt.AlignCenter)
            self.transactions_table.setItem(row, 4, item_type)