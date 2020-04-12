# Cloud Computing Project: Load Balancing in Jellyfish Networks


### [Instructions for Peer Validators](https://docs.google.com/document/d/1gw0bQXfTPnE98h_51koCD04AAzTgu5nammc-pARR2Jw/edit?usp=sharing)

### Instructions to Run Basic Network
1. Start up the VM on GCP. ``` ssh [external IP]```
2. In terminal window, ``` cd ../kat/cs419-project ```
3. In terminal window, ``` sudo python jellyfish_network.py ```
4. mininet> ``` pingall ```
5. mininet> ``` iperf h0 h1 ```
6. mininet> ``` exit ```
7. ``` sudo mn ``` to clear network (needs to be done after each run)

### Instructions to Run Remote Controller
1. Start up the VM on GCP. ``` ssh [external IP]``` in two separate terminal windows. ``` cd ../kat/cs419-project ``` in both windows.
2. In terminal window 1, run ``` python jellyfish_prescript.py ``` to generate a saved graph state in the form of an adjacency list and custom routing file.
3. In terminal window 2, start the controller.
   1. For default routing, run ``` ~/pox/pox.py riplpox.riplpox --topo=jelly,20,20,5,graph_adjlist ```
   2. For custom routing, run ``` ~/pox/pox.py riplpox.riplpox --topo=jelly,20,20,5,graph_adjlist --routing=jelly,ecmp_8_test --mode=reactive ```
4. In terminal window 1, start the network. Run ``` sudo mn --custom ~/ripl/ripl/mn.py --topo=jelly,20,20,5,graph.adjlist --controller=remote --mac ```
   1. mininet> ``` pingall ```
   2. mininet> ``` iperf h0 h1 ```
   3. mininet> ``` exit ```
8. In terminal 2, exit pox controller by hitting ctrl-D

### Lingering Issues
- FIXED, pingall now reaches all hosts. ~~After some research and a lot of headache, I've discovered that Mininet does not work well with cycles in a graph, which is why it's dropping packets.~~ Manually specified 10.0.X.X IP addresses and added stp and failMode params to addSwitch() calls.
- Iperf tests with multiple hosts at a time (via script). Could add logic to Mininet startup in jellyfish_network.py script but this does not work with the remote controller since Mininet startup is handled by ripl.

### Done
- Built and tested custom Jellyfish topo and network. Jellyfish network was generated based on the topology described in [this paper](https://www.usenix.org/system/files/conference/nsdi12/nsdi12-final82.pdf).
- Configured network to work with a remote controller. Added custom topology flag to ripl/ripl/mn.py (``` topo=jelly,[NHOSTS][NSWITCHES],[NPORTS],[ADJLIST_FILE] ```) which directs to our topo in jellyfish_network.py.
- Separated graph creation from network creation. Before this, we were generating the graph topology at Mininet startup time. Graph is now pre-generated and saved as an adjaceny list. This allows us to generate routing schemes for the saved graph. Jellyfish topo processes the adjacency list file to build the network.
- Added logic for ECMP and routing file output. Routing is "calculated" based on the saved graph and outputted in pickle format.
- Modified getRouting() in riplpox/riplpox/util.py and riplpox/riplpox/riplpox.py for custom routing flag (```--routing=jelly[ROUTING FILE]```) and argument parsing. Added the i/o to process the pkl routing file in JellyfishRouting class in ripl/ripl/routing.py.

### Next Steps:
- More robust iperf testing
- K-shortest paths routing

### Citations
- [Ripl](https://github.com/brandonheller/ripl) library
- [Riplpox](https://github.com/brandonheller/riplpox) library
- [lechengfan](https://github.com/lechengfan/cs244-assignment2/tree/f4f0f06fbb939a8a3bb9a10bd3446363f53bf6b2) repository
