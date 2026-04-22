from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import chromadb
import re
from dotenv import load_dotenv
import os

# Charger les variables d'environnement
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["smart_recipe_db"]
recipes_collection = db["recipes"]

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

client_chroma = chromadb.PersistentClient(path=os.getenv("CHROMA_DB_PATH", "./chroma_db"))
collection = client_chroma.get_or_create_collection(name="recipes_embeddings")

def normalize_text(text_list):
    """
    Nettoie et normalise une liste de textes en supprimant les espaces multiples et les caractères spéciaux.
    
    Args:
        text_list (list): Liste de chaînes de caractères.
    
    Returns:
        list: Liste de chaînes de caractères normalisées.
    """
    normalized = []
    for t in text_list:
        t = t.strip().lower()
        t = re.sub(r'\s+', ' ', t)  # Réduire espaces multiples
        t = re.sub(r'[^\w\s]', '', t)  # Enlever les caractères spéciaux
        normalized.append(t)
    return normalized

def vectorize_text(title, ingredients, directions):
    text = f"{title} {' '.join(ingredients)} {' '.join(directions)}"
    return model.encode([text])[0]

def process_batch(batch):
    ids = []
    embeddings = []
    metadatas = []

    for recipe in batch:
        try:
            name = recipe.get("name", "").strip() or "Unnamed Recipe"
            ingredients = recipe.get("ingredients", [])
            directions = recipe.get("directions", [])

            # Normalisation
            ingredients = normalize_text(ingredients)
            directions = normalize_text(directions)

            if not ingredients or not directions:
                continue  # Ignorer les recettes incomplètes

            ingredients_str = ", ".join(ingredients)
            directions_str = ". ".join(directions)

            embedding = vectorize_text(name, ingredients, directions)

            ids.append(str(recipe["_id"]))
            metadatas.append({
                "title": name,
                "ingredients": ingredients_str,
                "directions": directions_str
            })
            embeddings.append(embedding)
        except Exception as e:
            print(f"Erreur lors du traitement de la recette {recipe.get('_id')}: {e}")

    if ids:
        collection.add(
            documents=["" for _ in ids],
            embeddings=embeddings,
            ids=ids,
            metadatas=metadatas
        )

def main():
    LIMIT = int(os.getenv("RECIPE_LIMIT", 5000))
    recipes = list(recipes_collection.find(
        {"directions": {"$exists": True, "$ne": []}},
        {"_id": 1, "name": 1, "ingredients": 1, "directions": 1}
    ).limit(LIMIT))

    batch_size = int(os.getenv("BATCH_SIZE", 100))
    total_batches = (len(recipes) + batch_size - 1) // batch_size

    for i in range(0, len(recipes), batch_size):
        batch = recipes[i:i+batch_size]
        print(f"Processing batch {i // batch_size + 1}/{total_batches}...")

        try:
            process_batch(batch)
            print(f"Finished batch {i // batch_size + 1}/{total_batches}")
        except Exception as e:
            print(f"Error processing batch {i // batch_size + 1}: {e}")

    print("All batches processed successfully!")

if __name__ == "__main__":
    main()
