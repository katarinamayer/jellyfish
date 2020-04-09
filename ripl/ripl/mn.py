"""Custom topologies for Mininet

author: Brandon Heller (brandonh@stanford.edu)

To use this file to run a RipL-specific topology on Mininet.  Example:

  sudo mn --custom ~/ripl/ripl/mn.py --topo ft,4
"""

from ripl.dctopo import FatTreeTopo #, JellyfishTopo #, VL2Topo, TreeTopo
#from ripl.jellyfish import Jellyfish
from ripl.jellfish_network import Jellyfish 


topos = { 'ft': FatTreeTopo, 'jelly': Jellyfish}
#,
#          'vl2': VL2Topo,
#          'tree': TreeTopo }
