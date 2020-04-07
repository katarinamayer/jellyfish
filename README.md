# Project: Load Balancing in Jellyfish Networks

### Instructions to Run Basic (Non-Remote Controller)
1. Start up the VM on GCP. ``` ssh [external IP]```
2. In terminal window, ``` cd cs419-project ```
3. In terminal window, ``` sudo python jelly.py ```
4. mininet> ``` pingall ```
5. mininet> ``` exit ``` (may also need to hit ctrl-c to fully exit)
6. ``` sudo mn ``` to clear network (needs to be done after each time you run it)

### ** Instructions to Run Remote Controller **
1. Start up the VM on GCP. ``` ssh [external IP]``` in two separate terminal windows.
2. In terminal window 1, run ``` ~/pox/pox.py riplpox.riplpox --topo=jelly,20,5,5,20 --routing=hashed --mode=reactive ``` I imported and added our class Jellyfish to ripl/ripl/mn.py as a custom topology which is why this works. This controller uses default "hashed" routing.
3. In terminal window 2, run ``` sudo mn --custom ~/ripl/ripl/mn.py --topo=jelly,20,5,5,20 --controller=remote --mac ```

#### TODO/Next Steps:
- Write and pre-run a script which will to create and output a "routing file" (pkl file). Add this as a command line arg when starting the controller. e.g. The command to run the controller will be ```pox/pox.py riplpox.riplpox --topo=jelly,[N_NODES],[N_PORTS],[N_SERVERPORTS][N_SWITCHES] --routing=jelly,[ROUTING_FILE] --mode=reactive ```
- We can specify multiple types of routing this way by generating different routing files. e.g. ECMP


#### Lingering Issues
- FIXED, pingall now reaches all hosts. ~~After some research and a lot of headache, I've discovered that Mininet does not work well with cycles in a graph, which is why it's dropping packets.~~

#### Done
- Custom toplogy built and tested
- Configured ripl/ripl/mn.py for custom topology flag (```--topo=jelly[N_NODES],[N_PORTS],[N_SERVERPORTS][N_SWITCHES]```)
- Configured riplpox/riplpox/util.py for custom routing flag (```--routing=jelly[ROUTING FILE]```). Added the i/o to process the pkl routing file.
