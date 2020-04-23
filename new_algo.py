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
    
    9: for i ← 1, b do                                  # for i in range (0,b)
        10: x ← SAMPLEUNIFORM(p)                        # x = (edge(uv), fraction of edge (t)) e.g. randomly choose edge along p, randomly choose some t:0-1 incl, 
                                                        # loop through all edges in graph, remove all edges where no point along edge is in row
                                                        # for each edge in graph:
                                                            # for each endpoint (a,b) in edge:
                                                                # calc len shortest path a,u + t
                                                                # calc len shortest path a,v + 1-t
                                                                # d = min(above paths)
                                                                # if d < row, remove edge

                                                            # for each ednpoint, find distance from endpoint to x.
                                                            # e.g. Find min length distance from the endpoint to each of x's endpoints  
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

# find up to k diverse paths
def diverse_paths(graph, k=8):

    diverse_paths = {}
    b = 2

    graph_c = graph

    for src in range(n):
        for dst in range(src+1, n):
            S = heuristic(src, dst, graph_c)
            diverse_paths[(str(src), str(dst))] = [p for p in S]

    return diverse_paths
            

def heuristic(src, dst, graph_c, b):
    U = []
    S = []

    if nx.has_path(graph_c, source=src, target=dst)
        p = nx.shortest_path(graph_c, source=src, target=dst)
        U.append((p,graph_c))
        S.add(p)

    while (len(U) > 0):
        p, G = U.pop(0)
        row = 0.1*len(p)

        for i in range(0,b):
            G_c = G
            edge_index = random.randrange(len(p)-1)

            u = p[edge_index]
            v = p[edge_index + 1]

            t = random.random()

            for edge in G_c.edges():
                a = edge[0]
                b = edge[0]

                if nx.has_path(G_c, a, u):
                    path_a_u = nx.shortest_path(G_c, a, u)
                    a_u_len = len(path_a_u) + t

                    path_a_v = nx.shortest_path(G_c, a, v)
                    a_v_len = len(path_a_v) + (1-t)

                    path_b_u = nx.shortest_path(G_c, b, u)
                    b_u_len = len(path_b_u) + t

                    path_b_v = nx.shortest_path(G_c, b, v)
                    b_v_len = len(path_b_v) + (1-t)

                    if a_u_len < row or a_v_len < row or b_u_len < row or b_v_len < row:
                        G_c.remove(a,b)

            if nx.has_path(G_c, src, dst):
                p_c = nx.shortest_path(G_c, src, dst)
                U.append((p_c,G_c))


            if acceptable(p_c, S):
                S.append(p_c)

            if len(S) = k:
                return S
                        
    return S



def acceptable(p_c, S):

    if len(S) < 1:
        return True

    else:
        count = 0
        for row in S:
            for node in row:
                if node in p_c:
                    count += 1

        if float(count)/float(len(p_c)) < 0.9:
            return True

    return False




                    # remove edges as above from G_copy
                    # Find new shortest path between src and dest in G_copy

                    # if path from s--->d
                        # p' = get shortest path
                        # add pair (p', G_copy) to U queue

                    # if P < 90% similar to any other path (the higher the %, the less diverse)
                        # add p' to S

                    # if length of S = k
                        # break

            #return S















