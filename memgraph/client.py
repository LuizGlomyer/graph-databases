import sys
import os
from neo4j import GraphDatabase

sys.path.append(os.path.abspath("../neo4j"))
from crud import Neo4jAPI
from crud import insert_persons
from crud import insert_poc


if __name__ == "__main__":
    neo4j_api = Neo4jAPI("bolt://localhost:7687", "", "")
    try:
        insert_persons(neo4j_api)
        insert_poc(neo4j_api)
    finally:
        # Close connection
        neo4j_api.close()
