from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

# Charger les variables d'environnement
load_dotenv()

# Récupérer les informations de connexion à partir du fichier .env
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "**********")

class Neo4jConnector:
    """
    Classe pour gérer la connexion et l'exécution des requêtes Cypher dans Neo4j.
    """
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    def close(self):
        """
        Ferme la connexion avec Neo4j.
        """
        self.driver.close()

    def run_query(self, query, parameters=None):
        """
        Exécute une requête Cypher.
        Args:
            query (str): Requête Cypher à exécuter.
            parameters (dict, optional): Paramètres pour la requête. Par défaut, None.
        Returns:
            list: Résultats de la requête.
        """
        if parameters is None:
            parameters = {}
        with self.driver.session() as session:
            result = session.run(query, **parameters)
            return [record for record in result]

# Instance globale pour réutiliser la connexion
neo4j_db = Neo4jConnector()
