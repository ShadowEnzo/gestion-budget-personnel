from PySide6 import QtWidgets, QtCore
from model.dashboard_model import DashboardModel

class DashboardView(QtWidgets.QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.setWindowTitle("Dashboard Budget Personnel")
        self.model = DashboardModel(user_id)
        self.setup_ui()
        self.refresh_view()

    def setup_ui(self):
        # Sidebar (menu latéral)
        self.sidebar = QtWidgets.QListWidget()
        self.sidebar.setFixedWidth(180)
        self.sidebar.addItem("Dashboard")
        self.sidebar.addItem("Transactions")
        self.sidebar.addItem("Ajouter une transaction")
        self.sidebar.addItem("Budgets")
        self.sidebar.addItem("Catégories")
        self.sidebar.setCurrentRow(0)

        # Labels principaux
        self.label_income = QtWidgets.QLabel()
        self.label_expense = QtWidgets.QLabel()
        self.label_balance = QtWidgets.QLabel()
        
        # Tableau des transactions
        self.transactions_table = QtWidgets.QTableWidget()
        self.transactions_table.setColumnCount(5)
        self.transactions_table.setHorizontalHeaderLabels(["Montant", "Catégorie", "Date", "Libellé", "Type"])
        self.transactions_table.horizontalHeader().setStretchLastSection(True)

        # Liste des catégories de dépenses
        self.category_list = QtWidgets.QListWidget()

        # Bouton de rafraîchissement
        self.refresh_btn = QtWidgets.QPushButton("Rafraîchir")
        self.refresh_btn.clicked.connect(self.refresh_view)

        # Layout principal (dashboard content)
        dashboard_layout = QtWidgets.QVBoxLayout()
        dashboard_layout.addWidget(self.label_balance)
        dashboard_layout.addWidget(self.label_income)
        dashboard_layout.addWidget(self.label_expense)
        dashboard_layout.addWidget(QtWidgets.QLabel("Répartition des dépenses par catégorie :"))
        dashboard_layout.addWidget(self.category_list)
        dashboard_layout.addWidget(QtWidgets.QLabel("Dernières transactions :"))
        dashboard_layout.addWidget(self.transactions_table)
        dashboard_layout.addWidget(self.refresh_btn)

        # Layout horizontal pour sidebar + dashboard
        main_layout = QtWidgets.QHBoxLayout()
        main_layout.addWidget(self.sidebar)
        main_layout.addLayout(dashboard_layout)
        self.setLayout(main_layout)

    def refresh_view(self):
        self.model.refresh_data()
        self.label_income.setText(f"Total revenus : {self.model.income:.2f} €")
        self.label_expense.setText(f"Total dépenses : {self.model.expense:.2f} €")
        self.label_balance.setText(f"Solde actuel : {self.model.net_worth['today']:.2f} €")

        # Répartition des dépenses par catégorie
        self.category_list.clear()
        for tag in self.model.expense_tags:
            self.category_list.addItem(f"{tag['tag']} : {tag['amount']:.2f} € ({tag['percent']}%)")

        # Dernières transactions
        transactions = self.model.transaction_model.get_all_transactions()
        self.transactions_table.setRowCount(0)
        for t in transactions[-10:][::-1]:  # Les 10 dernières
            row = self.transactions_table.rowCount()
            self.transactions_table.insertRow(row)
            self.transactions_table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(t[1])))
            self.transactions_table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(t[2])))
            self.transactions_table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(t[3])))
            self.transactions_table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(t[4])))
            self.transactions_table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(t[5])))
    