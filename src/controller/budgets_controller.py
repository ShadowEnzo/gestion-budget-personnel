from view.budgets_view import BudgetsView

class BudgetsController:
    def __init__(self, view=None):
        if view is not None:
            self.view = view
        else:
            self.view = BudgetsView()
    def show(self):
        self.view.show()
