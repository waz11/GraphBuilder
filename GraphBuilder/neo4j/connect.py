import json
import string
from neo4j import GraphDatabase

# pip install neo4j

# QUERIES:
from GraphBuilder.Parser.json_functions import read_json_file

deleteAll = "MATCH (n) DETACH DELETE n"
selectAll = "MATCH (n) RETURN (n)"


class GraphByNeo4j:

    def __init__(self):
        uri = "neo4j://localhost:7687"
        user = "neo4j"
        password = "1234"

        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.session = self.driver.session()

    # def close(self):
    #     self.driver.close()


    def executeQuery(self, query):
        tx = self.session.begin_transaction()
        result = tx.run(query)
        tx.commit()
        return result

    def build_graph(self,vertices :list,edges :list):
        query = self.__build_vertices(vertices)
        query += self.__build_edges(edges)
        query = query[:-1]
        self.executeQuery(query)

    def __build_edges(self,edges) ->string:
        query = ""
        for e in edges:
            type = e['type']
            source = e['from']
            to = e['to']
            query += "((v{})-[:{}]->(v{})),".format(source, type, to)
        return query

    def __build_vertices(self, vertices) ->string:
        query = 'CREATE '
        for v in vertices:
            key = v['key']
            name = v['name']
            type = v['type']
            # attributes = v['attributes']
            obj = 'Class'
            if type=='method': obj='Method'
            elif type=='interface': obj='Interface'
            query += "(v{}:{} ".format(key,'Node') + '{' + "key:'{}', name:'{}', type:'{}'".format(key,name,type) + '}),'
        return query



        # for e in edges:
        #     type = e['type']
        #     source = e['from']
        #     to = e['to']
        #     query = query + "((v{})-[:{}]->(v{})),".format(source, type, to)
        #
        # query = query[:-1]
        # self.executeQuery(query)


def loading_graph_file(path) -> None:
    data :json = read_json_file(path)
    vertices :list = data['vertices']
    edges :list = data['edges']
    return vertices, edges


if __name__ == "__main__":
    vertices, edges = loading_graph_file('../../Files/graphs/Electricity_Billing_System.json')
    app = GraphByNeo4j()
    app.executeQuery('MATCH (n) DETACH DELETE n')
    app.build_graph(vertices,edges)
    # res = app.executeQuery(selectAll)
