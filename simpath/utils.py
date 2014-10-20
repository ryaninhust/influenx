def get_node_in_neighbors(graph, node):
    """ Collect one node in neighors """
    in_edges = graph.in_edges(node)
    return set([in_edge[0] for in_edge in in_edges])


def get_node_out_neighbors(graph, node):
    """Coolect one node out neighors"""
    out_edges = graph.out_edges(node)
    return set([out_edge[0]] for out_edge in out_edges)
