from model.transactions_model import Transaction
from model.budget_model import Budget
from model.category_model import Category

class DashboardModel:
    def __init__(self, user_id = 1):
        self.user_id = user_id
        self.transaction_model = Transaction()
        self.budget_model = Budget()
        self.category_model = Category()
        self.refresh_data()

    def refresh_data(self):
        transactions = self.transaction_model.get_all_transactions(self.user_id)
        self.income = sum(t[1] for t in transactions if t[5] == "revenu")
        self.expense = sum(t[1] for t in transactions if t[5] == "dépense")
        budgets = self.budget_model.get_budgets(self.user_id)
        self.budget = sum(b[1] for b in budgets)

        self.net_worth = {
            "today": self.income - self.expense,
            "retirement": (self.income - self.expense) * 10,
            "life_expectancy": (self.income - self.expense) * 20
        }

        self.goals = [
            {"label": "Épargne retraite", "amount": 10000},
            {"label": "Vacances", "amount": 2000}
        ]

        categories = self.category_model.get_all_category(self.user_id)
        total_expense = self.expense if self.expense > 0 else 1
        self.expense_tags = []
        for cat in categories:
            cat_expense = sum(
                t[1] for t in transactions if t[2] == cat[0] and t[5] == "dépense"
            )
            percent = round((cat_expense / total_expense) * 100, 2)
            self.expense_tags.append({
                "tag": cat[1],
                "amount": cat_expense,
                "percent": percent
            })
