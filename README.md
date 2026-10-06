# 🥦 Smart Recipe Finder

**Smart Recipe Finder** est une application intelligente de recommandation culinaire basée sur **l'IA générative**, la **recherche vectorielle** et les **bases de données NoSQL et graphes**.

L'application permet aux utilisateurs d'obtenir des suggestions de recettes personnalisées à partir de requêtes formulées en langage naturel, par exemple :

* 🥕 Ingrédients disponibles
* 🍽️ Type de plat recherché
* 🥗 Régime alimentaire
* 🌱 Préférences nutritionnelles
* ⏱️ Temps de préparation
* 💡 Envie ou contexte particulier

Le système combine une architecture **client-serveur**, un pipeline **RAG (Retrieval-Augmented Generation)**, la recherche sémantique et l'IA générative afin de fournir des recommandations pertinentes et contextualisées.

---

## 🏗️ Architecture du Système

L'application repose sur une architecture modulaire composée d'un frontend Streamlit, d'un backend Flask et de plusieurs composants de données et d'intelligence artificielle.

```text
                          ┌──────────────────────┐
                          │      Utilisateur     │
                          └──────────┬───────────┘
                                     │
                                     ▼
                          ┌──────────────────────┐
                          │  Frontend Streamlit  │
                          │      Port : 8501     │
                          └──────────┬───────────┘
                                     │ HTTP
                                     ▼
                          ┌──────────────────────┐
                          │     Backend Flask    │
                          │      Port : 5000     │
                          └──────────┬───────────┘
                                     │
               ┌─────────────────────┼─────────────────────┐
               │                     │                     │
               ▼                     ▼                     ▼
       ┌───────────────┐     ┌───────────────┐     ┌───────────────┐
       │   ChromaDB    │     │    MongoDB    │     │     Neo4j     │
       │ Recherche     │     │ Stockage des  │     │ Graphe des    │
       │ vectorielle   │     │   recettes    │     │ relations     │
       └───────┬───────┘     └───────────────┘     └───────┬───────┘
               │                                           │
               ▼                                           ▼
       ┌───────────────────┐                       ┌──────────────────┐
       │ Sentence          │                       │ Requêtes Cypher │
       │ Transformers      │                       │ & relations     │
       │ Embeddings        │                       │ culinaires      │
       └─────────┬─────────┘                       └──────────────────┘
                 │
                 ▼
       ┌─────────────────────────┐
       │      Google GenAI       │
       │ Génération & synthèse   │
       │ des recommandations     │
       └─────────────────────────┘
```

---

## 🧩 Composants de l'Architecture

### 🎨 Frontend — Streamlit

L'interface utilisateur est développée avec **Streamlit**.

Elle permet notamment :

* La saisie de requêtes en langage naturel
* L'affichage des recettes recommandées
* L'affichage des ingrédients
* L'affichage des étapes de préparation
* L'affichage d'informations contextuelles
* La présentation dynamique des résultats
* L'accès à des liens vers des tutoriels vidéo

---

### ⚙️ Backend — Flask

Le backend est développé avec **Flask** et expose une API permettant de :

* Recevoir les requêtes utilisateur
* Traiter et préparer les requêtes
* Générer les embeddings
* Effectuer les recherches sémantiques
* Interroger MongoDB
* Interroger Neo4j
* Orchestrer le pipeline RAG
* Appeler le modèle Google GenAI
* Retourner les recommandations au frontend

---

## 🗄️ Bases de Données

### 🍃 MongoDB

MongoDB est utilisé comme base de données NoSQL principale pour stocker les recettes.

Le système contient plus de **20 000 recettes** avec différentes informations :

* Titre
* Ingrédients
* Étapes de préparation
* Informations complémentaires
* Métadonnées culinaires

MongoDB constitue la source principale des données utilisées lors de la recherche et de la recommandation.

---

### 🔎 ChromaDB

ChromaDB est utilisé pour l'indexation et la recherche vectorielle.

Les recettes et les requêtes utilisateur sont transformées en représentations vectorielles grâce aux embeddings.

Le système peut ensuite rechercher les recettes les plus proches sémantiquement de la requête utilisateur.

```text
Requête utilisateur
        │
        ▼
Sentence Transformers
        │
        ▼
Embedding vectoriel
        │
        ▼
ChromaDB
        │
        ▼
Recherche par similarité
        │
        ▼
Recettes pertinentes
```

---

### 🕸️ Neo4j

Neo4j est utilisé pour représenter les relations entre les recettes et leurs ingrédients sous forme de graphe de connaissances.

Exemple :

```text
              ┌──────────────┐
              │    Recette   │
              │   Couscous   │
              └───────┬──────┘
                      │
               HAS_INGREDIENT
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
   ┌─────────┐   ┌─────────┐   ┌─────────┐
   │ Semoule │   │ Carotte │   │ Courgette│
   └─────────┘   └─────────┘   └─────────┘
```

Les relations principales sont basées notamment sur :

```text
(:Recipe)-[:HAS_INGREDIENT]->(:Ingredient)
```

Cette représentation permet d'exploiter les relations entre les recettes et les ingrédients.

---

## 🤖 Intelligence Artificielle

### Sentence Transformers

**Sentence Transformers** est utilisé pour transformer les requêtes textuelles et les informations culinaires en embeddings.

Exemple :

```text
"recette avec poulet et riz"
                │
                ▼
       Sentence Transformers
                │
                ▼
       Vecteur numérique
                │
                ▼
             ChromaDB
```

Cela permet de réaliser une recherche basée sur le **sens de la requête** et non uniquement sur la correspondance exacte des mots.

---

### Google GenAI

**Google GenAI** est utilisé pour la génération et la synthèse des réponses.

Le modèle permet notamment de :

* Générer des recommandations personnalisées
* Expliquer les résultats
* Fournir des conseils contextuels
* Générer des informations nutritionnelles
* Formuler une réponse naturelle à l'utilisateur

Le modèle intervient après la récupération des informations pertinentes afin de produire une réponse contextualisée.

---

## 🔄 Pipeline RAG

Le système utilise une approche **Retrieval-Augmented Generation (RAG)**.

Le fonctionnement général est le suivant :

```text
Utilisateur
    │
    ▼
Requête en langage naturel
    │
    ▼
Prétraitement
    │
    ▼
Génération de l'embedding
    │
    ▼
Recherche vectorielle
    │
    ▼
ChromaDB
    │
    ├──────────────► MongoDB
    │
    └──────────────► Neo4j
                         │
                         ▼
                     Informations
                     contextuelles
                         │
                         ▼
                     Google GenAI
                         │
                         ▼
                  Réponse personnalisée
                         │
                         ▼
                     Streamlit UI
```

Cette architecture permet de combiner :

* La recherche sémantique
* Les données structurées
* Les relations du graphe
* L'intelligence artificielle générative

---

## 📁 Structure du Répertoire

```text
smart-recipe-finder/
│
├── backend/
│   ├── app.py                  # Point d'entrée de l'API Flask
│   ├── generate_response.py    # Génération des réponses via Google GenAI
│   ├── search.py               # Logique de recherche vectorielle
│   ├── preprocess.py           # Pipeline d'ingestion et de préparation
│   ├── mongodb_to_neo4j.py     # Synchronisation MongoDB vers Neo4j
│   ├── neo4j_connector.py      # Connexion et requêtes Cypher
│   └── requirements.txt        # Dépendances Python du backend
│
├── frontend/
│   ├── app.py                  # Application Streamlit
│   └── assets/                 # Images, illustrations et ressources
│
├── docs/
│   └── rapport-technique.pdf   # Rapport technique du projet
│
├── .gitignore
└── README.md
```

---

## ⚙️ Guide d'Installation & Démarrage

### 1. Prérequis

Avant de commencer, assurez-vous d'avoir installé :

* **Python 3.8 ou supérieur**
* **MongoDB**
* **Neo4j**
* Une **clé API Google GenAI**
* **Git**

Vérifiez votre version de Python :

```bash
python --version
```

Vérifiez votre installation Git :

```bash
git --version
```

---

### 2. Cloner le projet

Clonez le dépôt GitHub :

```bash
git clone https://github.com/walidlabied09/smart-recipe-finder.git
```

Accédez au projet :

```bash
cd smart-recipe-finder
```

---

### 3. Créer l'environnement virtuel

#### Windows

```bash
python -m venv env
```

Activez ensuite l'environnement :

```bash
.\env\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv env
```

Activez ensuite l'environnement :

```bash
source env/bin/activate
```

Lorsque l'environnement est activé, vous devriez voir `(env)` au début de votre terminal.

---

### 4. Installer les dépendances

Accédez au dossier backend :

```bash
cd backend
```

Installez les dépendances :

```bash
pip install -r requirements.txt
pip install streamlit
```

---

## 🔐 Configuration

### Variables d'environnement

Créez un fichier `.env` dans le dossier `backend/`.

```text
smart-recipe-finder/
│
├── backend/
│   ├── .env
│   ├── app.py
│   ├── search.py
│   └── ...
│
└── frontend/
```

Ajoutez les variables suivantes :

```env
MONGO_URI=mongodb://localhost:27017
CHROMA_DB_PATH=./chroma_db
PALM_API_KEY=votre_cle_api_google_genai
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=votre_mot_de_passe
```

> ⚠️ Ne partagez jamais votre clé API ou votre mot de passe Neo4j publiquement.

---

## 🗃️ Préparation des données

Avant de lancer l'application, les données doivent être préparées et indexées.

Depuis le dossier `backend/` :

```bash
python preprocess.py
```

Cette étape permet notamment de :

* Charger les données
* Préparer les recettes
* Générer les embeddings
* Construire l'index vectoriel
* Préparer les données nécessaires à la recherche

---

## 🚀 Démarrer le Backend

Depuis le dossier `backend/` :

```bash
python app.py
```

Le serveur Flask démarre sur :

```text
http://127.0.0.1:5000
```

---

## 🎨 Démarrer le Frontend

Ouvrez un **deuxième terminal**.

Retournez à la racine du projet :

```bash
cd smart-recipe-finder
```

Accédez au frontend :

```bash
cd frontend
```

Lancez Streamlit :

```bash
streamlit run app.py
```

L'interface est accessible sur :

```text
http://localhost:8501
```

---

## 🔄 Démarrage complet

Une fois MongoDB et Neo4j démarrés, le lancement du projet peut être résumé comme suit :

### Terminal 1 — Backend

```bash
cd smart-recipe-finder
.\env\Scripts\activate
cd backend
python preprocess.py
python app.py
```

### Terminal 2 — Frontend

```bash
cd smart-recipe-finder
.\env\Scripts\activate
cd frontend
streamlit run app.py
```

---

## 🧪 Exemple d'utilisation

L'utilisateur peut saisir une requête naturelle telle que :

```text
Je cherche une recette avec du poulet, du riz et des légumes.
```

Ou :

```text
Je veux une recette végétarienne rapide avec des tomates et des pâtes.
```

Le système va :

1. Analyser la requête.
2. Générer un embedding.
3. Rechercher les recettes similaires dans ChromaDB.
4. Récupérer les informations détaillées depuis MongoDB.
5. Exploiter les relations disponibles dans Neo4j.
6. Fournir le contexte au modèle Google GenAI.
7. Générer une réponse personnalisée.
8. Afficher le résultat dans l'interface Streamlit.

---

## 🧱 Technologies utilisées

| Technologie              | Utilisation               |
| ------------------------ | ------------------------- |
| 🐍 Python                | Langage principal         |
| 🌐 Flask                 | Backend / API REST        |
| 🎨 Streamlit             | Interface utilisateur     |
| 🍃 MongoDB               | Stockage des recettes     |
| 🔎 ChromaDB              | Recherche vectorielle     |
| 🕸️ Neo4j                | Graphe de connaissances   |
| 🤖 Google GenAI          | IA générative             |
| 🧠 Sentence Transformers | Génération des embeddings |
| 🔗 Cypher                | Requêtes Neo4j            |
| 📦 Git / GitHub          | Gestion du code source    |

---

## 📊 Fonctionnalités principales

* ✅ Recherche de recettes en langage naturel
* ✅ Recherche sémantique
* ✅ Recommandations personnalisées
* ✅ Recherche vectorielle avec ChromaDB
* ✅ Stockage des recettes avec MongoDB
* ✅ Graphe de connaissances avec Neo4j
* ✅ Génération d'embeddings avec Sentence Transformers
* ✅ Génération de réponses avec Google GenAI
* ✅ Architecture RAG
* ✅ Interface interactive avec Streamlit
* ✅ API backend avec Flask
* ✅ Possibilité d'afficher des tutoriels vidéo
* ✅ Conseils nutritionnels contextualisés

---

## 🔒 Sécurité

Les informations sensibles doivent être stockées dans des variables d'environnement et ne doivent jamais être directement écrites dans le code source.

Exemple :

```env
PALM_API_KEY=votre_cle_api
NEO4J_PASSWORD=votre_mot_de_passe
```

Le fichier `.env` doit être ignoré par Git grâce au fichier `.gitignore`.

---

## 📄 Documentation

Le rapport technique du projet est disponible dans le dossier :

```text
docs/rapport-technique.pdf
```

---

## 👥 Auteurs

Projet d'ingénierie réalisé dans le cadre du cycle **Big Data Engineering** à l'**Université Internationale de Rabat (UIR)**.

### Encadrement académique

* **M. Hamza Gamouh**
* **M. Hakim Hafidi**

---

## 📜 Licence

Ce projet a été réalisé dans un cadre académique.

Toute utilisation, modification ou redistribution du projet doit respecter les conditions définies par ses auteurs.
