'''

Output: A set S of at most k diverse, short paths in G from
s to g.

1: U ← EmptyQueue
2: S ← ∅
3: p ← SHORTESTPATH(G, s, g) #choose a shortest path

Make copy of the graph

4: if p not empty then                      # e.g. while shortest path doesn't fail
    5: enqueue(U,(p, G))                    # add the path and the graph as a pair to the queue.
    6: S ← {p}                              # add path to set.

7: while U not empty do
    8: (p, G) ← dequeue(U)                  # dequeue a path-graph pair
    
    9: for i ← 1, b do                      # for i in range (0,b)
        10: x ← SAMPLEUNIFORM(p)            # get a random node from the path (not endpoints if you can help it)
        11: E0 ← {e ∈ E : d(x, e(t)) ≥ ρ ∀t ∈ [0, 1]}
        12: G0 ← (V, E0)
        13: p0 ← SHORTESTPATH(G0, s, g)
        
        4: if p0 not empty then
            15: enqueue(U,(p0, G0))
        
        16: if ACCEPTABLE(p0) then
            17: S ← S ∪ {p0}
        
        18: if |S| = k then
            19: return S

return S
'''

def diverse_paths(graph, k=8):

    diverse_paths = {}
    b = 2

    graph_copy = graph

    for src in range(n):
        for dst in range(src+1, n):
            U = []
            S = {}
            path_len = nx.shortest_path_length(graph_copy, source=src, target=dst)
            row = 0.1 * path_len

            if nx.has_path(graph_copy, source=src, target=dst)
                p = nx.shortest_path(graph_copy, source=src, target=dst)
                U.append((p,graph_copy))
                S.add(p)

            while (len(U) > 0):
                U.pop(0)

                for i in range(0,b):











