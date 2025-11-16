from view.category_view import CategoryView

class CategoriesController:
    def __init__(self, view=None):
        if view is not None:
            self.view = view
        else:
            self.view = CategoryView()
    def show(self):
        self.view.show()
