from view.dashboard_view import DashboardView
from controller.transactions_controller import TransactionsController

class DashboardController:
    def __init__(self, user_id, main_window=None):
        self.user_id = user_id
        self.view = DashboardView(user_id)
        self.transactions_controller = None
        self.main_window = main_window
        self.connect_signals()

    def logout(self):
        if self.main_window:
            self.main_window.return_to_login()

    def connect_signals(self):
        # Rafraîchir le dashboard quand on clique sur le bouton
        self.view.refresh_btn.clicked.connect(self.refresh_dashboard)
        # Navigation dans la sidebar (exemple)
        self.view.sidebar.currentRowChanged.connect(self.handle_sidebar_navigation)

    def handle_sidebar_navigation(self, index):
        # Si c'est l'item de déconnexion (dernier item), on déconnecte
        if index == self.view.sidebar.count() - 1:
            self.logout()
            return
        # Si c'est un des espaceurs, on ignore
        if index >= 5:
            return
        # Change la page affichée dans le stacked widget
        self.view.set_page(index)
        if index == 0:
            self.view.refresh_view()
        elif index == 1:
            self.open_transactions_controller()
        elif index == 2:
            self.prepare_add_transaction_form()
        elif index == 3:
            self.prepare_budgets_page()
        elif index == 4:
            self.prepare_categories_page()

    # (supprimé, la bonne version logout est déjà plus haut)

    def refresh_dashboard(self):
        self.view.refresh_view()



    def prepare_budgets_page(self):
        # Ici tu peux ajouter des actions à faire à l'ouverture de la page budgets
        pass

    def prepare_categories_page(self):
        # Rafraîchit la liste des catégories à chaque affichage
        self.view.categories_page.refresh_list()

    def prepare_add_transaction_form(self):
        # Connecte le bouton du formulaire à la méthode d'ajout
        page = self.view.add_transaction_page
        try:
            page.submit_btn.clicked.disconnect()
        except Exception:
            pass
        page.submit_btn.clicked.connect(self.submit_add_transaction)

    def submit_add_transaction(self):
        page = self.view.add_transaction_page
        montant = page.amount_input.text()
        categorie = page.category_input.currentText()
        date = page.date_input.date().toString("yyyy-MM-dd")
        type_ = page.type_input.currentText().lower()
        description = page.desc_input.text()

        # Récupère l'id de la catégorie
        from model.category_model import Category
        cat_model = Category()
        cat_row = cat_model.get_category_by_name(categorie)
        if cat_row:
            category_id = cat_row[0]
        else:
            page.show_error("Catégorie invalide")
            return

        # Ajoute la transaction
        from model.transactions_model import Transaction
        model = Transaction()
        try:
            montant_float = float(montant)
        except ValueError:
            page.show_error("Montant invalide")
            return
        model.create_transaction(
            amount=montant_float,
            category_id=category_id,
            date=date,
            label=description,
            type=type_,
            user_id=self.user_id
        )
        page.show_success("Transaction ajoutée !")
        # Optionnel: reset le formulaire
        page.amount_input.clear()
        page.desc_input.clear()

    def open_transactions_controller(self):
        # Utilise la vue déjà présente dans le stacked widget
        if self.transactions_controller is None:
            # Passe la vue existante à TransactionsController
            self.transactions_controller = TransactionsController(self.user_id, self.view.transactions_page)
        self.transactions_controller.refresh_transactions()


    def show(self):
        self.view.showMaximized()