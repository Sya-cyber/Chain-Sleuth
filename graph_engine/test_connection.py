from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "password"

def test_connection():
    driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))
    
    try:
        driver.verify_connectivity()
        print("✅ Successfully connected to Neo4j!")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
    finally:
        driver.close()

if __name__ == "__main__":
    test_connection()