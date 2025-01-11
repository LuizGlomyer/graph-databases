# memgraph

## Running the database
`docker compose up` and go to http://localhost:3000/lab.

## Running the API

>python3 -m venv venv \
>source venv/bin/activate \
>pip install -r requirements.txt

Memgraph baasically uses the same driver as Neo4j. The file `client.py` reuses the same code that is used in the neo4j folder.


## Useful Cypher queries

>Get all nodes and edges
```cypher
MATCH (e) RETURN e
```

>Delete all nodes and edges

```cypher
MATCH (n) DETACH DELETE n
```
