# test_dashboard_model.py
from .dashboard_model import DashboardModel

if __name__ == "__main__":
    model = DashboardModel(user_id=1)
    print("Revenus totaux:", model.income)
    print("Dépenses totales:", model.expense)
    print("Budget restant:", model.budget)
    print("Net worth:", model.net_worth)
    print("Objectifs:", model.goals)
    print("Tags de dépenses:", model.expense_tags)