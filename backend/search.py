from sentence_transformers import SentenceTransformer
import chromadb
import os
import logging

# Configurer le logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

client_chroma = chromadb.PersistentClient(path=os.getenv("CHROMA_DB_PATH", "./chroma_db"))
collection = client_chroma.get_or_create_collection(name="recipes_embeddings")

def search_recipes(query, top_k=3):
    """
    Recherche des recettes pertinentes en fonction de la requête utilisateur.

    Args:
        query (str): La requête de l'utilisateur.
        top_k (int, optional): Nombre de résultats à retourner. Defaults to 3.

    Returns:
        tuple: Liste des métadonnées des recettes, leurs embeddings, et l'embedding de la requête.
    """
    if not query:
        raise ValueError("La requête ne peut pas être vide.")

    query_embedding = model.encode([query])[0]
    logger.info(f"Query embedding: {query_embedding[:5]}... (truncated)")

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["embeddings", "metadatas", "documents"]
    )

    final_results = []
    recipe_embeddings = []
    for i, metadata in enumerate(results["metadatas"][0]):
        metadata["id"] = metadata.get("id", f"recipe_{i}")
        final_results.append(metadata)
        recipe_embeddings.append(results["embeddings"][0][i])

    logger.info("Final results:")
    for res in final_results:
        logger.info(res)

    return final_results, recipe_embeddings, query_embedding
