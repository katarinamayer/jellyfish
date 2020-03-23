# Project: Load Balancing in Jellyfish Networks

### Phase 1: Building our Network
The first step in our project is to create and simulate a jellfish network. We begin by constructing a random graph topology. Based on Singla et al. we construct our random graph using the algorithm that follows:
- Randomly pick a pair of non adjacent switches with free ports.
- Join them with a link
- Repeat until no further links can be added.
- If a switch remains with >= 2 free ports (p1, p2), incorporate them by removing a uniform-random existing link (x,y) and adding links (p1, x) and (p2, y).

We constructed our graph using the Mininet framework in order to help simulate our network.
