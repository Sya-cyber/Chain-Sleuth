from neo4j import GraphDatabase  # type: ignore[import-not-found]

#1. Ww are defining connection details
URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "chain_sleuth_password_123"

def test_connection():
    #2. Creating driver instance
    #We pass the URI and a tuple containing (username, passwrd)
    driver = GraphDatabase.drive(URI, auth=(USERNAME, PASSWORD))

    try:
        #3. Try to connect
        driver.verify_connectivity()
        print("Successfully connected to Neo4j")

    except Exception as e:
        #4 Catch the error if the database is asleep or the password is wrong
        print(f"connection failed: {e}")

    finally:
        #5. Always close the driver to free up resources
        driver.close()

    #6. Run the function
    if __name__=="__main__":
        test_connection()
