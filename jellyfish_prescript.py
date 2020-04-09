# Last revised 4/9/20
# Script containing logic to output adjacency list (saved graph) and routing files
# Run this prior to jellyfish_network.py to generate files

import os
import sys
import networkx
import random
import matplotlib.pyplot as plt
import pickle
from graphviz import Graph
import networkx as nx

# custom class to build Jellyfish graph
from jellyfish_graph import Jellyfish 


def compute_ecmp(graph): 
    # graph param is a networkx graph
    return 0

def compute_ksp(graph):
    return 0



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
    nx.write_adjlist(graph, "graph.ADJLIST")

    ''' output routing files '''



if __name__ == '__main__':
    main()