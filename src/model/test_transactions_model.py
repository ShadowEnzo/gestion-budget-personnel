# Exemple de test pour transactions_model.py
# ...à placer dans un fichier test_transactions_model.py...

from transactions_model import Transaction

# Instanciation du modèle
transaction_model = Transaction()

# 1. Création d'une transaction
new_id = transaction_model.create_transaction(
    amount=100.0,
    category_id=1,
    date="2025-11-12",
    label="Achat épicerie",
    type="dépense",
    user_id=1
)
print("ID de la nouvelle transaction :", new_id)

# 2. Lecture d'une transaction
transaction = transaction_model.get_transaction(new_id)
print("Transaction récupérée :", transaction)

# 3. Lecture de toutes les transactions
all_transactions = transaction_model.get_all_transactions()
print("Toutes les transactions :", all_transactions)

# 4. Mise à jour d'une transaction
rows_updated = transaction_model.update_transaction(
    transaction_id=new_id,
    amount=120.0,
    category_id=1,
    date="2025-11-12",
    label="Achat épicerie modifié",
    type="dépense",
    user_id=1
)
print("Nombre de lignes modifiées :", rows_updated)

# 5. Suppression d'une transaction
rows_deleted = transaction_model.delete_transaction(new_id)
print("Nombre de lignes supprimées :", rows_deleted)