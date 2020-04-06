# Project: Load Balancing in Jellyfish Networks

### Instructions to Run
1. Start up the VM on GCP
2. ``` ssh [external IP]``` in two separate terminal windows
3. In terminal window 1, run ``` sudo ~/pox/pox.py forwarding.l2_learning ```
4. In terminal window 2, type ``` cd cs419-project ```
5. In terminal window 2, type ``` sudo python jelly.py ```
6. mininet> ``` pingall ```
7. mininet> ``` exit ``` (may also need to hit ctrl-c to fully exit)
8. ``` sudo mn ``` to clear network (needs to be done after each time you run it)

### Phase 1: Building our Network
The first step in our project is to create and simulate a jellyfish network. We begin by constructing a random graph topology. Based on Singla et al. we construct our random graph using the algorithm that follows:
- Randomly pick a pair of non adjacent switches with free ports. Join them with a link and repeat until no further links can be added.
- If a switch remains with >= 2 free ports (p1, p2), incorporate them by removing a uniform-random existing link (x,y) and adding links (p1, x) and (p2, y).

We constructed our graph using the Mininet framework in order to help simulate our network.

#### Lingering Issues
- FIXED, pingall now reaches all hosts. ~~After some research and a lot of headache, I've discovered that Mininet does not work well with cycles in a graph, which is why it's dropping packets.~~

### Phase 2: KSP & ECMP
