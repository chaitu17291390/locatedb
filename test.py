from neo4j import GraphDatabase, TRUST_ALL_CERTIFICATES

uri = "neo4j://d5bf9943.databases.neo4j.io"
username = "neo4j"
password = "B2ACONAtQtaBYdo4N4WbHYRhM80z2psIQfuVWgiwABE"

driver = GraphDatabase.driver(uri, auth=(username, password), encrypted=True, trust=TRUST_ALL_CERTIFICATES)

try:
    with driver.session() as session:
        result = session.run("MATCH (n) RETURN n LIMIT 10")
        for record in result:
            print(record)
except Exception as e:
    print(f"Failed to connect to Neo4j AuraDB: {e}")
finally:
    driver.close()
