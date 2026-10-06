# 🥦 Smart Recipe Finder

**Smart Recipe Finder** est une application intelligente de recommandation culinaire basée sur **l'IA générative**, la **recherche vectorielle** et les **bases de données NoSQL et graphes**.

L'application permet aux utilisateurs d'obtenir des suggestions de recettes personnalisées à partir de requêtes formulées en langage naturel, par exemple :

- 🥕 Ingrédients disponibles
- 🍽️ Type de plat recherché
- 🥗 Régime alimentaire
- 🌱 Préférences nutritionnelles
- ⏱️ Temps de préparation
- 💡 Envie ou contexte particulier

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
      │   ChromaDB    │     │   MongoDB     │     │    Neo4j      │
      │ Recherche     │     │ Stockage des  │     │ Graphe des    │
      │ vectorielle   │     │   recettes    │     │ relations     │
      └───────┬───────┘     └───────────────┘     └───────┬───────┘
              │                                             │
              ▼                                             ▼
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
