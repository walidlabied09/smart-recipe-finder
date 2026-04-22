import google.generativeai as genai
from dotenv import load_dotenv
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import logging

# Charger les variables d'environnement
load_dotenv()

# Configurer le logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurer l'API avec la clé d'API
genai.configure(api_key=os.getenv("PALM_API_KEY"))

def generate_response(query, recipes, recipe_embeddings, query_embedding):
    """
    Génère une réponse basée sur la requête utilisateur et les recettes trouvées.
    Ajoute des liens vidéo basés sur les identifiants des recettes.

    Args:
        query (str): La requête de l'utilisateur.
        recipes (list): Liste des recettes pertinentes.
        recipe_embeddings (list): Liste des embeddings des recettes.
        query_embedding (ndarray): Embedding de la requête.

    Returns:
        str: La réponse générée par le modèle GenAI.
    """
    if not recipes or not recipe_embeddings:
        return "Aucune recette pertinente trouvée."
        
    # Calcul des scores de similarité
    similarity_scores = cosine_similarity([query_embedding], recipe_embeddings)[0]
    adjusted_recipes = sorted(zip(recipes, similarity_scores), key=lambda x: x[1], reverse=True)

    input_text = f"User query: {query}\n\nHere are some recipes to consider:\n"
    recipe_links = {}  # Dictionnaire pour stocker les liens vidéo

    for recipe, _ in adjusted_recipes[:3]:
        recipe_id = recipe.get("id", "unknown_id")
        title = recipe.get("title", "").strip() or "Unnamed Recipe"
        ingredients = recipe.get("ingredients", "")
        directions = recipe.get("directions", "").strip()
        directions = directions[:200] if len(directions) > 200 else directions

        # Associer un lien vidéo à l'identifiant
        youtube_link = f"https://www.youtube.com/watch?v={recipe_id}"  # Placeholder
        recipe_links[recipe_id] = youtube_link

        input_text += f"- {title} (Video: {youtube_link})\n"
        input_text += f"  Ingredients: {ingredients}\n"
        input_text += f"  Steps: {directions}...\n\n"

    input_text += (
        "Please provide a helpful response considering the following user preferences:\n"
        "1. Main preferences: dietary restrictions, cuisine type, or cooking style.\n"
        "2. Ease of preparation: simple to prepare, minimal ingredients.\n"
        "3. Flavor and enjoyment: balanced and enjoyable dishes.\n"
        "4. Additional criteria: health focus, specific cuisines.\n"
        "Additionally, compare the recipes and explain why other options may be less suitable."
        " Suggest a complementary dish or side if applicable.\n\n"
        "Please limit your response to approximately 200 words."
    ) # i used artificial links so i didnt add id of recete in the prompt

    # Appeler le modèle GenAI
    try:
        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
        response = model.generate_content(
            contents=[input_text],
            generation_config={"temperature": 0.7, "max_output_tokens": 300}
        )

        if response and response.candidates:
            candidate = response.candidates[0]
            generated_text = ''.join(part.text for part in candidate.content.parts)
            # Ajouter les liens vidéo à la fin de la réponse générée
            generated_text += "\n\nVideo Links:\n" + "\n".join(
                [f"{recipe_id}: {link}" for recipe_id, link in recipe_links.items()]
            )
            return generated_text.strip()
        else:
            return "Aucune réponse reçue du modèle."
    except Exception as e:
        logger.error(f"Erreur inattendue : {e}")
        return "Une erreur inattendue est survenue lors de la génération de la réponse."
