import heapq


def get_node_in_neighbors(graph, node):
    """ Collect one node in neighors """
    in_edges = graph.in_edges(node)
    return set([in_edge[0] for in_edge in in_edges])


def get_node_out_neighbors(graph, node):
    """Coolect one node out neighors"""
    out_edges = graph.out_edges(node)
    return set([out_edge[0]] for out_edge in out_edges)


def write_celf_q(celf_q, path):
    with open(path, 'w') as celf_q_file:
        celf_q_file.writelines('%f %s\n' % t for t in celf_q)


def read_celf_q(path, selected_node_list):
    celf_q = []
    with open(path) as celf_q_file:
        for t in celf_q_file.readlines():
            celf_str = t.strip().split(' ')
            celf_t = (float(celf_str[0]), int(celf_str[1]))
            if celf_t[1] in selected_node_list:
                continue
            celf_q.append(celf_t)
    heapq.heapify(celf_q)
    return celf_q


