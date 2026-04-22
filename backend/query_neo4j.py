from neo4j_connector import neo4j_db

def find_recipes_by_ingredient(ingredient_name):
    """
    Recherche des recettes contenant un ingrédient donné.
    Args:
        ingredient_name (str): Nom de l'ingrédient.
    Returns:
        list: Liste des recettes contenant cet ingrédient.
    """
    query = """
    MATCH (r:Recipe)-[:HAS_INGREDIENT]->(i:Ingredient {name: $ingredient_name})
    RETURN r.title AS recipe_title
    """
    results = neo4j_db.run_query(query, {"ingredient_name": ingredient_name.lower()})
    return [record["recipe_title"] for record in results]
