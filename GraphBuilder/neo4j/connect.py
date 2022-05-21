import json
import string
from neo4j import GraphDatabase
from GraphBuilder.Parser.json_functions import read_json_file

# pip install neo4j
selectAll = "MATCH (n) RETURN (n)"
deleteAll = "MATCH (n) DETACH DELETE n"


class GraphByNeo4j:

    def __init__(self, port=7687, user="neo4j", password='1234'):
        uri = "neo4j://localhost:"+str(port)
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.session = self.driver.session()

    def executeQuery(self, query):
        tx = self.session.begin_transaction()
        result = tx.run(query)
        tx.commit()
        return result

    def build_graph(self,vertices :list,edges :list):
        for v in vertices:
            query = self.add_vertex(v)
            self.executeQuery(query)

        for e in edges:
            query = self.add_edge(e)
            self.executeQuery(query)


    def add_edge(self, edge) ->string:
        type = edge['type']
        source = edge['from']
        to = edge['to']
        query = "MATCH (a:Node),(b:Node) WHERE a.key = '{}' AND b.key = '{}' CREATE (a)-[r:{}]->(b)".format(source,to,type)
        return query

    def add_vertex(self, vertex) -> string:
        query = 'CREATE '
        key = vertex['key']
        name = vertex['name']
        type = vertex['type']
      # attributes = v['attributes']
        query += "(v{}:{} ".format(key, 'Node') + '{' + "key:'{}', name:'{}', type:'{}'".format(key, name, type) + '})'
        return query

def loading_graph_file(path) -> None:
    data :json = read_json_file(path)
    vertices :list = data['vertices']
    edges :list = data['edges']
    return vertices, edges


if __name__ == "__main__":
    # path = '../../Files/graphs/hssf.json'
    path = '../../Files/graphs/iterableList.json'
    # path = '../../Files/graphs/ron.json'

    vertices, edges = loading_graph_file(path)

    app = GraphByNeo4j()
    app.executeQuery('MATCH (n) DETACH DELETE n')
    app.build_graph(vertices,edges)
    # res = app.executeQuery(selectAll)
