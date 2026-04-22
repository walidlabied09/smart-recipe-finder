from neo4j import GraphDatabase

def test_connection():
    uri = "bolt://localhost:7687"  # Remplacez par votre URI Neo4j
    user = "neo4j"
    password = "******"  # Remplacez par le mot de passe de Neo4j
    
    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        with driver.session() as session:
            result = session.run("RETURN 'Neo4j Connection Successful' AS message")
            for record in result:
                print(record["message"])
    except Exception as e:
        print(f"Erreur de connexion : {e}")
    finally:
        driver.close()

test_connection()
