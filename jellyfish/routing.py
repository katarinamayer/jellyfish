# Last revised 4/23/20
# Routing algorithms for Jellyfish

from __future__ import division
import pickle
import pdb
import os
import networkx as nx
import random
from itertools import islice
import matplotlib.pyplot as plt


''' implementation to compute equal-cost multipaths (ECMP) with networkx library, 
    inspired by https://github.com/lechengfan/cs244-assignment2/blob/master/build_topology.py '''

def compute_ecmp(): 
    g = nx.read_adjlist("graph_adjlist", nodetype = int)
    n = g.number_of_nodes()
    ecmp_paths = {}
    for src in range(n):
        for dst in range(src+1, n):
            shortest_paths = nx.all_shortest_paths(g, source=src, target=dst)
            ecmp_paths[(str(src), str(dst))] = [p for p in shortest_paths]
    return ecmp_paths


''' implementation to compute k-shortest paths with networkx library, 
    inspired by https://github.com/lechengfan/cs244-assignment2/blob/master/build_topology.py '''

def compute_ksp(k=8):
    g = nx.read_adjlist("graph_adjlist", nodetype = int)
    n = g.number_of_nodes()
    all_ksp = {}
    for src in range(n):
        for dst in range(src+1, n):
            ksp = list(islice(nx.shortest_simple_paths(g, source=src, target=dst), k))
            all_ksp[(str(src), str(dst))] = ksp
    return all_ksp


''' implementation to compute (up to) k diverse short paths '''

def compute_dsp(k=8):
    diverse_paths = {}
    b = 2

    g = nx.read_adjlist("graph_adjlist", nodetype = int, create_using=nx.Graph())
    n = g.number_of_nodes()
    graph_c = g
    # print(nx.info(graph_c))

    # src = 0
    # dst = 1
    # S = heuristic(src, dst, graph_c, b, k)
    # diverse_paths[(str(src), str(dst))] = [p for p in S]

    for src in range(n):
        print("source " + str(src))
        for dst in range(src+1, n):
            print("dest " + str(dst))
            S = heuristic_algorithm(src, dst, graph_c, b, k)
            diverse_paths[(str(src), str(dst))] = [p for p in S]

    return diverse_paths
            

''' diverse short paths algorithm (original implementation)	
	adapted from Voss et al, A Heuristic Approach to Finding Diverse Short Paths
 	https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7139774 '''
    
def heuristic_algorithm(src, dst, graph_c, b, k):
    U = []
    S = []

    if nx.has_path(graph_c, source=src, target=dst):
        p = nx.shortest_path(graph_c, source=src, target=dst)
        U.append((p,graph_c))
        S.append(p)

    while (len(U) > 0):
        (p, G) = U.pop(0)
        for i in range(0,b):

            G_c = nx.Graph()
            G_c.add_edges_from(G.edges())

            edge_index = random.randrange(len(p)-1)

            # print(p)
            u = p[edge_index]
            v = p[edge_index + 1]
            # print(u,v)

            t = random.random()
            row = 0.25*len(p)

            #G_c_edges = G_c.edges()
            toRemove = []
            for edge in G_c.edges():
                a = edge[0]
                b = edge[1]

                if nx.has_path(G_c, a, u):
                    path_a_u = nx.shortest_path(G_c, a, u)
                    a_u_len = len(path_a_u) + t - 1

                    path_a_v = nx.shortest_path(G_c, a, v)
                    a_v_len = len(path_a_v) + (1-t) - 1

                    path_b_u = nx.shortest_path(G_c, b, u)
                    b_u_len = len(path_b_u) + t - 1

                    path_b_v = nx.shortest_path(G_c, b, v)
                    b_v_len = len(path_b_v) + (1-t) - 1

                    if a_u_len <= row or a_v_len <= row or b_u_len <= row or b_v_len <= row:
                        #G_c.remove_edge(a,b)
                        toRemove.append((a,b))

            for edge in toRemove:
                G_c.remove_edge(edge[0], edge[1])

            if G_c.has_edge(u,v):
                G_c.remove_edge(u,v)

            if nx.has_path(G_c, src, dst):
                p_c = nx.shortest_path(G_c, src, dst)
                U.append((p_c,G_c))

                if acceptable(p_c, S):
                    S.append(p_c)
                #print("added to S")

            #if acceptable(p_c, S):
            #if p_c not in

            if len(S) == k:
                return S
    return S


def acceptable(p_c, S):
    if len(S) < 1:
        return True

    else:
        for path in S:
            if path == p_c:
                return False

    return True

    # else:
    #     count = 0
    #     for row in S:
    #         for node in row:
    #             if node in p_c:
    #                 count += 1

    #     if float(count)/float(len(p_c)) < 0.9:
    #         return True

    # return False

