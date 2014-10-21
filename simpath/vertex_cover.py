import operator

import networkx as nx


def find_max_degree_nodes(graph, degrees):
    """Find node with max degrees in current graph """
    degrees_sorted_list = sorted(degrees.items(), key=operator.itemgetter(1),
                                 reverse=True)
    return degrees_sorted_list[0][0]


def find_vertex_cover(graph):
    """Find vertex cover using max_degree pop"""
    vertex_cover = []
    undirected_graph = graph.to_undirected()
    degrees = undirected_graph.degree()
    edges_count = len(undirected_graph.edges())
    while edges_count:
        max_degree_node = find_max_degree_nodes(undirected_graph, degrees)
        vertex_cover.append(max_degree_node)
        edges_count = remove_node_edges(undirected_graph,
                                        max_degree_node, degrees, edges_count)
    return set(vertex_cover)


def remove_node_edges(graph, node, degrees, edges_count):
    neighbors = graph.neighbors(node)
    edges_count -= len(neighbors)
    for n in neighbors:
        degrees[n] -= 1
    degrees.pop(node, None)
    graph.remove_node(node)
    return edges_count


if __name__ == "__main__":
    test_graph = nx.DiGraph()
    test_graph.add_path([1, 2, 3])
    print(find_vertex_cover(test_graph))
