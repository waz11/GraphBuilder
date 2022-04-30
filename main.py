from GraphGenerator import GraphGenerator

if __name__ == '__main__':

    generator = GraphGenerator()
    with open('corpus.txt') as file:
        corpus = [line.rstrip() for line in file]
    for url in corpus: generator.generate_graph_from_git_project(url)

