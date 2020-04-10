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

def create_routing_table(paths_file_name, numSwitches):
    table = {}
    for i in range(numSwitches):
        table[str(i)] = {}
    all_paths = load_obj(paths_file_name)
    for key, value in all_paths.items():
        start, end = key
        for pathId in range(len(value)):
            path = value[pathId]
            for i in range(len(path)-1):
                nextHop = path[i+1]
                currentNode = path[i]
                src_dst_pair = (str(start), str(end))
                if src_dst_pair not in table[str(currentNode)]:
                    table[str(currentNode)][src_dst_pair] = {}
                table[str(currentNode)][src_dst_pair][str(pathId)] = str(nextHop)
        #same but for the reverse direction
        for j in range(len(path)-1, 0, -1):
            nextHop = path[j-1]
            currentNode = path[j]
            dst_src_pair = (str(end), str(start))
            if dst_src_pair not in table[str(currentNode)]:
                table[str(currentNode)][dst_src_pair] = {}
            table[str(currentNode)][dst_src_pair][str(pathId)] = str(nextHop)
        
    return table


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

    ''' output routing files '''



if __name__ == '__main__':
    main()
