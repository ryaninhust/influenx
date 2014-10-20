import operator

import networkx as nx


def find_max_degree_nodes(graph):
    """Find node with max degrees in current graph """
    x = graph.degree()
    degrees_sorted_list = sorted(x.items(), key=operator.itemgetter(1),
                                 reverse=True)
    return degrees_sorted_list[0][0]


def find_vertex_cover(graph):
    """Find vertex cover using max_degree pop"""
    vertex_cover = []
    undirected_graph = nx.Graph(graph)
    print(undirected_graph.edges())
    while undirected_graph.edges():
        max_degree_node = find_max_degree_nodes(undirected_graph)
        print(max_degree_node)
        vertex_cover.append(max_degree_node)
        undirected_graph.remove_node(max_degree_node)
    return set(vertex_cover)


if __name__ == "__main__":
    test_graph = nx.DiGraph()
    test_graph.add_path([1, 2, 3])
    print(find_vertex_cover(test_graph))
