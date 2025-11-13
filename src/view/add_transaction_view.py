from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QComboBox,
    QDateEdit, QPushButton, QMessageBox
)
from PySide6.QtCore import QDate

class AddTransactionView(QWidget):
    def __init__(self, categories, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ajouter une transaction")
        self.setMinimumWidth(300)

        layout = QVBoxLayout()
        form = QFormLayout()

        self.amount_input = QLineEdit()
        form.addRow("Montant :", self.amount_input)

        self.category_input = QComboBox()
        self.category_input.addItems(categories)
        form.addRow("Catégorie :", self.category_input)

        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        form.addRow("Date :", self.date_input)

        self.type_input = QComboBox()
        self.type_input.addItems(["Revenu", "Dépense"])
        form.addRow("Type :", self.type_input)

        self.desc_input = QLineEdit()
        form.addRow("Description :", self.desc_input)

        self.submit_btn = QPushButton("Ajouter")
        self.submit_btn.clicked.connect(self.submit_transaction)

        layout.addLayout(form)
        layout.addWidget(self.submit_btn)
        self.setLayout(layout)

    def submit_transaction(self):
        montant = self.amount_input.text()
        categorie = self.category_input.currentText()
        date = self.date_input.date().toString("yyyy-MM-dd")
        type_ = self.type_input.currentText()
        description = self.desc_input.text()

        # Ici, tu peux ajouter la logique pour envoyer ces données au contrôleur
        QMessageBox.information(self, "Succès", "Transaction ajoutée !")