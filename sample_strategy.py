import sys
import DiffusionModel


def read_graph_with_status(nodes_file, edges_file, status_file):
    # generate the graph
    model = DiffusionModel.MultiPlayerLTModel(nodes_file, edges_file, player_num=1)
    # store the status of nodes in graph
    nodes_list = list()
    with open(status_file,'r') as f:
        while True:
            line = f.readline()
        if not line:
            break
        nodes = line.strip().split()
        for n in nodes:
        nodes_list.append(int(n))
    for n in nodes_list:
        model.g.node[n]['status'] = 'activated'

    # return a directed graph
    return model.g


def write_result(selected_nodes_list, selected_nodes_file):
    # write selected nodes to file
    with open(selected_nodes_file, 'w') as f:
        for node in selected_nodes_list:
            f.write('%s ' %node)


if __name__ == '__main__':
    player_id = sys.argv[1]
    nodes_file = sys.argv[2]
    edges_file = sys.argv[3]
    status_file = sys.argv[4]
    nodes_num_per_iter = int(sys.argv[5])
    selected_nodes_file = sys.argv[6]
    time_limit_in_sec = sys.argv[7]  

    g = read_graph_with_status(nodes_file, edge_file, status_file)  
  
    #......

    write_result(selected_nodes_list, selected_nodes_file)

    
