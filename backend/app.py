from flask import Flask, request, jsonify
from search import search_recipes
from generate_response import generate_response
from dotenv import load_dotenv
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from marshmallow import Schema, fields, ValidationError
import logging
from query_neo4j import find_recipes_by_ingredient
# IMPORT DU MODULE POUR LA SIMILARITÉ COSINUS
from sklearn.metrics.pairwise import cosine_similarity

# Charger les variables d'environnement
load_dotenv()

# Configurer le logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/recipes/by-ingredient', methods=['GET'])
def get_recipes_by_ingredient():
    ingredient = request.args.get('ingredient', '').strip()
    if not ingredient:
        return jsonify({"error": "L'ingrédient est requis."}), 400

    try:
        recipes = find_recipes_by_ingredient(ingredient)
        return jsonify({"ingredient": ingredient, "recipes": recipes}), 200
    except Exception as e:
        return jsonify({"error": f"Erreur interne : {str(e)}"}), 500



# Configurer la limitation de taux
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

# Schéma de validation pour la requête de recherche
class SearchSchema(Schema):
    query = fields.Str(required=True, validate=lambda s: len(s.strip()) > 0)
    top_k = fields.Int(missing=5, validate=lambda n: n > 0)

search_schema = SearchSchema()

@app.route('/search', methods=['POST'])
@limiter.limit("10 per minute")
def search_endpoint():
    try:
        data = search_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    user_query = data["query"].strip()
    top_k = data.get("top_k", 3)

    # Recherche de recettes
    try:
        recipes, recipe_embeddings, query_embedding = search_recipes(user_query, top_k=top_k)
    except Exception as e:
        return jsonify({"error": "Erreur interne lors de la recherche des recettes."}), 500

    if not recipes:
        return jsonify({
            "query": user_query,
            "response": "No relevant recipes found for your query."
        }), 200

    # Génération de la réponse
    try:
        response_text = generate_response(user_query, recipes, recipe_embeddings, query_embedding)
    except Exception as e:
        response_text = "Erreur lors de la génération de la réponse."

    # Ajouter les liens vidéo dans la réponse
    recipe_videos = {recipe["id"]: f"https://www.youtube.com/watch?v={recipe['id']}" for recipe in recipes} #https://www.youtube.com/watch?v=im2DetQWs24&t=2809s

    return jsonify({
        "query": user_query,
        "response": response_text,
        "recipes": recipes,
        "videos": recipe_videos  # Liste des liens vidéo
    }), 200

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad Request"}), 400

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal Server Error"}), 500
    

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
