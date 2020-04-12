# Project: Load Balancing in Jellyfish Networks

### Instructions to Run Basic (Non-Remote Controller)
1. Start up the VM on GCP. ``` ssh [external IP]```
2. In terminal window, ``` cd ../kat/cs419-project ```
3. In terminal window, ``` sudo python jellyfish_network.py ```
4. mininet> ``` pingall ```
5. mininet> ``` iperf ```
6. mininet> ``` exit ```
7. ``` sudo mn ``` to clear network (needs to be done after each run)

### Instructions to Run Remote Controller
1. Start up the VM on GCP. ``` ssh [external IP]``` in two separate terminal windows. ``` cd ../kat/cs419-project ``` in both windows.
2. In terminal window 1, run ``` python jellyfish_prescript.py ``` to generate a new saved graph state in the form of an adjacency list.
3. In terminal window 2, run ``` ~/pox/pox.py riplpox.riplpox --topo=jelly,20,20,5,graph_adjlist --routing=jelly,ecmp_8_test --mode=reactive ```.
4. In terminal window 1, run ``` sudo mn --custom ~/ripl/ripl/mn.py --topo=jelly,20,20,5,graph.adjlist --controller=remote --mac ```
5. mininet> ``` pingall ``` 
6. mininet> ``` iperf h0 h1 ```
7. mininet> ``` exit ```
8. Exit pox controller using ctrl-D

#### Next Steps:
- More robust iperf testing
- KSP

#### Lingering Issues
- FIXED, pingall now reaches all hosts. ~~After some research and a lot of headache, I've discovered that Mininet does not work well with cycles in a graph, which is why it's dropping packets.~~ Manually specified 10.0.X.X IP addresses and added stp and failMode params to addSwitch() calls.
- Iperf test multiple hosts at one time (via script). Could add logic to Mininet startup in jellyfish_network.py script but this does not work with the remote controller since Mininet startup is done by ripl.

#### Done
- Custom topology built and tested
- Configured network to work with a remote controller. e.g. added custom topology flag to ripl/ripl/mn.py (``` topo=jelly,[NHOSTS][NSWITCHES],[NPORTS],[ADJLIST_FILE] ```) which directs to our topo in jellyfish_network.py.
- Modified experiment structure to separate graph generation from network creation. Modified graph implmentation to output adjacency list (saved graph state). Modified Jellyfish topo to process adjacency list file and build network. Fixed riplpox config to work with new structure.
- Configured getRouting() in riplpox/riplpox/util.py for custom routing flag (```--routing=jelly[ROUTING FILE]```). Added the i/o to process the pkl routing file in JellyfishRouting class in ripl/ripl/routing.py.
- Wrote logic for ECMP and routing file output. Created and outputted a "routing file" (pkl file).
