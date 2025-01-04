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


def insert_persons(conn):
    # Create a node
    created_node = conn.create_node("Person", {"name": "Alice", "age": 30})
    print(f"Created Node:{created_node}")
    created_node = conn.create_node("Person", {"name": "Bob", "age": 35})
    print(f"Created Node:{created_node}")
    created_node = conn.create_node("Person", {"name": "Dario", "age": 26})
    print(f"Created Node:{created_node}")
    created_node = conn.create_node("Person", {"name": "Emily", "age": 23})
    print(f"Created Node:{created_node}\n")

    # Create a "KNOWS" relationship
    relationship = conn.create_relationship(
        "Person", "name", "Alice",
        "Person", "name", "Bob",
        "KNOWS",
        {"since": 2021}
    )
    print(f"Created Relationship:{relationship}")
    relationship = conn.create_relationship(
        "Person", "name", "Dario",
        "Person", "name", "Bob",
        "KNOWS",
        {"since": 2020}
    )
    print(f"Created Relationship:{relationship}")
    relationship = conn.create_relationship(
        "Person", "name", "Emily",
        "Person", "name", "Alice",
        "KNOWS",
        {"since": 2020}
    )
    print(f"Created Relationship:{relationship}\n")

    # Get a node
    retrieved_node = conn.get_node("Person", "name", "Alice")
    print(f"Retrieved Node:{retrieved_node}\n")

    # Update a node
    updated_node = conn.update_node("Person", "name", "Alice", {"age": 31, "name": "Clarissa"})
    print(f"Updated Node:{updated_node}\n")
    
    # Delete a relationship
    result = conn.delete_relationship(
        "Person", "name", "Emily",
        "Person", "name", "Clarissa",
        "KNOWS"
    )
    print(result)

    # Delete a node
    delete_msg = conn.delete_node("Person", "name", "Emily")
    print(delete_msg + '\n')


def insert_poc(conn):
    created_node = conn.create_node("Game", {"name": "Death Stranding"})
    created_node = conn.create_node("Game", {"name": "Metal Gear Solid V: Phantom Pain"})
    created_node = conn.create_node("Person", {"name": "Hideo Kojima"})
    created_node = conn.create_node("Person", {"name": "Norman Reedus"})
    created_node = conn.create_node("Character", {"name": "Sam Porter Bridges"})
    created_node = conn.create_node("Character", {"name": "Daryl Dixon"})
    created_node = conn.create_node("TV_Series", {"name": "The Walking Dead"})
    created_node = conn.create_node("Franchise", {"name": "Metal Gear"})
    created_node = conn.create_node("Platform", {"name": "PC"})
    created_node = conn.create_node("Tag", {"name": "Stealth"})
    created_node = conn.create_node("Tag", {"name": "Mocap"})

    relationship = conn.create_relationship(
        "Person", "name", "Norman Reedus",
        "Character", "name", "Sam Porter Bridges",
        "interprets"
    )
    relationship = conn.create_relationship(
        "Person", "name", "Norman Reedus",
        "Character", "name", "Daryl Dixon",
        "interprets"
    )
    relationship = conn.create_relationship(
        "Person", "name", "Norman Reedus",
        "Game", "name", "Death Stranding",
        "acts_for"
    )
    relationship = conn.create_relationship(
        "Person", "name", "Norman Reedus",
        "TV_Series", "name", "The Walking Dead",
        "acts_for"
    )
    relationship = conn.create_relationship(
        "Character", "name", "Sam Porter Bridges",
        "Game", "name", "Death Stranding",
        "is_character_of"
    )

    relationship = conn.create_relationship(
        "Character", "name", "Daryl Dixon",
        "TV_Series", "name", "The Walking Dead",
        "is_character_of"
    )
    relationship = conn.create_relationship(
        "Person", "name", "Hideo Kojima",
        "Game", "name", "Death Stranding",
        "is_writer"
    )

    relationship = conn.create_relationship(
        "Person", "name", "Hideo Kojima",
        "Game", "name", "Death Stranding",
        "is_director"
    )
    relationship = conn.create_relationship(
        "Person", "name", "Hideo Kojima",
        "Franchise", "name", "Metal Gear",
        "is_creator"
    )
    relationship = conn.create_relationship(
        "Franchise", "name", "Metal Gear",
        "Game", "name", "Metal Gear Solid V: Phantom Pain",
        "has_game"
    )
    relationship = conn.create_relationship(
        "Game", "name", "Metal Gear Solid V: Phantom Pain",
        "Tag", "name", "Stealth",
        "has_tag"
    )
    relationship = conn.create_relationship(
        "Game", "name", "Metal Gear Solid V: Phantom Pain",
        "Platform", "name", "PC",
        "has_platform",
        {"release_date": "2015"}
    )
    relationship = conn.create_relationship(
        "Game", "name", "Death Stranding",
        "Platform", "name", "PC",
        "has_platform"
    )
    relationship = conn.create_relationship(
        "Game", "name", "Death Stranding",
        "Tag", "name", "Mocap",
        "has_tag"
    )
    relationship = conn.create_relationship(
        "Game", "name", "Death Stranding",
        "Genre", "name", "Action",
        "has_genre"
    )
    relationship = conn.create_relationship(
        "Game", "name", "Metal Gear Solid V: Phantom Pain",
        "Genre", "name", "Action",
        "has_genre"
    )
    relationship = conn.create_relationship(
        "TV_Series", "name", "The Walking Dead",
        "Genre", "name", "Action",
        "has_genre"
    )

    # User data
    created_node = conn.create_node("User", {"id": "123456", "name": "Luiz"})
    relationship = conn.create_relationship(
        "User", "id", "123456",
        "Game", "name", "Metal Gear Solid V: Phantom Pain",
        "consumed",
        {
            "rating": 8, 
            "start_date": "20/08/2021",
            "end_date": "15/03/2022",
            "review": "This game is incomplete!"
        }
    )
    relationship = conn.create_relationship(
        "User", "id", "123456",
        "Game", "name", "Death Stranding",
        "consumed",
        {
            "rating": 9, 
            "start_date": "12/12/2023",
            "end_date": "10/01/2024",
            "review": "Great cinematic experience from Kojima!"
        }
    )
    relationship = conn.create_relationship(
        "User", "id", "123456",
        "TV_Series", "name", "The Walking Dead",
        "consumed",
        {
            "rating": 5, 
            "end_date": "12/06/2018",
            "review": "Watched until right before season 3. Lost interest over time."
        }
    )


if __name__ == "__main__":
    neo4j_api = Neo4jAPI("bolt://localhost:7687", "neo4j", "12345678")
    try:
        insert_persons(neo4j_api)
        insert_poc(neo4j_api)
    finally:
        # Close connection
        neo4j_api.close()
