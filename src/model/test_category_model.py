# ...existing code...
from category_model import Category

cat = Category()

# 1. Créer une catégorie
cat.create_category("Alimentation")

# 2. Récupérer par nom
print(cat.get_category_by_name("Alimentation"))

# 3. Récupérer toutes les catégories
print(cat.get_all_category())

# 4. Mettre à jour la catégorie
cat.update_category(1, "Courses alimentaires")

# 5. Supprimer la catégorie
cat.delete_category(1)