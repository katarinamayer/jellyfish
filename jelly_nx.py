# from mininet.net import Mininet
# from mininet.topo import Topo
# from mininet.util import dumpNodeConnections

import os
import sys
import argparse
import random
import copy
import networkx as nx
# need to import a bunch of mininet shit


class Jellyfish():
	#initialize nums
    def __init__(self, numNodes, numPorts, numServerPorts, numSwitches):
        self.numNodes = numNodes
        self.numPorts = numPorts
        self.numServerPorts = numServerPorts
        self.numSwitchPorts = numPorts-numServerPorts
        self.numSwitches = numSwitches

        # Initialize graph of switch topology using networkx
        self.graph = nx.Graph()
        self.graph.add_nodes_from(['s'+str(i+1) for i in range(numSwitches)])
        # nx.set_node_attributes(self.graph, self.numSwitchPorts, "OpenPorts")
        self.build_graph()

    def build_graph(self):
        '''
        Construct graph of switches using jellyfish algorithm
        '''
        self.open = set(self.graph.nodes)
        self.link_switches()

    def link_switches(self):

        openList = copy.deepcopy(list(self.open))
        random.shuffle(openList)

        for n1 in openList:
            n1_closed = False
            for n2 in openList:

                # If equals to itself or is neighbor, continue
                if n1==n2 or n1 in self.graph[n2]: continue

                self.graph.add_edge(n1,n2)

                if not has_open_ports(n2):
                    self.open.remove(n2)

                if not has_open_ports(n1):
                    n1_closed = True
                    break

            if n1_closed: 
                self.open.remove(n1)


    def has_open_ports(s):
        return self.graph.degree[s] < self.numSwitchPorts


#TODO
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--numNodes', help="Number of hosts", required=True)
    parser.add_argument('--numPorts', help="Number of total ports per switch", required=True)
    parser.add_argument('--numServerPorts', help="Number of ports per switch to reserve to servers", required=True)
    parser.add_argument('--numSwitches', help="Number of Switches", required=True)
    return parser.parse_args()


# initalize the actual mininet
def main():
    '''
    args = get_args()
    numNodes = args.numNodes
    numPorts = args.numPorts
    numServerPorts = arsg.numServerPorts
    numSwitches = args.numSwitches
    '''
    numNodes = 10
    numPorts = 10
    numServerPorts = 5
    numSwitches = 10


    topo = Jellyfish(numNodes, numPorts, numServerPorts, numSwitches)
    # network = Mininet(topo)

    # network.start()
    # network.pingAll()
    # network.stop()

if __name__ == '__main__':
    main()
