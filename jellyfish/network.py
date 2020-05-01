# Last Revised 4/30/20
# Build jellyfish network on Mininet based on adjacency list

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

        switches = []
        ports = []
        for i in range(self.numSwitches):
            switches.append(self.addSwitch('s' + str(i), stp=True, failMode='standalone'))
            ports.append(self.numPorts)
            
        # Connect each host to a switch
        for i in range(self.numNodes):
            self.addLink(hosts[i], switches[i], bw=100)
            ports[i] -= 1

        with open(adj_list) as f:
            for line in f:
                if line.startswith("#"):
                    continue
                tokens = line.split()
                source_node = tokens[0]
                for dest_node in tokens[1:]:
                    self.addLink(switches[int(source_node)], switches[int(dest_node)], bw=100)


# Required for running topo via --custom flag
topos = {'jelly' : Jellyfish }


# Running the topo via --custom flag DOES NOT run main() below
# Running via sudo network.py calls main()
def main():

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
