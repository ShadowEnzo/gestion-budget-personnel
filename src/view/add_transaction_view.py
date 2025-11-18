from PySide6 import QtWidgets
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QComboBox,
    QDateEdit, QPushButton, QMessageBox
)
from PySide6.QtCore import QDate
from PySide6 import QtCore

class AddTransactionView(QWidget):
    def __init__(self, categories, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ajouter une transaction")
        self.setMinimumWidth(300)

        layout = QVBoxLayout()
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(10)

        title = QPushButton("Ajouter une transaction")
        title.setEnabled(False)
        title.setStyleSheet("""
            QPushButton {
                background: none;
                color: #4fc3f7;
                font-size: 22px;
                font-weight: bold;
                border: none;
                margin-bottom: 6px;
                letter-spacing: 0.7px;
                font-family: 'Segoe UI', 'Arial', sans-serif;
            }
        """)
        layout.addWidget(title)

        card = QtWidgets.QFrame()
        card.setObjectName("Card")
        card.setStyleSheet("""
            QFrame#Card {
                background: #232a36;
                border-radius: 18px;
                border: 1.5px solid #2d3547;
                box-shadow: 0 4px 24px 0 rgba(79,195,247,0.10);
                padding: 0 0 0 0;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 18, 24, 18)
        card_layout.setSpacing(8)

        form = QFormLayout()
        form.setLabelAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        form.setFormAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        form.setHorizontalSpacing(14)
        form.setVerticalSpacing(8)
        form.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)

        label_style = "color:#4fc3f7;font-weight:600;min-width:110px;max-width:140px;text-align:right;"

        field_style = """
            QLineEdit, QComboBox, QDateEdit {
                background: #232a36;
                color: #eaeaea;
                border: 1.5px solid #2d3547;
                border-radius: 12px;
                padding: 8px 14px;
                font-size: 15px;
                font-family: 'Segoe UI', 'Arial', sans-serif;
                margin-bottom: 0px;
                transition: border 0.18s, box-shadow 0.18s;
            }
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
                border: 2px solid #4fc3f7;
                background: #232e3a;
                box-shadow: 0 0 0 2px #4fc3f733;
            }
            QLineEdit::placeholder {
                color: #8fa1b3;
                font-style: italic;
            }
        """

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Montant de la transaction")
        self.amount_input.setStyleSheet(field_style)
        form.addRow(f"<span style='{label_style}'>Montant :</span>", self.amount_input)

        self.category_input = QComboBox()
        self.category_input.addItems(categories)
        self.category_input.setStyleSheet(field_style)
        form.addRow(f"<span style='{label_style}'>Catégorie :</span>", self.category_input)

        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        self.date_input.setStyleSheet(field_style)
        form.addRow(f"<span style='{label_style}'>Date :</span>", self.date_input)

        self.type_input = QComboBox()
        self.type_input.addItems(["Revenu", "Dépense"])
        self.type_input.setStyleSheet(field_style)
        form.addRow(f"<span style='{label_style}'>Type :</span>", self.type_input)

        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText("Description (facultatif)")
        self.desc_input.setStyleSheet(field_style)
        form.addRow(f"<span style='{label_style}'>Description :</span>", self.desc_input)

        card_layout.addLayout(form)

        self.submit_btn = QPushButton("Ajouter")
        self.submit_btn.setCursor(QtCore.Qt.PointingHandCursor)
        self.submit_btn.setMinimumHeight(36)
        self.submit_btn.setMaximumWidth(140)
        self.submit_btn.setStyleSheet("""
            QPushButton {
                background: #4fc3f7;
                color: #232a36;
                font-weight: 700;
                font-size: 15px;
                border-radius: 12px;
                padding: 8px 0;
                margin-top: 8px;
                border: none;
                min-width: 120px;
                box-shadow: none;
                letter-spacing: 0.2px;
                transition: background 0.18s, color 0.18s, box-shadow 0.18s, outline 0.18s;
                outline: none;
            }
            QPushButton:hover {
                background: #43e97b;
                color: #232a36;
                box-shadow: 0 2px 10px 0 rgba(67,233,123,0.10);
            }
            QPushButton:pressed {
                background: #039be5;
                color: #eaeaea;
            }
            QPushButton:focus {
                outline: 2.5px solid #4fc3f7;
                outline-offset: 2px;
            }
        """)
        self.submit_btn.clicked.connect(self.submit_transaction)
        card_layout.addWidget(self.submit_btn, alignment=QtCore.Qt.AlignHCenter)

        layout.addWidget(card)
        self.setLayout(layout)

    def refresh_categories(self):
        from model.category_model import Category
        self.category_input.clear()
        categories = [cat[1] for cat in Category().get_all_category(self.user_id)]
        self.category_input.addItems(categories)

    def submit_transaction(self):
        # Cette méthode n'est plus utilisée, la logique est gérée par le controller
        pass

    def show_success(self, message):
        QMessageBox.information(self, "Succès", message)

    def show_error(self, message):
        QMessageBox.warning(self, "Erreur", message)