# from mininet.net import Mininet
# from mininet.topo import Topo
# from mininet.util import dumpNodeConnections
# from mininet.cli import CLI
# from mininet.log import setLogLevel, info
import os
import sys
import argparse
import random
import networkx as nx
from graphviz import Graph

# COMMENT OUT ALL MININET, JUST BUILD GRAPH LOCALLY

class Jellyfish():

    def __init__(self, numNodes, numPorts, numServerPorts, numSwitches):
        self.numNodes = numNodes
        self.numPorts = numPorts
        self.numServerPorts = numServerPorts
        self.numSwitches = numSwitches

        super(Jellyfish, self).__init__()

        hosts = []
        # for i in range(self.numNodes):
        #     hosts.append(self.addHost('h' + str(i)))
        #     #print(hosts[i])

        switches = []
        ports = []
        for i in range(self.numSwitches):
            # switches.append(self.addSwitch('s' + str(i)))
            ports.append(self.numPorts)
            # each switch has all open ports at this point

        # Connect each host to a switch
        for i in range(self.numNodes):
            # self.addLink(hosts[i], switches[i])
            ports[i] -= 1

        # For testing
        # self.addLink('s0', 's1')

        adjacent = self.build_graph(hosts, switches, ports)

        # # Add link to mininet
        # added_to_mininet = []
        # for link in adjacent:
        #     node1 = link[0]
        #     node2 = link[1]

        #     if((node2, node1) not in added_to_mininet): #check if the opposite is in the adjacent list
        #         self.addLink(switches[node1], switches[node2])
        #         #print("Link between s"+str(node1)+" and s"+str(node2)+" added to network.")
        #         added_to_mininet.append(link)
        

        # Initialize graph of switch topology using networkx
        # self.graph = nx.Graph()
        # self.graph.add_nodes_from(['s'+str(i) for i in range(numSwitches)])

    # algo to create graph
    
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

        ''' TODO
        If a switch remains with >= 2 free ports (p1, p2), 
        incorportate them by removing a uniform-random exisiting link (x,y) 
        and adding links (p1, x) and (p2, y).
        '''

        i = 0
        while i < self.numSwitches:
            if (ports[i] >= 2):

                #print("s"+str(i)+" has more than 2 ports.")

                randLink = random.choice(tuple(adjacent))

                if (randLink[0] == i or randLink[1] == i):
                    i += 0 # restart the loop to choose a new random link

                else:
                    #print("s"+str(i)+" has >= 2 ports. Link between "+str(randLink)+" broken. New links between "+str((i, randLink[0]))+" and "+str((i, randLink[1]))+" formed.")
                    adjacent.remove(randLink)
                    adjacent.remove((randLink[1], randLink[0]))

                    adjacent.add((i, randLink[0]))
                    adjacent.add((randLink[0], i))
                    adjacent.add((i, randLink[1]))
                    adjacent.add((randLink[1], i))
                    ports[i] -= 2
                    i += 1
            i+=1

        # Remove cycles
        adjacency_matrix = self.detectCycles(adjacent)

        # Use adjacency matrix to re-write adjacent        
        new_adjacent = set()
        for a in range(self.numSwitches):
            for b in range(self.numSwitches):
                if a != b:
                    if adjacency_matrix[a][b] == True:
                        new_adjacent.add((a,b))


        edge_list = new_adjacent
        self.visualize_graph(edge_list)

        return new_adjacent

    def visualize_graph(self, edge_list):
        # Visualize graph
        # g = nx.Graph()
        # g.add_nodes_from([i for i in range(edge_list)])
        # for a,b in adjacent:
        #     g.add_edge(a,b)
        # nx.draw(g)
        # plt.show()

        dot = Graph()
        # for i in range(self.numSwitches):
        #     dot.node(str(i))

        added = []
        for link in edge_list:
            node1 = link[0]
            node2 = link[1]

            if((node2, node1) not in added):
                dot.edge(str(node1), str(node2))
                added.append(link)

        dot.view()

        #dot.edges(['AB', 'AL'])
        #dot.edge('B', 'L', constraint='false')

    # Helper method to check if links are still possible
    def checkPossibleLinks(self, adjacent, ports):
        for i in range(self.numSwitches):
            if (ports[i] > 0):
                for j in range (self.numSwitches):
                    if (ports[j] > 0 and j != i):
                        if((i, j) not in adjacent):
                            return True
        return False

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
    numNodes = 80
    numPorts = 5
    numServerPorts = 5
    numSwitches = 80

    # setLogLevel( 'info' )

    # info( '* Creating Network\n' )
    topo = Jellyfish(numNodes=numNodes, numPorts=numPorts, numServerPorts=numServerPorts, numSwitches=numSwitches)
    # network = Mininet(topo=topo)

    # network.start()

    # dumpNodeConnections(network.hosts)
    # #network.pingAll()

    # network.run( CLI, network )
    # info( '* Stopping Network\n' )
    # network.stop()

if __name__ == '__main__':
    main()
