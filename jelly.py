from mininet.net import Mininet
from mininet.topo import Topo
from mininet.util import dumpNodeConnections

import os
import sys
import argparse
import random
#import networkx
# need to import a bunch of mininet shit


'''
Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo

class MyTopo( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        leftHost = self.addHost( 'h1' )
        rightHost = self.addHost( 'h2' )
        leftSwitch = self.addSwitch( 's3' )
        rightSwitch = self.addSwitch( 's4' )

        # Add links
        self.addLink( leftHost, leftSwitch )
        self.addLink( leftSwitch, rightSwitch )
        self.addLink( rightSwitch, rightHost )


topos = { 'mytopo': ( lambda: MyTopo() ) }
'''

class Jellyfish(Topo):

    #initialize nums
    def __init__(self, numNodes, numPorts, numServerPorts, numSwitches):
        
        #Topo.__init__(self)

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
            print(hosts[i])

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
        
        # #Track switch 1
        # marked_switch1 = []

        # # Loop through all switches
        # while len(marked_switch1) < self.numSwitches:
        #     index1 = random.randrange(self.numSwitches)

        #     # Check that switch has not been marked and that it has open ports
        #     while index1 not in marked_switch1 and ports[index1] > 0:

        #         # Track switch2
        #         marked_switch2 = []
        #         index2 = random.randrange(self.numSwitches)

        #         # Check that switch has not been marked, is not equal to index1 and has open ports
        #         while index2 not in marked_switch2 and index2 != index1 and ports[index2] > 0:

        #             # Check that the links are not adjacent
        #             while (index1, index2) not in adjacent:

        #                 # Form new link
        #                 self.addLink(switches[index1], switches[index2])
        #                 print("s"+str(index1)+" links to s"+str(index2))

        #                 ports[index1] -= 1
        #                 ports[index2] -= 1

        #                 # Add new link to set to track adjacency
        #                 adjacent.add((index1, index2))
        #                 adjacent.add((index2, index1))

        #                 # Mark swtich2
        #                 marked_switch2.append(index2)

        #     # Mark switch 1
        #     marked_switch1.append(index1)

        while checkPossibleLinks(adjacent):

            index1 = random.randrange(self.numSwitches)
            print("First switch is s"+str(index1))
            index2 = random.randrange(self.numSwitches)
            print("Second switch is s"+str(index2))
            while (index2 == index1):
                index2 = random.randrange(self.numSwitches)

            if (ports[index1] > 0 and ports[index2] > 0):
                if ((index1, index2) not in adjacent):

                    self.addLink(switches[index1], switches[index2])
                    print("s"+str(index1)+" links to s"+str(index2))

                    ports[index1] -= 1
                    ports[index2] -= 1


                    adjacent.add((index1, index2))
                    adjacent.add((index2, index1))



        '''
        For sampling non-neighbors, just shuffle a list of non-neighbors, iterate through,
        and check whether each node is in a set of closed ports
        '''

    def checkPossibleLinks(self, adjacent):

        for i in range(self.numNodes):
            if (ports[i] > 0):
                for j in range (self.numNodes):
                    if((i, j) not in adjacent):
                        return True

        return False



# #TODO
# def get_args():
#   parser = argparse.ArgumentParser()
#   parser.add_argument('--numNodes', help="Number of hosts", required=True)
#   parser.add_argument('--numPorts', help="Number of total ports per switch", required=True)
#   parser.add_argument('--numServerPorts', help="Number of ports per switch to reserve to servers", required=True)
#   parser.add_argument('--numSwitches', help="Number of Switches", required=True)
#   return parser.parse_args()


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

    topo = Jellyfish(numNodes=numNodes, numPorts=numPorts, numServerPorts=numServerPorts, numSwitches=numSwitches)
    network = Mininet(topo=topo)

    network.start()
    network.pingAll()
    network.stop()

if __name__ == '__main__':
    main()
