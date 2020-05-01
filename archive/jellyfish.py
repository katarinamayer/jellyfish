# Last Revised 4/5/20
# Stand alone implementation (old implementation)

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

    def __init__(self, numNodes, numPorts, numServerPorts, numSwitches):
        self.numNodes = numNodes
        self.numPorts = numPorts
        self.numServerPorts = numServerPorts
        self.numSwitches = numSwitches

        super(Jellyfish, self).__init__()

        hosts = []
        for i in range(self.numNodes):
            hosts.append(self.addHost('h' + str(i), ip = "127.0.0." +str(i+1)))

        switches = []
        ports = []
        for i in range(self.numSwitches):
            switches.append(self.addSwitch('s' + str(i)))
            ports.append(self.numPorts) # each switch has all open ports at this point
            

        # Connect each host to a switch
        for i in range(self.numNodes):
            self.addLink(hosts[i], switches[i])
            ports[i] -= 1

        adjacent = self.build_graph(hosts, switches, ports)
        
        # Add link to mininet
        added_to_mininet = []
        for link in adjacent:
            node1 = link[0]
            node2 = link[1]

            # check if opposite pair is in adjacent since do not want to double link
            if((node2, node1) not in added_to_mininet): 
                self.addLink(switches[node1], switches[node2])
                added_to_mininet.append(link)

    # Create graph
    def build_graph(self, hosts, switches, ports):

        '''
        Randomly pick a pair of (non-neighboring)
        switches with free ports, join them with a link,
        repeat until no further links can be added.
        '''

        # Track adjacent switches
        adjacent = set()

        while self.checkPossibleLinks(adjacent, ports):

            index1 = random.randrange(self.numSwitches)
            index2 = random.randrange(self.numSwitches)
            while (index2 == index1):
                index2 = random.randrange(self.numSwitches)

            if (ports[index1] > 0 and ports[index2] > 0):
                if ((index1, index2) not in adjacent):

                    ports[index1] -= 1
                    ports[index2] -= 1

                    adjacent.add((index1, index2))
                    adjacent.add((index2, index1))

        '''
        If a switch remains with >= 2 free ports (p1, p2), 
        incorportate them by removing a uniform-random exisiting link (x,y) 
        and adding links (p1, x) and (p2, y).
        '''

        i = 0
        while i < self.numSwitches:
            if (ports[i] >= 2):
                randLink = random.choice(tuple(adjacent))

                if (randLink[0] == i or randLink[1] == i):
                    i += 0 # restart the loop to choose a new random link

                else:
                    adjacent.remove(randLink)
                    adjacent.remove((randLink[1], randLink[0]))

                    adjacent.add((i, randLink[0]))
                    adjacent.add((randLink[0], i))
                    adjacent.add((i, randLink[1]))
                    adjacent.add((randLink[1], i))
                    ports[i] -= 2
                    i += 1
            i+=1

        '''
        # Remove cycles
        adjacency_matrix = self.detectCycles(adjacent)

        # Use adjacency matrix to re-write adjacent        
        new_adjacent = set()
        for a in range(self.numSwitches):
            for b in range(self.numSwitches):
                if a != b:
                    if adjacency_matrix[a][b] == True:
                        new_adjacent.add((a,b))

        # return new_adjacent
        ''' 

        return adjacent # do not remove cycles


    # Method to check if links are still possible
    def checkPossibleLinks(self, adjacent, ports):
        for i in range(self.numSwitches):
            if (ports[i] > 0):
                for j in range (self.numSwitches):
                    if (ports[j] > 0 and j != i):
                        if((i, j) not in adjacent):
                            return True
        return False

    # Method to detect cycles
    def detectCycles(self, adjacent):
        # loop through set of edges and build adjacency list
        adjacency_matrix = [[False]*self.numSwitches for i in range(self.numSwitches)]
        for link in adjacent:
            node1 = link[0]
            node2 = link[1]
            adjacency_matrix[node1][node2] = True
            adjacency_matrix[node2][node1] = True

        # run BFS
        node = random.randrange(self.numSwitches)
        visited = [False] * (self.numSwitches)
        for i in range(self.numSwitches):
            if visited[i] == False:
                self.removeCycles(i, -1, visited, adjacency_matrix)

        return adjacency_matrix

    # Method to remove cycles
    def removeCycles(self, node, parent, visited, adjacency_matrix):
        visited[node] = True
        for i in range(self.numSwitches):
            if (i != node and i != parent and adjacency_matrix[node][i] == True):
                if visited[i] == False:
                    self.removeCycles(i, node, visited, adjacency_matrix)
                else:
                    # remove the cycle in adjaceny_matrix
                    adjacency_matrix[i][node] = False
                    adjacency_matrix[node][i] = False


def main():

    numNodes = 20
    numPorts = 5
    numServerPorts = 5
    numSwitches = 20

    setLogLevel( 'info' )

    info( '* Creating Network\n' )
    topo = Jellyfish(numNodes=numNodes, numPorts=numPorts, numServerPorts=numServerPorts, numSwitches=numSwitches)
    network = Mininet(topo=topo)

    network.start()

    dumpNodeConnections(network.hosts)
    # network.pingAll()

    network.run( CLI, network )
    info( '* Stopping Network\n' )
    network.stop()

if __name__ == '__main__':
    main()
