# Script containing logic to output adjacency list (saved graph) and routing files

import os
import sys
import networkx
import random
import matplotlib.pyplot as plt
import pickle
from graphviz import Graph
import networkx as nx

from graph import Jellyfish

def compute_ecmp(graph): # graph will be a network_x graph
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

    nx.write_adjlist(G, "graph.ADJLIST")
    nx.write_edgelist(G, "graph.EDGELIST")


    # nx.draw(G)
    # plt.show()

    return G


''' Simple function to visualize graph for testing '''
def visualize_graph(edge_list):
    dot = Graph()
    added = []
    for link in edge_list:
        node1 = link[0]
        node2 = link[1]

        if((node2, node1) not in added):
            dot.edge(str(node1), str(node2))
            added.append(link)
    dot.view()



def main():
    ''' create files '''

    # testing
    graph = get_graph(20, 5)
    #visualize_graph(graph)


if __name__ == '__main__':
    main()