from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QListWidget, QMessageBox
)
from model.category_model import Category

class CategoryView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion des catégories")
        self.category_model = Category()
        self.layout = QVBoxLayout()

        self.list_widget = QListWidget()
        self.layout.addWidget(self.list_widget)

        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("Nom de la catégorie")
        self.layout.addWidget(self.input_name)

        self.add_button = QPushButton("Ajouter la catégorie")
        self.add_button.clicked.connect(self.add_category)
        self.layout.addWidget(self.add_button)

        # Boutons Modifier et Supprimer en bas
        button_layout = QHBoxLayout()
        self.update_button = QPushButton("Modifier")
        self.update_button.clicked.connect(self.update_category)
        button_layout.addWidget(self.update_button)

        self.delete_button = QPushButton("Supprimer")
        self.delete_button.clicked.connect(self.delete_category)
        button_layout.addWidget(self.delete_button)

        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)
        self.refresh_list()

        self.list_widget.itemClicked.connect(self.on_item_selected)
        self.selected_category_id = None

    def refresh_list(self):
        self.list_widget.clear()
        categories = self.category_model.get_all_category()
        for cat in categories:
            self.list_widget.addItem(f"{cat[0]} - {cat[1]}")

    def add_category(self):
        name = self.input_name.text().strip()
        if name:
            if self.category_model.get_category_by_name(name):
                QMessageBox.warning(self, "Erreur", "Cette catégorie existe déjà.")
            else:
                self.category_model.create_category(name)
                self.input_name.clear()
                self.refresh_list()
        else:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer un nom de catégorie.")

    def on_item_selected(self, item):
        cat_id, cat_name = item.text().split(" - ", 1)
        self.selected_category_id = int(cat_id)
        self.input_name.setText(cat_name)

    def update_category(self):
        if self.selected_category_id is None:
            QMessageBox.warning(self, "Erreur", "Sélectionnez une catégorie à modifier.")
            return
        new_name = self.input_name.text().strip()
        if new_name:
            self.category_model.update_category(self.selected_category_id, new_name)
            self.input_name.clear()
            self.selected_category_id = None
            self.refresh_list()
        else:
            QMessageBox.warning(self, "Erreur", "Le nom ne peut pas être vide.")

    def delete_category(self):
        if self.selected_category_id is None:
            QMessageBox.warning(self, "Erreur", "Sélectionnez une catégorie à supprimer.")
            return
        self.category_model.delete_category(self.selected_category_id)
        self.input_name.clear()
        self.selected_category_id = None
        self.refresh_list()