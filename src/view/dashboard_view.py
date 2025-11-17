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
        self.sidebar.setMinimumWidth(180)
        self.sidebar.setMaximumWidth(220)
        self.sidebar.setStyleSheet("")
        self.sidebar.addItem("Dashboard")
        self.sidebar.addItem("Transactions")
        self.sidebar.addItem("Ajouter une transaction")
        self.sidebar.addItem("Budgets")
        self.sidebar.addItem("Catégories")
        # Ajout d'un grand espaceur visuel pour pousser l'item en bas
        for _ in range(10):
            spacer_item = QtWidgets.QListWidgetItem("")
            spacer_item.setFlags(QtCore.Qt.NoItemFlags)
            self.sidebar.addItem(spacer_item)
        # Ajout de l'item de déconnexion avec icône et style
        logout_item = QtWidgets.QListWidgetItem("  Se déconnecter")
        font = logout_item.font()
        font.setBold(True)
        logout_item.setFont(font)
        # Ajout d'une icône unicode (power)
        logout_item.setText("\u23FB  Se déconnecter")
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
        self.transactions_table.horizontalHeader().setStretchLastSection(True)
        # Ajuste la largeur de la colonne Catégorie pour afficher le texte en entier
        self.transactions_table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
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
        self.transactions_table.setRowCount(0)
        for t in transactions[-10:][::-1]:
            row = self.transactions_table.rowCount()
            self.transactions_table.insertRow(row)
            self.transactions_table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(t[1])))
            # Remplacer l'ID par le nom de la catégorie
            cat_name = category_id_to_name.get(t[2], str(t[2]))
            self.transactions_table.setItem(row, 1, QtWidgets.QTableWidgetItem(cat_name))
            self.transactions_table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(t[3])))
            self.transactions_table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(t[4])))
            self.transactions_table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(t[5])))