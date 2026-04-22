import streamlit as st
import requests
import pandas as pd
from dotenv import load_dotenv
import os

# Charger les variables d'environnement
load_dotenv()

# URL du backend
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:5000/search") 

# Titre de l'application
st.title("Smart Recipe Finder 🥦")
st.write("""
Découvrez de nouvelles recettes passionnantes adaptées à vos envies et ingrédients ! 
Que vous cherchiez de l'inspiration ou une surprise culinaire, cette application alimentée par l'IA
explorera plus de 20 000 recettes pour trouver celle qui vous convient. 🗾
""")
st.divider()  # Ligne séparatrice pour l'organisation visuelle

# Champ de saisie pour la requête utilisateur
user_input = st.text_input("Qu'avez-vous envie de cuisiner aujourd'hui ? Partagez vos idées et laissez-nous vous aider !")

# Bouton pour obtenir des recommandations
if st.button('Obtenir des recommandations !'):
    if not user_input.strip():
        # Alerte si aucune entrée n'a été fournie
        st.warning("Veuillez entrer une requête pour obtenir des recommandations.")
    else:
        # Afficher une animation de chargement pendant le traitement
        with st.spinner("Recherche de délicieuses idées..."):
            try:
                # Appel au backend pour obtenir les recommandations
                response = requests.post(
                    BACKEND_URL,
                    json={'query': user_input, 'top_k': 3}
                )
                response.raise_for_status()  # Vérifie si la requête a échoué
                data = response.json()

                # Extraction des données de la réponse du backend
                query = data.get('query', '')  # La requête utilisateur
                response_text = data.get('response', '')  # Réponse générée par l'IA
                recipes = data.get('recipes', [])  # Liste des recettes recommandées
                videos = data.get("videos", {})  # Vidéos associées aux recettes

                # Vérifier si aucune recette n'a été trouvée
                if not recipes:
                    st.error("Aucune recette pertinente n'a été trouvée pour votre requête. Essayez un autre terme.")
                    st.stop()  # Arrête le processus si aucune recette n'est disponible

                # Afficher la réponse générée par l'IA sans inclure les liens vidéo
                st.markdown("### **Suggestion de l'IA :**")
                if response_text:
                    # Supprimer la section "Video Links:" si elle existe dans la réponse
                    if "Video Links:" in response_text:
                        response_text = response_text.split("Video Links:")[0].strip()

                    # Formater et afficher la réponse générée
                    html_content = f"""
                    <div style="text-align: justify; margin-bottom: 20px; line-height: 1.6;">
                        {response_text}
                    </div>
                    """
                    st.markdown(html_content, unsafe_allow_html=True)
                else:
                    st.markdown("Aucune réponse disponible.")

                # Afficher les recettes recommandées
                st.markdown("### **Recettes recommandées :**")

                for recipe in recipes:
                    # Extraction des informations de chaque recette
                    title = recipe.get('title', 'Recette sans nom').capitalize()
                    ingredients = recipe.get('ingredients', [])
                    directions = recipe.get('directions', 'Aucune direction disponible')
                    recipe_id = recipe.get('id', '')

                    # Conversion des ingrédients en chaîne de caractères si nécessaire
                    if isinstance(ingredients, list):
                        ingredients = ', '.join(ingredients)

                    # Affichage de la carte de la recette (titre et ingrédients)
                    recipe_html = f"""
                    <div style="border: 1px solid #ddd; border-radius: 8px; padding: 15px; margin-bottom: 15px; background-color: #f9f9f9;">
                        <h4 style="color: #074E0A;">{title}</h4>
                        <p><b>Ingrédients :</b> {ingredients if ingredients else 'Aucun ingrédient disponible.'}</p>
                    </div>
                    """
                    st.markdown(recipe_html, unsafe_allow_html=True)

                    # Utiliser un expander pour afficher les étapes de préparation et les vidéos
                    with st.expander(f"Directions pour {title}"):
                        if directions and directions != 'Aucune direction disponible':
                            # Diviser les étapes en phrases pour les afficher
                            steps = directions.split('.')
                            steps = [step.strip() for step in steps if step.strip()]
                            for i, step in enumerate(steps, start=1):
                                st.markdown(f"{i}. {step}")
                        else:
                            st.write("Aucune direction disponible.")

                        # Ajouter le lien vidéo sous les étapes
                        if recipe_id in videos:
                            video_link = videos[recipe_id]
                            st.markdown(f"### **Tutoriel vidéo**")
                            st.markdown(f"[Regarder le tutoriel ici]({video_link})", unsafe_allow_html=True)

            # Gestion des erreurs possibles
            except requests.exceptions.RequestException as e:
                st.error(f"Erreur lors de la récupération des recettes : {e}")
            except ValueError as e:
                st.error(f"Erreur d'analyse de la réponse du backend : {e}")
            except Exception as e:
                st.error(f"Une erreur inattendue s'est produite : {e}")
