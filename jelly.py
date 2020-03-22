from mininet.net import Mininet
from mininet.topo import Topo
from mininet.util import dumpNodeConnections

import os
import sys
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

class constructGraph():

	#initialize nums
	def __init__(self, numNodes, numPorts, numSwitches):
        self.numNodes = numNodes
        self.numPorts = numPorts
        self.numSwitches = numSwitches

    '''
    see https://github.com/mininet/mininet/wiki/Introduction-to-Mininet
    class SingleSwitchTopo(Topo):
        "Single switch connected to n hosts."
        def build(self, n=2):
            switch = self.addSwitch('s1')
            # Python's range(N) generates 0..N-1
            for h in range(n):
                host = self.addHost('h%s' % (h + 1))
                self.addLink(host, switch)
    '''

	#algo to create graph
	def build(self):

        hosts = []
        for i in range(numNodes):
            hosts.append(self.addHost('h' + str(i)))

        switches = []
        for i in range(numSwitches):
            switches.append(self.addHost('s' + str(i))

        #randomly pick a pair of (non-neighboring) switches with free ports.



# initalize the actual mininet
def main():

    #get cmd line args for params in future
    numNodes = 10
    numPorts = 10
    numSwitches = 10

    topo = constructGraph(numNodes, numPorts, numSwitches)
    network = Mininet(topo)

    network.start()
    network.pingAll()
    network.stop()
