# Last revised 4/23/20
# Auxillary functions for Jellyfish

from __future__ import division
import pickle
import pdb
import os
import networkx as nx
import random
from itertools import islice
import matplotlib.pyplot as plt


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

def get_path_counts(ecmp_paths, all_ksp, traffic_matrix, all_links):
    counts = {}
    # initialize counts for all links
    for link in all_links:
        a, b = link
        counts[(str(a),str(b))] = {"8-ksp":0, "8-ecmp": 0, "64-ecmp": 0} 
        counts[(str(b),str(a))] = {"8-ksp":0, "8-ecmp": 0, "64-ecmp": 0} 
    for start_host in range(len(traffic_matrix)):
        dest_host = traffic_matrix[start_host]
        start_node = start_host/3
        dest_node = dest_host/3
        if start_node == dest_node:
            continue
        # swap them so that start_node < dest_node
        if start_node > dest_node:
            start_node, dest_node = dest_node, start_node
        paths = ecmp_paths[(str(start_node), str(dest_node))]
        if len(paths) > 64:
            paths = paths[:64]
        for i in range(len(paths)):
            path = paths[i]
            prev_node = None
            for node in path:
                if not prev_node:
                    prev_node = node
                    continue
                link = (str(prev_node), str(node))
                if i < 8:
                    counts[link]["8-ecmp"] += 1
                counts[link]["64-ecmp"] += 1
                prev_node = node

        ksp = all_ksp[(str(start_node), str(dest_node))]
        for path in ksp:
            prev_node = None
            for node in path:
                if not prev_node:
                    prev_node = node
                    continue
                link = (str(prev_node), str(node))
                counts[link]["8-ksp"] += 1
                prev_node = node
    
    return counts


def assemble_histogram(path_counts, file_name):
    ksp_distinct_paths_counts = []
    ecmp_8_distinct_paths_counts = []
    #ecmp_64_distinct_paths_counts = []
    

    for _, value in sorted(path_counts.iteritems(), key=lambda (k,v): (v["8-ksp"],k)):
        ksp_distinct_paths_counts.append(value["8-ksp"])
    for _, value in sorted(path_counts.iteritems(), key=lambda (k,v): (v["8-ecmp"],k)):
        ecmp_8_distinct_paths_counts.append(value["8-ecmp"])
    # for _, value in sorted(path_counts.iteritems(), key=lambda (k,v): (v["64-ecmp"],k)):
    #     ecmp_64_distinct_paths_counts.append(value["64-ecmp"])

#   print ksp_distinct_paths_counts
#   print ecmp_8_distinct_paths_counts
#   print ecmp_64_distinct_paths_counts
    x = range(len(ksp_distinct_paths_counts))
    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    ax1.plot(x, ksp_distinct_paths_counts, color='b', label="8 Shortest Paths")
    # ax1.plot(x, ecmp_64_distinct_paths_counts, color='r', label="64-way ECMP")
    ax1.plot(x, ecmp_8_distinct_paths_counts, color='g', label="8-way ECMP")
    plt.legend(loc="upper left");
    ax1.set_xlabel("Rank of Link")
    ax1.set_ylabel("# of Distinct Paths Link is on")
    plt.savefig("plots/%s_plot.png" % file_name)


def random_derangement(n):
    while True:
        v = range(n)
        for j in range(n - 1, -1, -1):
            p = random.randint(0, j)
            if v[p] == j:
                break
            else:
                v[j], v[p] = v[p], v[j]
        else:
            if v[0] != 0:
                return tuple(v)
