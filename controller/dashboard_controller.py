class DashboardController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.update_view()

    def update_view(self):
        self.view.income_label.setText(f"INCOME: {self.model.income} €")
        self.view.expense_label.setText(f"EXPENSE: {self.model.expense} €")
        self.view.budget_label.setText(f"BUDGET: {self.model.budget} €")
        self.view.goals_list.clear()
        for goal in self.model.goals:
            self.view.goals_list.addItem(f"{goal['label']}: {goal['amount']} €")
        self.view.expense_tags_list.clear()
        for tag in self.model.expense_tags:
            self.view.expense_tags_list.addItem(f"{tag['tag']}: {tag['amount']} € ({tag['percent']}%)")