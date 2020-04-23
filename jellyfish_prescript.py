# Last revised 4/15/20
# Script containing logic to output adjacency list (saved graph), routing files and tests
# Run this prior to jellyfish_network.py to generate files

import os
import sys
import networkx
import random
import matplotlib.pyplot as plt
import pickle
import networkx as nx
import util as util

# custom class to build Jellyfish graph
from jellyfish_graph import Jellyfish 

TRANSFORM_DIR = 'transformed_routes'
PKL_DIR = 'pickled_routes'


''' Get graph, convert to networkx graph, save adjacency list to store graph '''
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

def get_tests(n):
    ''' get random sampling of tests '''

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
        f.write("h" + str(c) + " iperf -c h" + str(s) + " -t 90 -e >> perftest/results/single_flow_client.txt &\n")
        g.write("h" + str(s) + " iperf -s -e &\n")
        g.write("h" + str(c) + " iperf -c h" + str(s) + " -P 8 -t 90 -e >> perftest/results/eight_flow_client.txt &\n")

    g.close()
    f.close()


def main():
    ''' output graph files in main directory '''
    #graph = nx.Graph()
    edges = get_graph(20,5)
    #print(edges)
    #print(G.edges())

    # newG = nx.Graph()
    # newG.add_edges_from(edges)
    # print(newG.edges())

    #nx.draw(G)
    #plt.show()
    #graph = nx.Graph(get_graph(10, 5))

    graph = nx.read_adjlist("graph_adjlist", nodetype = int)
    # nx.draw(graph)
    # plt.savefig("called.png")
    # print(nx.info(graph))
    # print(graph.edges())
    
    # nx.write_adjlist(graph, "graph_adjlist")
    n = graph.number_of_nodes()

    ''' output tests in perftest/tests '''
    get_tests(n)

    ''' output routing files in pickled_routes '''
    filename = 'test'
    ecmp_routes = util.compute_ecmp(graph)
    ecmp_path = os.path.join(PKL_DIR, 'ecmp_{}.pkl'.format(filename))
    util.save_obj(ecmp_routes, ecmp_path)

    ksp_routes = util.compute_ksp(graph,8)
    ksp_path = os.path.join(PKL_DIR, 'ksp_{}.pkl'.format(filename))
    util.save_obj(ksp_routes, ksp_path)

    diverse_routes = util.diverse_paths(graph, 8)
    print(diverse_routes)

    ''' output routing files in transformed_routes '''
    k = 8
    t_ecmp_routes = util.transform_paths_dpid(ecmp_path, k)
    t_ecmp_path = os.path.join(TRANSFORM_DIR, 'ecmp_{}_{}.pkl'.format(k, filename))
    util.save_obj(t_ecmp_routes, t_ecmp_path)

    t_ksp_routes = util.transform_paths_dpid(ksp_path, k)
    t_ksp_path = os.path.join(TRANSFORM_DIR, 'ksp_{}_{}.pkl'.format(k, filename))
    util.save_obj(t_ksp_routes, t_ksp_path)

if __name__ == '__main__':
    main()
