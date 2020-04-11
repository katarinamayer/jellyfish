# Last revised 4/9/20
# Script containing logic to output adjacency list (saved graph) and routing files
# Run this prior to jellyfish_network.py to generate files

import os
import sys
import networkx
import random
import matplotlib.pyplot as plt
import pickle
# from graphviz import Graph
import networkx as nx
import jelly_utils as util

# custom class to build Jellyfish graph
from jellyfish_graph import Jellyfish 

TRANSFORM_DIR = 'transformed_routes'
PKL_DIR = 'pickled_routes'

def save_obj(obj, path):
    with open(path, 'wb') as f:
        pickle.dump(obj,f)

def load_obj(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

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


''' Get graph, convert to networkx graph, save ADJLIST file to store graph '''
def get_graph(nSwitches, nPorts): 

    j = Jellyfish(nSwitches, nPorts)
    edge_list = j.adjacent

    G = nx.Graph()
    added = []
    for edge in edge_list:
        node1 = edge[0]
        node2 = edge[1]
        if((node2, node1) not in added):
            G.add_edge(node1, node2)
            added.append(edge)

    # nx.draw(G)
    # plt.savefig("graph.png")

    return G


def main():
    ''' output graph files '''
    graph = get_graph(20, 5)
    nx.write_adjlist(graph, "graph.adjlist")
    n = graph.number_of_nodes()

    ''' output routing files '''
    filename = 'test_1'
    ecmp_routes = compute_ecmp(graph)
    ecmp_path = os.path.join(PKL_DIR, 'ecmp_{}.pkl'.format(filename))
    save_obj(ecmp_routes, ecmp_path)

    k = 8
    t_ecmp_routes = util.transform_paths_dpid('ecmp_{}'.format(filename), k)
    t_ecmp_path = os.path.join(TRANSFORM_DIR, 'ecmp_{}_{}.pkl'.format(k, filename))
    save_obj(t_ecmp_routes, t_ecmp_path)

if __name__ == '__main__':
    main()
