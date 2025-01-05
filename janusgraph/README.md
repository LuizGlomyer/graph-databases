# janusgraph

## Running the database
`docker compose up` and go to http://localhost:3001/.

## Running the API

>python3 -m venv venv \
>source venv/bin/activate \
>pip install -r requirements.txt

Now execute the following file with Python:

- `api.py` provides a minimal api for general use


## Useful Gremlin queries

>Get all nodes and edges
```python
g.V()
```

>Delete all nodes and edges

```python
g.V().drop()
```
