# neo4j

## Running the database
`docker compose up` and go to http://localhost:7474/browser/.

## Running the API

>python3 -m venv venv \
>source venv/bin/activate \
>pip install -r requirements.txt

Now execute one of these files with Python:

- `api.py` provides a minimal api for general use
- `crud.py` provides an CRUD API that freely create nodes (with classes) and edges.


## Useful Cypher queries

>Get all nodes and edges
```cypher
MATCH (e) RETURN e
```

>Delete all nodes and edges

```cypher
MATCH (n) DETACH DELETE n
```
