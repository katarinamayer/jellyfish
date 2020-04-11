import pickle
import pdb
import os
import networkx as nx

def compute_ecmp(graph): 
    '''
    Assumptions made: nodes are labelled from 0 to n,
    where n is the number of nodes in the graph
    '''
    n = graph.number_of_nodes()
    ecmp_paths = {}
    for src in range(n):
        for dst in range(src+1, n):
            shortest_paths = nx.all_shortest_paths(graph, source=src, target=dst)
            ecmp_paths[(str(src), str(dst))] = [p for p in shortest_paths]
    return ecmp_paths

def compute_ksp(graph, k=8):
    n = graph.number_of_nodes()
    all_ksp = {}
    for a in range(n):
        for b in range(src+1, n):
            ksp = list(islice(nx.shortest_simple_paths(networkx_graph, source=str(src), target=str(dst)), k))
            all_ksp[(str(src), str(dst))] = ksp
    return all_ksp

def save_obj(obj, path):
    with open(path, 'wb') as f:
        pickle.dump(obj,f, protocol=0)

def load_obj(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

def transform_paths_dpid(paths_file_name, maxLen):
	all_paths = load_obj(paths_file_name)
	table = {}
	for key, value in all_paths.items():
		key_dpid = (switch_to_dpid(key[0]), switch_to_dpid(key[1]))
		table[key_dpid] = []
		reversed_key = (switch_to_dpid(key[1]), switch_to_dpid(key[0]))
		table[reversed_key] = []
		for path in value[:maxLen]:
			transformed_path = list(map(switch_to_dpid, path))
			table[key_dpid].append(transformed_path)
			table[reversed_key].append(transformed_path[::-1])
	return table

def switch_to_dpid(switchIndex):
	return str(switchIndex) + "_1"

