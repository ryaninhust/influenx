import heapq
from .utils import get_node_in_neighbors, get_node_out_neighbors
from .vertex_cover import find_vertex_cover

def cal_non_cover_spread(graph, non_cover_node, filter_result):
    out_neighbors = get_node_out_neighbors(non_cover_node)
    spread = 1
    for out in out_neighbors:
        m = graph.edge[non_cover_node][out]['weight'] * filter_result[non_cover_node]
        spread += m
    return spread


def cal_simpath(graph, eta, l, k, simpath_spread_method, back_trace):
    CELF_Q = []
    vertex_cover_set = find_vertex_cover(graph)
    V = set(graph.nodes())
    V_C = V - vertex_cover_set
    global_result = {}
    filter_result = {}

    for u in vertex_cover_set:
        U = V_C | get_node_in_neighbors(u)
        theta_u = simpath_spread_method(graph, set([u,]), eta, U)
        global_result[u] = theta_u
        for v in U:
            theta_V_v_u = simpath_spread_method(graph, set([u,v]), eta, U)
            filter_result[u] = theta_V_v_u
        heapq.heappush(CELF_Q, (theta_u, u))

    for v in V_C:
        theta_v = cal_non_cover_spread(graph, v, filter_result)
        heapq.heappush(CELF_Q, (theta_v, v))

    S = set()
    spd = 0

    while len(S) < k:
        U = [heapq.heappop(CELF_Q)[1] for i in range(l)]
        V_S = V - S

        for x in U:
            theta_V_x_S = simpath_spread_method(graph, S | set([x]), eta, U)
            theta_V_S_x = back_trace(x, eta, V_S, set())
            theta_S_x = theta_V_x_S + theta_V_S_x
            margin_gain = theta_S_x - spd
            heapq.heappush(CELF_Q, (margin_gain, x))
        seed = heapq.heappop(CELF_Q)
        S.add(seed[1])
    return S

