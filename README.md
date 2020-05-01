# Load Balancing in Jellyfish Networks


### [Instructions for Peer Validators](https://docs.google.com/document/d/12diR7cZjga3QByGUJ_-UPkwQ9HItD67_AWI2WW5HUQ0/edit?usp=sharing)

### [Final Presentation](https://docs.google.com/presentation/d/1VC06KK8xzkOqqk9WotgSNXZwlDYV1wZLeO8lsE6WPMY/edit?usp=sharing)


### Progress Achieved
- [X] Built and tested custom Jellyfish topo and network. Our network is based on the topology described in [Jellyfish: Networking Data Centers Randomly, Singla et al](https://www.usenix.org/system/files/conference/nsdi12/nsdi12-final82.pdf).
- [X] Configured network to work with a remote controller.
- [X] Separated graph creation from network creation. Before this, we were generating the graph topology at Mininet startup time. Graph is now pre-generated and saved as an adjaceny list. This allows us to generate routing schemes for the saved graph. network.py processes the adjacency list file to build the network.
- [X] Added logic for ECMP and K-shortest paths and routing file output. Paths are generated based on the saved graph and outputted in pickle format.
- [X] Modified riplpox files for custom routing flag (```--routing=jelly[ROUTING FILE]```) and argument parsing. Added the I/O to process the pkl routing file in JellyfishRouting class in ripl/ripl/routing.py.
- [X] Implemented K-diverse short paths algorithm, adapted from [A Heuristic Approach to Finding Diverse Short Paths, Voss et al](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7139774)
- [X] Conducted iperf testing and data analysis.

### Lingering Issues
- [X] FIXED, pingall now reaches all hosts. ~~After some research and a lot of headache, I've discovered that Mininet does not work well with cycles in a graph, which is why it's dropping packets.~~ Manually specified 10.0.X.X IP addresses and added stp and failMode params to addSwitch() calls.
- [X] FIXED, wrote a script with tests. Call script using ``` source ``` command in Mininet CLI. ~~Iperf tests with multiple hosts at a time (via script). Could add logic to Mininet startup in jellyfish_network.py script but this does not work with the remote controller since Mininet startup is handled by ripl.~~
- [ ] Launch POX controller directly from within repository directory.


### Citations
- [Jellyfish: Networking Data Centers Randomly, Singla et al](https://www.usenix.org/system/files/conference/nsdi12/nsdi12-final82.pdf)
- [A Heuristic Approach to Finding Diverse Short Paths, Voss et al](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7139774)
- [mininet/mininet](https://github.com/mininet/mininet)
- [brandonheller/ripl](https://github.com/brandonheller/ripl)
- [brandonheller/riplpox](https://github.com/brandonheller/riplpox)
- [lechengfan/cs244](https://github.com/lechengfan/cs244-assignment2)
