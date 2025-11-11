from PySide6 import QtWidgets

class DashboardView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.income_label = QtWidgets.QLabel()
        self.expense_label = QtWidgets.QLabel()
        self.budget_label = QtWidgets.QLabel()
        self.goals_list = QtWidgets.QListWidget()
        self.expense_tags_list = QtWidgets.QListWidget()

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.income_label)
        layout.addWidget(self.expense_label)
        layout.addWidget(self.budget_label)
        layout.addWidget(QtWidgets.QLabel("Goals:"))
        layout.addWidget(self.goals_list)
        layout.addWidget(QtWidgets.QLabel("Expenses by Tag:"))
        layout.addWidget(self.expense_tags_list)