import heapq
from .utils import get_node_in_neighbors, get_node_out_neighbors
from .vertex_cover import find_vertex_cover

def cal_non_cover_spread(graph, non_cover_node, filter_result):
    out_neighbors = get_node_out_neighbors(non_cover_node)
    spread = 1
    for out in out_neighbors:
        m = (graph.edge[non_cover_node][out]['weight'] *
             filter_result[non_cover_node][out])
        spread += m
    return spread


def init_simpath(graph, eta, simpath_spread_method, back_trace):
    celf_q = []
    vertex_cover_set = find_vertex_cover(graph)
    V = set(graph.nodes())
    V_C = V - vertex_cover_set
    filter_result = {}

    for u in vertex_cover_set:
        U = V_C & get_node_in_neighbors(u)
        theta_u, filter_result[u]= simpath_spread_method(graph, set([u,]), eta, U)
        heapq.heappush(celf_q, (theta_u, u))

    for v in V_C:
        theta_v = cal_non_cover_spread(graph, v, filter_result)
        heapq.heappush(celf_q, (theta_v, v))

    return celf_q


def common_simpath(graph, celf_q, l, k, simpath_spread_method, back_trace, eta):
    S = set()
    spd = 0
    V = set(graph.nodes())

    examined_nodes = set()
    while len(S) < k:
        V_S = V - S
        U = set(heapq.nlargest(l, celf_q))
        if U[0] in examined_nodes:
            celf_q.remove(U[0])
            S.add(U[0][1])
            examined_nodes = set()
            continue
        for x in U:
            if x in examined_nodes:
                continue
            celf_q.remove(x)
            theta_V_x_S = simpath_spread_method(graph, S | set([x]), eta, U)
            theta_V_S_x = back_trace(x, eta, V_S, set())
            theta_S_x = theta_V_x_S + theta_V_S_x
            margin_gain = theta_S_x - spd
            heapq.heappush(celf_q, (margin_gain, x))
            examined_nodes.add(x)
    return S

