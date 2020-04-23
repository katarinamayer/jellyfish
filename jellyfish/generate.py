# Last revised 4/23/20
# Script containing logic to output adjacency list, routing files and tests
# Run this prior to network.py to generate files

import os
import sys
import networkx
import random
import matplotlib.pyplot as plt
import pickle
import networkx as nx
import util as util

''' Custom routing algorithms '''
import routing as routing

''' Custom class to build Jellyfish graph '''
from graph import Jellyfish 

TRANSFORM_DIR = '../routes/transformed'
PKL_DIR = '../routes/pickled'


''' Get graph, convert to networkx graph
    and save adjacency list to store graph '''

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
    # plt.savefig("graph.png", with_labels=True)
    # print(nx.info(G))
    # print(G.edges())

    nx.write_adjlist(G, "graph_adjlist")

    return G.edges()

''' Get random sampling of tests. 
    Divide hosts in half clients, half servers '''

def get_tests(n):

    HostNums = []
    for i in range(n):
        HostNums.append(i)

    random.shuffle(HostNums)
    clients = HostNums[0::2]
    servers = HostNums[1::2]
    pairs = zip(clients, servers)

    f = open("perftest/tests/single_flow", "w+")
    g = open("perftest/tests/eight_flow", "w+")
    for pair in pairs:
        c = pair[0]
        s = pair[1]

        f.write("h" + str(s) + " iperf -s -e &\n")
        f.write("h" + str(c) + " iperf -c h" + str(s) + " -e >> perftest/results/single_flow.txt &\n")
        g.write("h" + str(s) + " iperf -s -e &\n")
        g.write("h" + str(c) + " iperf -c h" + str(s) + " -P 8 -e >> perftest/results/eight_flow.txt &\n")

    g.close()
    f.close()


def main():
    
    ''' Get graph '''
    edges = get_graph(20,5)
    graph = nx.read_adjlist("graph_adjlist", nodetype = int)
    n = graph.number_of_nodes()

    # nx.draw(graph)
    # plt.savefig("called.png")
    # print(nx.info(graph))
    # print(graph.edges())
    # nx.write_adjlist(graph, "graph_adjlist")

    ''' Output tests in perftest/tests '''
    get_tests(n)

    ''' Output routing files for ECMP, KSP and DP '''
    k = 8

    filename = 'test'
    ecmp_routes = routing.compute_ecmp()
    ecmp_path = os.path.join(PKL_DIR, 'ecmp_{}.pkl'.format(filename))
    util.save_obj(ecmp_routes, ecmp_path)

    ksp_routes = routing.compute_ksp(k)
    ksp_path = os.path.join(PKL_DIR, 'ksp_{}.pkl'.format(filename))
    util.save_obj(ksp_routes, ksp_path)

    diverse_routes = routing.compute_diverse_paths(k)
    print(diverse_routes)
    diverse_path = os.path.join(PKL_DIR, 'dp_{}.pkl'.format(filename))
    util.save_obj(diverse_routes, diverse_path)

    t_ecmp_routes = util.transform_paths_dpid(ecmp_path, k)
    t_ecmp_path = os.path.join(TRANSFORM_DIR, 'ecmp_{}_{}.pkl'.format(k, filename))
    util.save_obj(t_ecmp_routes, t_ecmp_path)

    t_ksp_routes = util.transform_paths_dpid(ksp_path, k)
    t_ksp_path = os.path.join(TRANSFORM_DIR, 'ksp_{}_{}.pkl'.format(k, filename))
    util.save_obj(t_ksp_routes, t_ksp_path)

    t_diverse_routes = util.transform_paths_dpid(diverse_path, k)
    t_diverse_path = os.path.join(TRANSFORM_DIR, 'dp_{}_{}.pkl'.format(k, filename))
    util.save_obj(t_diverse_routes, t_diverse_path)

if __name__ == '__main__':
    main()
