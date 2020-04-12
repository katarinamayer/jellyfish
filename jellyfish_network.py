# Last Revised 4/9/20
# Script to build network on mininet based on adjacency list
# Refer to running instructions in README

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.util import dumpNodeConnections
from mininet.cli import CLI

from mininet.log import setLogLevel, info
import os
import sys
import argparse
import random
# import networkx as nx

class Jellyfish(Topo):

    def __init__(self, numNodes, numSwitches, numPorts, adj_list):
        self.numNodes = numNodes
        self.numPorts = numPorts
        self.numSwitches = numSwitches

        super(Jellyfish, self).__init__()

        hosts = []
        for i in range(self.numNodes):
            hosts.append(self.addHost('h' + str(i), ip = "10.0." +str(i+1)+".10"))
            #print("10.0." +str(i+1)+".10")
            #print(hosts[i])

        switches = []
        ports = []
        for i in range(self.numSwitches):
            switches.append(self.addSwitch('s' + str(i), stp=True, failMode='standalone'))
            ports.append(self.numPorts) # each switch has all open ports at this point
            
        # Connect each host to a switch
        for i in range(self.numNodes):
            self.addLink(hosts[i], switches[i])
            ports[i] -= 1

        with open(adj_list) as f:
            for line in f:
                if line.startswith("#"):
                    continue
                tokens = line.split()
                source_node = tokens[0]
                for dest_node in tokens[1:]:
                    self.addLink(switches[int(source_node)], switches[int(dest_node)])

    #     adjacent = self.build_graph(hosts, switches, ports)
        
    #     # Add link to mininet
    #     added_to_mininet = []
    #     for link in adjacent:
    #         node1 = link[0]
    #         node2 = link[1]

    #         # check if opposite pair is in adjacent since we don't want to double link
    #         if((node2, node1) not in added_to_mininet): 
    #             self.addLink(switches[node1], switches[node2])
    #             #print("Link between s"+str(node1)+" and s"+str(node2)+" added to network.")
    #             added_to_mininet.append(link)

    # # Create graph
    # def build_graph(self, hosts, switches, ports):

    #     '''
    #     Randomly pick a pair of (non-neighboring)
    #     switches with free ports, join them with a link,
    #     repeat until no further links can be added.
    #     '''

    #     # Track adjacent switches
    #     adjacent = set()

    #     while self.checkPossibleLinks(adjacent, ports):

    #         index1 = random.randrange(self.numSwitches)
    #         index2 = random.randrange(self.numSwitches)
    #         while (index2 == index1):
    #             index2 = random.randrange(self.numSwitches)

    #         if (ports[index1] > 0 and ports[index2] > 0):
    #             if ((index1, index2) not in adjacent):

    #                 ports[index1] -= 1
    #                 ports[index2] -= 1

    #                 adjacent.add((index1, index2))
    #                 adjacent.add((index2, index1))

    #     '''
    #     If a switch remains with >= 2 free ports (p1, p2), 
    #     incorportate them by removing a uniform-random exisiting link (x,y) 
    #     and adding links (p1, x) and (p2, y).
    #     '''

    #     i = 0
    #     while i < self.numSwitches:
    #         if (ports[i] >= 2):
    #             #print("s"+str(i)+" has more than 2 ports.")
    #             randLink = random.choice(tuple(adjacent))

    #             if (randLink[0] == i or randLink[1] == i):
    #                 i += 0 # restart the loop to choose a new random link

    #             else:
    #                 #print("s"+str(i)+" has >= 2 ports. Link between "+str(randLink)+" broken. New links between "+str((i, randLink[0]))+" and "+str((i, randLink[1]))+" formed.")
    #                 adjacent.remove(randLink)
    #                 adjacent.remove((randLink[1], randLink[0]))

    #                 adjacent.add((i, randLink[0]))
    #                 adjacent.add((randLink[0], i))
    #                 adjacent.add((i, randLink[1]))
    #                 adjacent.add((randLink[1], i))
    #                 ports[i] -= 2
    #                 i += 1
    #         i+=1

    #     return adjacent # do not remove cycles

        
    # '''
    # def visualize_graph(edge_list):
    #     # Visualize graph
    #     g = nx.Graph()
    #     g.add_nodes_from([i for i in range(edge_list)])
    #     for a,b in adjacent:
    #         g.add_edge(a,b)
    #     nx.draw(g)
    #     plt.show()
    #     '''

    # # Method to check if links are still possible
    # def checkPossibleLinks(self, adjacent, ports):
    #     for i in range(self.numSwitches):
    #         if (ports[i] > 0):
    #             for j in range (self.numSwitches):
    #                 if (ports[j] > 0 and j != i):
    #                     if((i, j) not in adjacent):
    #                         return True
    #     return False

'''
# TODO
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--numNodes', help="Number of hosts", required=True)
    parser.add_argument('--numPorts', help="Number of total ports per switch", required=True)
    parser.add_argument('--numServerPorts', help="Number of ports per switch to reserve to servers", required=True)
    parser.add_argument('--numSwitches', help="Number of Switches", required=True)
    return parser.parse_args()
'''

def main():
    '''
    args = get_args()
    numNodes = args.numNodes
    numPorts = args.numPorts
    numServerPorts = arsg.numServerPorts
    numSwitches = args.numSwitches
    '''
    numHosts = 20
    numSwitches = 20
    numPorts = 5
    adj_list = "graph_adjlist"

    setLogLevel( 'info' )

    info( '* Creating Network\n' )
    topo = Jellyfish(numNodes=numHosts, numSwitches=numSwitches, numPorts=numPorts, adj_list = adj_list)
    network = Mininet(topo=topo)
    
    network.start()
    dumpNodeConnections(network.hosts)
    network.pingAll()

    network.run( CLI, network )
    info( '* Stopping Network\n' )
    network.stop()

if __name__ == '__main__':
    main()
