from pymongo import MongoClient
from neo4j_connector import neo4j_db

# Connexion à MongoDB
MONGO_URI = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URI)
db = client["smart_recipe_db"]
recipes_collection = db["recipes"]

def create_recipe_with_ingredients(recipe):
    """
    Insère une recette et ses ingrédients dans Neo4j.
    Args:
        recipe (dict): Données de la recette.
    """
    title = recipe.get("name", "Unnamed Recipe")
    ingredients = recipe.get("ingredients", [])

    # Requête Cypher pour insérer la recette
    query_recipe = """
    MERGE (r:Recipe {title: $title})
    RETURN r
    """

    # Requête Cypher pour relier les ingrédients
    query_ingredient = """
    MATCH (r:Recipe {title: $title})
    MERGE (i:Ingredient {name: $ingredient})
    MERGE (r)-[:HAS_INGREDIENT]->(i)
    RETURN r, i
    """

    # Insérer la recette
    neo4j_db.run_query(query_recipe, {"title": title})

    # Insérer les ingrédients
    for ingredient in ingredients:
        ingredient = ingredient.strip().lower()
        if ingredient:
            neo4j_db.run_query(query_ingredient, {"title": title, "ingredient": ingredient})

def migrate_recipes(limit=100):
    """
    Extrait les recettes de MongoDB et les insère dans Neo4j.
    Args:
        limit (int): Nombre maximum de recettes à migrer.
    """
    # Extraire les recettes de MongoDB avec une limite
    recipes = recipes_collection.find(
        {"directions": {"$exists": True, "$ne": []}},  # Filtrer les recettes avec des directions
        {"_id": 0, "name": 1, "ingredients": 1, "directions": 1}  # Limiter les champs retournés
    ).limit(limit)  # Limiter le nombre de recettes migrées

    # Compteur pour suivre la progression
    count = 0

    # Insérer les recettes dans Neo4j
    for recipe in recipes:
        create_recipe_with_ingredients(recipe)
        count += 1
        print(f"Recette insérée ({count}/{limit}) : {recipe.get('name')}")

    print(f"Migration terminée avec succès ! Total de recettes migrées : {count}")

if __name__ == "__main__":
    migrate_recipes(limit=100)
