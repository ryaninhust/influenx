import heapq
from .vertex_cover import find_vertex_cover
from .simpath_spread import simpath_spread
from .utils import write_celf_q
#from .simpath_spread import simpath_spread, back_track

def cal_non_cover_spread(graph, non_cover_node, filter_result):
    spread = 1
    for out in filter_result.get(non_cover_node, {}).keys():
        m = (graph.edge[non_cover_node][out]['influence'] *
             filter_result[non_cover_node][out])
        spread += m
    return spread


def init_simpath(graph, eta, optimize=False):
    celf_q = []
    V = set(graph.nodes())

    if not optimize:
        for v in V:
            theta_v,_ = simpath_spread(set([v,]), eta, set(), graph)
            heapq.heappush(celf_q, (theta_v, v))
        return celf_q

    vertex_cover_set = find_vertex_cover(graph)
    V_C = V - vertex_cover_set
    filter_result = {}

    for u in vertex_cover_set:
        U = V_C & set(graph.predecessors(u))
        theta_u, u_vs_dict = simpath_spread(set([u,]), eta, U, graph)

        #dict[v] = theta_V_s(u)
        v_keys = u_vs_dict.keys()
        for v_key in v_keys:
            origin_value = filter_result.get(v_key, {})
            kv_tuples = list(origin_value.items())
            kv_tuples.append((u, u_vs_dict[v_key]))
            filter_result[v_key] = dict(kv_tuples)

        heapq.heappush(celf_q, (theta_u, u))

    for v in V_C:
        theta_v = cal_non_cover_spread(graph, v, filter_result)
        heapq.heappush(celf_q, (theta_v, v))

    return celf_q


def common_simpath(graph, celf_q, l, k, eta):
    S = []
    spd = 0
#    V = set(graph.nodes())

    examined_nodes = set()
    while len(S) < k:
        #V_S = V - S
        U = heapq.nlargest(l, celf_q)
        if U[0] in examined_nodes or (set(U) & examined_nodes) == set(U):
            print(U[0])
            celf_q.remove(U[0])
            S.append(U[0][1])
            examined_nodes = set()
            spd = U[0][0] + spd
            continue
        #theta_V_x_S, V_dict = simpath_spread(S, eta, set(U), graph)
        for x in U:
            if x in examined_nodes:
                continue
            celf_q.remove(x)
            #theta_V_S_x = back_track(x[1], eta, V_S, set(), graph)
            #theta_S_x = V_dict.get(x[1], 0) + theta_V_S_x[0]
            theta_S_x = simpath_spread(set(S) | set([x[1]]), eta, set(), graph)
            margin_gain = theta_S_x[0] - spd
            heapq.heappush(celf_q, (margin_gain, x[1]))
            examined_nodes.add(x)
    write_celf_q(celf_q, './networks/celf_q_test.txt')
    return S

