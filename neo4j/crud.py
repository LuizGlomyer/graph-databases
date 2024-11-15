from neo4j import GraphDatabase


class Neo4jAPI:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        with self.driver.session() as session:
            result = session.run("MATCH (n) DETACH DELETE n")


    def close(self):
        self.driver.close()


    def create_node(self, label, properties):
        query = f"CREATE (n:{label} {{ {', '.join([f'{k}: ${k}' for k in properties.keys()])} }}) RETURN n"
        with self.driver.session() as session:
            result = session.run(query, **properties)
            node = result.single()
            return node[0] if node else None


    def get_node(self, label, property_key, property_value):
        query = f"MATCH (n:{label} {{{property_key}: $value}}) RETURN n"
        with self.driver.session() as session:
            result = session.run(query, value=property_value)
            node = result.single()
            return node[0] if node else None


    def update_node(self, label, property_key, property_value, updates):
        set_clause = ', '.join([f"n.{k} = ${k}" for k in updates.keys()])
        query = f"MATCH (n:{label} {{{property_key}: $value}}) SET {set_clause} RETURN n"
        with self.driver.session() as session:
            result = session.run(query, value=property_value, **updates)
            node = result.single()
            return node[0] if node else None


    def delete_node(self, label, property_key, property_value):
        query = f"MATCH (n:{label} {{{property_key}: $value}}) DELETE n RETURN count(n) as count"
        with self.driver.session() as session:
            result = session.run(query, value=property_value)
            count = result.single()["count"]
            return f"Deleted {count} node(s)." if count > 0 else "No node found to delete."


    def create_relationship(self, label1, property_key1, property_value1,
                        label2, property_key2, property_value2,
                        relationship_type, relationship_properties=None):
      relationship_properties = relationship_properties or {}
      relationship_props = ', '.join([f"{k}: ${k}" for k in relationship_properties.keys()])

      query = (
          f"MATCH (a:{label1} {{{property_key1}: $value1}}), (b:{label2} {{{property_key2}: $value2}}) "
          f"CREATE (a)-[r:{relationship_type} {{ {relationship_props} }}]->(b) "
          f"RETURN type(r) AS relationship, properties(r) AS properties"
      )

      parameters = {"value1": property_value1, "value2": property_value2, **relationship_properties}

      with self.driver.session() as session:
        result = session.run(query, **parameters)
        record = result.single()
        return record.data() if record else None


    def delete_relationship(self, label1, property_key1, property_value1,
                         label2, property_key2, property_value2,
                         relationship_type):
      query = (
          f"MATCH (a:{label1})-[r:{relationship_type}]->(b:{label2}) "
          f"WHERE a.{property_key1} = $value1 AND b.{property_key2} = $value2 "
          f"DELETE r"
      )
      
      parameters = {"value1": property_value1, "value2": property_value2}
      
      with self.driver.session() as session:
          session.run(query, **parameters)
          return f"Deleted relationship of type '{relationship_type}' between {property_value1} and {property_value2}."


if __name__ == "__main__":
    neo4j_api = Neo4jAPI("bolt://localhost:7687", "neo4j", "12345678")

    # Create a node
    created_node = neo4j_api.create_node("Person", {"name": "Alice", "age": 30})
    print("Created Node:", created_node)
    created_node = neo4j_api.create_node("Person", {"name": "Bob", "age": 35})
    print("Created Node:", created_node)
    created_node = neo4j_api.create_node("Person", {"name": "Dario", "age": 26})
    print("Created Node:", created_node)
    created_node = neo4j_api.create_node("Person", {"name": "Emily", "age": 23})
    print("Created Node:", created_node)
    print()


    # Create a "KNOWS" relationship
    relationship = neo4j_api.create_relationship(
        "Person", "name", "Alice",
        "Person", "name", "Bob",
        "KNOWS",
        {"since": 2021}
    )
    print("Created Relationship:", relationship)
    relationship = neo4j_api.create_relationship(
        "Person", "name", "Dario",
        "Person", "name", "Bob",
        "KNOWS",
        {"since": 2020}
    )
    print("Created Relationship:", relationship)
    relationship = neo4j_api.create_relationship(
        "Person", "name", "Emily",
        "Person", "name", "Alice",
        "KNOWS",
        {"since": 2020}
    )
    print("Created Relationship:", relationship)
    print()


    # Get a node
    retrieved_node = neo4j_api.get_node("Person", "name", "Alice")
    print("Retrieved Node:", retrieved_node)
    print()


    # Update a node
    updated_node = neo4j_api.update_node("Person", "name", "Alice", {"age": 31, "name": "Clarissa"})
    print("Updated Node:", updated_node)
    print()
    
    
    # Delete a relationship
    result = neo4j_api.delete_relationship(
        "Person", "name", "Emily",
        "Person", "name", "Clarissa",
        "KNOWS"
    )
    print(result)


    # Delete a node
    delete_msg = neo4j_api.delete_node("Person", "name", "Emily")
    print(delete_msg)
    print()

    # Close connection
    neo4j_api.close()
