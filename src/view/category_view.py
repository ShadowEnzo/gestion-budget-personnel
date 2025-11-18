from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QListWidget, QMessageBox
from PySide6.QtCore import Signal
from model.category_model import Category

class CategoryView(QWidget):
    category_added = Signal()
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Gestion des catégories")
        self.setMinimumWidth(420)
        self.setStyleSheet("""
            QWidget {
                background-color: #181c22;
            }
            .Card {
                background: #232a36;
                border-radius: 18px;
                border: 1.5px solid #2d3547;
                box-shadow: 0 4px 24px 0 rgba(79,195,247,0.10);
                padding: 0;
                margin-bottom: 22px;
            }
            QListWidget {
                background: transparent;
                color: #eaeaea;
                border: none;
                border-radius: 12px;
                font-size: 16px;
                font-family: 'Segoe UI', 'Arial', sans-serif;
                padding: 6px 0 6px 0;
                min-height: 80px;
                max-height: 160px;
                outline: none;
            }
            QListWidget::item {
                padding: 10px 20px;
                border-radius: 8px;
                margin-bottom: 3px;
                transition: background 0.18s;
            }
            QListWidget::item:selected {
                background: #2d3547;
                color: #4fc3f7;
                font-weight: bold;
                outline: 2px solid #4fc3f7;
            }
            QListWidget::item:hover {
                background: #232a36;
                color: #81d4fa;
            }
            QLineEdit {
                background: #232a36;
                color: #fff;
                border: 1.5px solid #232a36;
                border-radius: 8px;
                padding: 10px 16px;
                font-size: 15px;
                margin-bottom: 0px;
                transition: border 0.18s;
            }
            QLineEdit:focus {
                border: 2px solid #4fc3f7;
                background: #232e3a;
            }
            QLineEdit::placeholder {
                color: #8fa1b3;
                font-style: italic;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4fc3f7, stop:1 #232a36);
                color: #181c22;
                font-weight: 600;
                font-size: 15px;
                border-radius: 12px;
                padding: 8px 22px;
                margin: 0 8px 0 0;
                border: none;
                min-width: 90px;
                min-height: 32px;
                box-shadow: 0 2px 10px 0 rgba(79,195,247,0.10);
                letter-spacing: 0.2px;
                transition: background 0.18s, color 0.18s, box-shadow 0.18s, outline 0.18s;
                outline: none;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #43e97b, stop:1 #4fc3f7);
                color: #232a36;
                box-shadow: 0 4px 18px 0 rgba(67,233,123,0.18);
            }
            QPushButton:pressed {
                background: #232a36;
                color: #4fc3f7;
                box-shadow: 0 1px 4px 0 rgba(79,195,247,0.10);
            }
            QPushButton:focus {
                outline: 2.5px solid #4fc3f7;
                outline-offset: 2px;
            }
            QLabel, QListWidget, QPushButton, QLineEdit {
                font-family: 'Segoe UI', 'Arial', sans-serif;
            }
        """)
        self.category_model = Category()
        self.layout = QVBoxLayout()
        self.layout.setSpacing(26)
        self.layout.setContentsMargins(36, 36, 36, 36)

        title = QtWidgets.QLabel("Gestion des catégories")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #4fc3f7; margin-bottom: 10px; letter-spacing: 0.7px;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(title)

        # Card autour de la liste
        self.card = QtWidgets.QFrame()
        self.card.setObjectName("Card")
        card_layout = QtWidgets.QVBoxLayout(self.card)
        card_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.setSpacing(0)
        self.list_widget = QListWidget()
        card_layout.addWidget(self.list_widget)
        self.layout.addWidget(self.card)

        # Espacement visuel entre la liste et la saisie
        self.layout.addSpacing(12)

        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("Nom de la catégorie")
        self.input_name.setClearButtonEnabled(True)
        self.layout.addWidget(self.input_name)

        # Espacement visuel entre la saisie et les actions
        self.layout.addSpacing(8)

        self.add_button = QPushButton("Ajouter la catégorie")
        self.add_button.setCursor(QtCore.Qt.PointingHandCursor)
        self.add_button.clicked.connect(self.add_category)
        self.layout.addWidget(self.add_button)

        # Espacement visuel entre le bouton ajouter et les actions
        self.layout.addSpacing(4)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        self.update_button = QPushButton("Modifier")
        self.update_button.setCursor(QtCore.Qt.PointingHandCursor)
        self.update_button.clicked.connect(self.update_category)
        button_layout.addWidget(self.update_button)

        self.delete_button = QPushButton("Supprimer")
        self.delete_button.setCursor(QtCore.Qt.PointingHandCursor)
        self.delete_button.clicked.connect(self.delete_category)
        button_layout.addWidget(self.delete_button)

        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)
        self.refresh_list()

        self.list_widget.itemClicked.connect(self.on_item_selected)
        self.selected_category_id = None

    def refresh_list(self):
        self.list_widget.clear()
        categories = self.category_model.get_all_category(self.user_id)
        for cat in categories:
            self.list_widget.addItem(f"{cat[0]} - {cat[1]}")

    def add_category(self):
        name = self.input_name.text().strip()
        if name:
            if self.category_model.get_category_by_name(name, self.user_id):
                QMessageBox.warning(self, "Erreur", "Cette catégorie existe déjà.")
            else:
                self.category_model.create_category(name, self.user_id)
                self.input_name.clear()
                self.refresh_list()
                self.category_added.emit()
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