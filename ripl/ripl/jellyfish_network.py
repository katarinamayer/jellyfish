# Last Revised 4/11/20
# Script to build jellyfish network on mininet based on adjacency list
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

'''
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--numNodes', help="Number of hosts", required=True)
    parser.add_argument('--numPorts', help="Number of total ports per switch", required=True)
    parser.add_argument('--numServerPorts', help="Number of ports per switch to reserve to servers", required=True)
    parser.add_argument('--numSwitches', help="Number of Switches", required=True)
    return parser.parse_args()
'''

# Running the topo via --custom flag does not run main()
# Running via sudo network.py calls main()
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
    # network.pingAll()

    network.run( CLI, network )
    info( '* Stopping Network\n' )
    network.stop()

if __name__ == '__main__':
    main()
