import pickle
import pdb
import os
import networkx as nx
from itertools import islice

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
    for src in range(n):
        for dst in range(src+1, n):
            ksp = list(islice(nx.shortest_simple_paths(graph, source=src, target=dst), k))
            all_ksp[(str(src), str(dst))] = ksp

    #print(all_ksp)
    return all_ksp

''' Algorithm from https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7139774
def diverse_paths(graph, k=8):

    diverse_paths = {}
    b = 2

    graph_copy = graph

    for src in range(n):
        for dst in range(src+1, n):
            U = []
            S = {}
            path_len = nx.shortest_path_length(graph_copy, source=src, target=dst)
            row = 0.1 * path_len

            if nx.has_path(graph_copy, source=src, target=dst)
                p = nx.shortest_path(graph_copy, source=src, target=dst)
                U.append((p,graph_copy))
                S.add(p)

            while (len(U) > 0):
                U.pop(0)

                for i in range(0,b):
'''

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

