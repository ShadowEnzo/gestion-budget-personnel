class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password  # À hasher en pratique

class Transaction:
    def __init__(self, amount, category, date, label, type_):
        self.amount = amount
        self.category = category
        self.date = date
        self.label = label
        self.type = type_  # "income" ou "expense"

class Category:
    def __init__(self, name):
        self.name = name

class Budget:
    def __init__(self, amount, category):
        self.amount = amount
        self.category = category