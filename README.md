# Project: Load Balancing in Jellyfish Networks

### Instructions to Run Basic (Non-Remote Controller)
1. Start up the VM on GCP. ``` ssh [external IP]```
2. In terminal window, ``` cd cs419-project ```
3. In terminal window, ``` sudo python jellyfish_network.py ```
4. mininet> ``` pingall ```
5. mininet> ``` exit ``` (may also need to hit ctrl-c to fully exit)
6. ``` sudo mn ``` to clear network (needs to be done after each time you run it)

### Instructions to Run Remote (Custom) Controller
1. Start up the VM on GCP. ``` ssh [external IP]``` in two separate terminal windows. ``` cd cs419-project ``` in both windows.
2. In terminal window 1, run ``` python3 jellyfish_prescript.py ``` to generate a new saved graph state in the form of an adjacency list.
3. In terminal window 2, run ``` ~/pox/pox.py riplpox.riplpox --topo=jelly,20,20,5,graph.adjlist --routing=hashed --mode=reactive ``` I added our Jellyfish topo to ripl/ripl/mn.py as a custom topology which is why it is recognized. This controller uses default "hashed" routing.
4. In terminal window 1, run ``` sudo mn --custom ~/ripl/ripl/mn.py --topo=jelly,20,20,5,graph.adjlist --controller=remote --mac ```
5. Simple connectivity test: ``` pingall ```. Simple iperf test: ``` iperf h1 h2 ```.
6. iperf experiments (TODO)

#### Next Steps:
- (Laurent) in jellyfish_prescript.py, write logic for ecmp. Create and output a "routing file" (pkl file). This will be a command line arg when starting the controller. e.g. The command to run the controller will be ```pox/pox.py riplpox.riplpox --topo=jelly,[NHOSTS][NSWITCHES],[NPORTS],[ADJLIST_FILE] --routing=jelly,[ROUTING_FILE] --mode=reactive ```

#### Lingering Issues
- FIXED, pingall now reaches all hosts. ~~After some research and a lot of headache, I've discovered that Mininet does not work well with cycles in a graph, which is why it's dropping packets.~~

#### Done
- Custom topology built and tested
- Configured network to work with a remote controller. e.g. modified ripl/ripl/mn.py for custom topology flag (``` topo=jelly,[NHOSTS][NSWITCHES],[NPORTS],[ADJLIST_FILE] ```)
- Modified experiment structure (separated graph generation from network creation). Modified graph implmentation to output adjacency list (saved graph state). Modified Jellyfish topo to process adjacency list file and build network. Fixed riplpox config to work with new structure.
- Configured riplpox/riplpox/util.py for custom routing flag (```--routing=jelly[ROUTING FILE]```). Added the i/o to process the pkl routing file in JellyfishRouting class in ripl/ripl/routing.py . To run --routing=jelly, need to uncomment extra path arg in getRouting() in riplpox/riplpox/util.py
