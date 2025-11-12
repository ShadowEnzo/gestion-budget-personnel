class DashboardModel:
    def __init__(self):
        self.income = 5742.29
        self.expense = 3461.28
        self.budget = 224.91
        self.net_worth = {
            "today": 523021.63,
            "retirement": 3172937.61,
            "life_expectancy": 18632936.52
        }
        self.goals = [
            {"label": "Retirement", "amount": 2385785.71},
            {"label": "John's Education", "amount": 889526.71},
            {"label": "New House", "amount": 392022.60}
        ]
        self.expense_tags = [
            {"tag": "Rent", "amount": 1423.21, "percent": 41.12},
            # Ajoute d'autres catégories ici
        ]