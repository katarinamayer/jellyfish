# Project: Load Balancing in Jellyfish Networks

### Phase 1: Building our Network
The first step in our project is to create and simulate a jellfish network. We begin by constructing a random graph topology. (#TODO) Based on Singla et al. we construct our random graph topology as follows:
- Randomly pick a pair of (non-neighboring) switches with free ports.
- Join them with a link
- Repeat until no further links can be added.
- If a switch remains with >= 2 free ports (p1, p2), incorportate them by removing a uniform-random exisiting link (x,y) and addign links (p1, x) and (p2, y).
