from mininet.net import Mininet
from mininet.topo import Topo
from mininet.util import dumpNodeConnections

import os
import sys
import argparse
import random
#import networkx

class Jellyfish(Topo):

    def __init__(self, numNodes, numPorts, numServerPorts, numSwitches):
        self.numNodes = numNodes
        self.numPorts = numPorts
        self.numServerPorts = numServerPorts
        self.numSwitches = numSwitches

        super(Jellyfish, self).__init__()
        self.build()

        # Initialize graph of switch topology using networkx
        # self.graph = nx.Graph()
        # self.graph.add_nodes_from(['s'+str(i) for i in range(numSwitches)])

    #algo to create graph
    def build(self):
        hosts = []
        # print("x")
        for i in range(self.numNodes):
            hosts.append(self.addHost('h' + str(i)))
            #print(hosts[i])

        switches = []
        ports = []
        for i in range(self.numSwitches):
            switches.append(self.addSwitch('s' + str(i)))
            ports.append(self.numPorts)
            # each switch has all open ports at this point

        #Connect each host to a switch --> ASSUME EQUAL NUM OF EACH (for now)
        for i in range(self.numNodes):
            self.addLink(hosts[i], switches[i])
            ports[i] -= 1

        '''
        Randomly pick a pair of (non-neighboring)
        switches with free ports, join them with a link,
        repeat until no further links can be added.
        '''

        # Track adjacent switches
        adjacent = set()
        adjacency_list = [][] # array of sets

        while self.checkPossibleLinks(adjacent, ports):

            index1 = random.randrange(self.numSwitches)
            index2 = random.randrange(self.numSwitches)
            while (index2 == index1):
                index2 = random.randrange(self.numSwitches)

            if (ports[index1] > 0 and ports[index2] > 0):
                if ((index1, index2) not in adjacent):

                    #self.addLink(switches[index1], switches[index2])
                    print("s"+str(index1)+" forms link to s"+str(index2))

                    ports[index1] -= 1
                    ports[index2] -= 1

                    adjacent.add((index1, index2))
                    adjacent.add((index2, index1))

        ''' TODO
        If a switch remains with >= 2 free ports (p1, p2), 
        incorportate them by removing a uniform-random exisiting link (x,y) 
        and adding links (p1, x) and (p2, y).
        '''

        #print("exited loop")

        i = 0
        while i < self.numSwitches:
            if (ports[i] >= 2):

                #print("s"+str(i)+" has more than 2 ports.")

                randLink = random.choice(tuple(adjacent))
                #print(randLink)

                if (randLink[0] == i or randLink[1] == i):
                    i += 0 # restart the loop to choose a new random link

                else:
                    print("s"+str(i)+" has >= 2 ports. Link between "+str(randLink)+" broken. New links between "+str((i, randLink[0]))+" and "+str((i, randLink[1]))+" formed.")
                    adjacent.remove(randLink)
                    adjacent.remove((randLink[1], randLink[0]))

                    adjacent.add((i, randLink[0]))
                    adjacent.add((randLink[0], i))
                    adjacent.add((i, randLink[1]))
                    adjacent.add((randLink[1], i))
                    ports[i] -= 2
                    i += 1

        added = []
        for link in adjacent:
            linkIndex1 = link[0]
            linkIndex2 = link[1]

            if((linkIndex2, linkIndex1) not in added): #check if the opposite is in the adjacent list
                self.addLink(switches[linkIndex1], switches[linkIndex2])
                print("Link between s"+str(linkIndex1)+" and s"+str(linkIndex2)+" added to network.")
                added.append(link)

        self.edge_list = adjacent

    def visualize_graph():
        # Visualize graph
        g = nx.Graph()
        g.add_nodes_from([i for i in range(self.edge_list)])
        for a,b in adjacent:
            g.add_edge(a,b)
        nx.draw(g)
        plt.show()

    # Helper method to check if links are still possible
    def checkPossibleLinks(self, adjacent, ports):
        for i in range(self.numSwitches):
            if (ports[i] > 0):
                for j in range (self.numSwitches):
                    if (ports[j] > 0 and j != i):
                        if((i, j) not in adjacent):
                            return True
        return False

    #def checkCyles(node1, node2, adjacency_list):

    def detectCycles(self, adjacent):
        # loop through set of edges and build adjacency list
        for link in adjacent:
            # create adjacency_matrix
            # use a 2D array of booleans

        # run BFS
        node = random.randrange(self.numSwitches)
        visited = [False] * (self.numSwitches)
        for i in range(self.numSwitches):
            if visited[i] == False:
                self.removeCycles(i, -1, visited, adjacency_matrix)

    def removeCycles(self, node, parent, visited, adjacency_matrix):
        visited[node] = True
        for i in range(self.numSwitches):
            if (i != node and i != parent and adjacency_matrix[node][i] == True):
                if visited[i] == False:
                    self.removeCycles(i, node, visited, adjacency_matrix)
                else:
                    # remove the cycle


# #TODO
# def get_args():
#   parser = argparse.ArgumentParser()
#   parser.add_argument('--numNodes', help="Number of hosts", required=True)
#   parser.add_argument('--numPorts', help="Number of total ports per switch", required=True)
#   parser.add_argument('--numServerPorts', help="Number of ports per switch to reserve to servers", required=True)
#   parser.add_argument('--numSwitches', help="Number of Switches", required=True)
#   return parser.parse_args()


def main():
    '''
    args = get_args()
    numNodes = args.numNodes
    numPorts = args.numPorts
    numServerPorts = arsg.numServerPorts
    numSwitches = args.numSwitches
    '''
    numNodes = 10
    numPorts = 15
    numServerPorts = 5
    numSwitches = 10

    topo = Jellyfish(numNodes=numNodes, numPorts=numPorts, numServerPorts=numServerPorts, numSwitches=numSwitches)
    network = Mininet(topo=topo)

    network.start()
    network.pingAll()
    network.stop()

if __name__ == '__main__':
    main()
