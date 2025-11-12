from budget_model import Budget

budget = Budget()

budget.create_budget(1000, 1, 1)

print(budget.get_budgets())

budget.update_budget(budget_id=1, amount=1200)

budget.delete_budget(budget_id=1)