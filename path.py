import random
import networkx as nx
import matplotlib.pyplot as plt
# from jelly import *
from algorithms import *


def ECMP(graph):
    pass


def main():
    pass


if __name__ == "__main__":
    g = nx.erdos_renyi_graph(10, .3, directed=False)
    nx.draw(g)
    plt.show()
    # Assume cost of 1 
    for u in g:
    	for v in g[u]:
    		g[u][v]['cost'] = 1 
    paths = ksp_yen(g, 0, 4)
    print(paths)
    

