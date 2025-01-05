from gremlin_python import statics
from gremlin_python.structure.graph import Graph
from gremlin_python.process.graph_traversal import __
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.anonymous_traversal import traversal


# Create a connection to the Gremlin server
connection = DriverRemoteConnection('ws://localhost:8182/gremlin', 'g',)


# Create the Graph traversal source
graph = Graph()
g = traversal().withRemote(connection)

# Drop all vertices and edges
g.V().drop().iterate()

# Add vertices
g.addV('Person').property('name', 'Alice').property('age', 30).iterate()
g.addV('Person').property('name', 'Bob').property('age', 32).iterate()
g.addV('Person').property('name', 'Clarissa').property('age', 23).iterate()
g.addV('Person').property('name', 'Dario').property('age', 25).iterate()
g.addV('Person').property('name', 'Eric').property('age', 13).iterate()
g.addV('Person').property('name', 'Fernanda').property('age', 46).iterate()


# Add an edge between vertices
g.V().has('name', 'Alice').as_('a').V().has('name', 'Bob').addE('knows').property('since', 2020).property('first_met_in', "School").from_('a').iterate()
g.V().has('name', 'Alice').as_('a').V().has('name', 'Clarissa').addE('knows').property('since', 2015).property('first_met_in', "Home").from_('a').iterate()
g.V().has('name', 'Alice').as_('a').V().has('name', 'Dario').addE('knows').from_('a').iterate()
g.V().has('name', 'Clarissa').as_('a').V().has('name', 'Alice').addE('knows').from_('a').iterate()
g.V().has('name', 'Dario').as_('a').V().has('name', 'Eric').addE('knows').from_('a').iterate()
g.V().has('name', 'Eric').as_('a').V().has('name', 'Fernanda').addE('knows').from_('a').iterate()

connection.close()
