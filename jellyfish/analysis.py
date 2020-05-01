# analysis.py
# Last revised 4/30/20
# Process and graph results across all experiments, same code as analysis.ipynb

from os import path
import os
from tabulate import tabulate
from process import *
from collections import defaultdict
import re

import numpy as np
import matplotlib.pyplot as plt


# Set up dirs/filenames
results_dir = 'perftest/results'
dirs = sorted(next(os.walk(results_dir))[1])
host_dirs = defaultdict(list)
hosts = set()
for subdir in dirs:
    num_hosts = int(re.search(r'\d+', subdir).group())
    hosts.add(num_hosts)
    host_dirs[num_hosts].append(results_dir + '/' +subdir)
host_dirs = dict(host_dirs)
hosts = sorted(list(hosts))

metrics = ['transfer', 'throughput', 'latency']
units = ['MBytes', 'MBit/s', '\u03BCs']
protocols = ['dsp', 'ecmp', 'ksp']
exps = ['eight', 'single']
# Filenames in each result directory (all the same)
filenames = [['{0}_{1}.txt'.format(p, e) for p in protocols] for e in exps]
filenames = dict(zip(exps, filenames))


def plot_metric_vs_hosts(ecmp_data, ksp_data, dsp_data, metric, num_conn):
    fig = plt.figure()
    fig, ax = plt.subplots(figsize=(8, 4.5))
    servers = []
    for i in range(len(hosts)):
    	servers.append(hosts[i]/2)

    ax.plot(servers, ecmp_data, label='ECMP', marker='.')
    ax.plot(servers, ksp_data, label='8-Shortest Paths', marker='.')
    ax.plot(servers, dsp_data, label='8-Diverse Short Paths', marker='.')
    
    unit = units[metrics.index(metric)]
    plt.xlabel('Number of Server Pairs', fontsize=12)
    plt.ylabel('Average {} ({})'.format(metric.capitalize(), unit), fontsize=12)

    #plt.suptitle("test", fontsize=12)
    plt.suptitle('{}'.format(metric.capitalize()), fontsize=13)
    if num_conn == 'single':
    	plt.title('{} Flow / Server Pair'.format(num_conn.capitalize()), fontsize=11)
    else:
    	plt.title('{} Parallel Flows / Server Pair'.format(num_conn.capitalize()), fontsize=11)

    ax.legend()

    t_min, t_max = 0, np.max([ecmp_data, ksp_data, dsp_data])
    # plt.axis((hosts[0], hosts[-1], 0, t_max))
    plt.xticks(servers)
    if metric == 'latency':
    	plt.ylim(200000, 600000)   

    plt.show()


def aggregate_average(num_hosts, num_conn):
    dir = host_dirs[num_hosts]
    files = filenames[num_conn]
    ecmp, ksp, dsp = [], [], []
    for subdir in dir:
        dsp.append(read_file(subdir + '/' + files[0]))
        ecmp.append(read_file(subdir + '/' + files[1]))
        ksp.append(read_file(subdir + '/' + files[2]))
    results = [np.mean(results, 0) for results in [dsp, ecmp, ksp]]
    results = [dict(zip(metrics, result)) for result in results]
        
    return dict(zip(protocols, results))


def plot_results(num_conn, metric):
    data = [aggregate_average(num_hosts, num_conn) for num_hosts in hosts]

    ecmp_data = [sub_data['ecmp'][metric] for sub_data in data]
    ksp_data = [sub_data['ksp'][metric] for sub_data in data]
    dsp_data = [sub_data['dsp'][metric] for sub_data in data]
        
    plot_metric_vs_hosts(ecmp_data, ksp_data, dsp_data, metric, num_conn)


plot_results('single', 'throughput')
plot_results('eight', 'throughput')
plot_results('single', 'latency')
plot_results('eight','latency')