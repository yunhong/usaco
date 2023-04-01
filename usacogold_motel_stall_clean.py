
def read_inputs(inputs):
    first_line = inputs[0]
    second_line = inputs[1]
    third_line = inputs[2]
    fourth_line = inputs[3]
    
    N, M = first_line
    second_line = inputs[1]
    C = list(second_line)
    S = list(third_line)
    F = list(fourth_line)

    edges = []
    for i in range(4, 4+M):
        line = inputs[i]
        ui, vi = line
        edges.append((ui, vi))
    # end for
    return [C, S, F, edges]
    

in1 = [[2, 0], [1, 2], [2, 2], [2, 2]]
in2 = [[2, 1], [1, 1], [2, 1], [2, 1], [1, 2]]
in3 = [[2, 1], [1, 1], [2, 1], [1, 2], [1, 2]]
in4 = [[2, 1], [1, 1], [1, 2], [2, 1], [1, 2]]
in5 = [[5, 4], [1, 2, 3, 4, 4], [2, 3, 5, 4, 2], [5, 3, 2, 4, 2], [1, 2], [1, 3], [1, 4], [4, 5]]
in6 = [[5, 5], [4, 3, 2, 4, 3], [3, 4, 3, 4, 2], [2, 3, 4, 4, 3], [1, 2], [2, 3], [3, 1], [4, 1], [4, 5]]
in7 = [[4, 3], [3, 2, 4, 1], [2, 3, 4, 4], [4, 2, 3, 4], [4, 2], [4, 1], [4, 3]]
in8 = [[6, 6], [1, 2, 3, 4, 2, 2], [2, 3, 5, 4, 4, 2], [5, 3, 2, 4, 4, 2], [1, 2], [2, 3], [3, 1], [1, 4], [4, 5], [1, 6]]
inputs = in8
[C, S, F, edges] = read_inputs(inputs)

#print(str([C, S, F, edges]))
# after getting C, S, F, edges, for each node, (color, start_key, final_key)
# and build the adjacency graph
def build_graph(C, S, F, edges):
    N = len(C)
    nodes = N * [0]
    for i in range(N):
        nodes[i] = (i, C[i], S[i], F[i], [])

    for edge in edges:
        (ui, vi) = edge
        u, v = ui - 1, vi - 1
        NB_u = nodes[u][4]
        NB_v = nodes[v][4]
        NB_u.append(v)
        NB_v.append(u)
    # end for
    
    return nodes
# end for build_graph

nodes = build_graph(C, S, F, edges)

for node in nodes:
    print(str(node))
        
# keep track of number of nodes that need to be matched
num_not_matched = 0
for node in nodes:
    if(node[2] != node[3]): num_not_matched += 1

N = len(C)
nodes_visited = N * [0] # global variable
keys_kept = dict() # global variable

def add_dict(dic, key):
    if(key not in dic): dic[key] = 1
    else: dic[key] += 1
    
def sub_dict(dic, key):
    if(dic[key] > 1): dic[key] -= 1
    else: del dic[key]

def get_cand(nodes_visited, NB_u, keys_kept):
    candidates = []
    for v in NB_u:
        if(v == 0):
            candidates.append(v)
        elif(nodes_visited[v] < 2) and (nodes[v][1] in keys_kept):
            candidates.append(v)
    return candidates

# when a node is visited twice, it must be true, otherwise False
def DFS(node):
    global num_not_matched
    if(num_not_matched == 0): return True
    # keep track of keys maintained during the walk process
    index, color, stall_key, final_key, NB_u = node

    nodes_visited[index] += 1
    visit_cnt = nodes_visited[index] # at least 1

    if(visit_cnt == 1): # first time visit
        add_dict(keys_kept, stall_key)
        if(final_key == stall_key): # break a good match, add one of unmatched
            num_not_matched += 1

    if(visit_cnt == 1) or (index == 0):
        candidates = get_cand(nodes_visited, NB_u, keys_kept)
        if(len(candidates) > 0):
            #print('debug: ' + str([node[1:4], candidates, keys_kept, nodes_visited, num_not_matched]))
            for v in candidates:
                result = DFS(nodes[v])
                if(result): return True
            # end for v

    
    # consider the case to put final_key into stall
    if(final_key in keys_kept):
        sub_dict(keys_kept, final_key)
        num_not_matched -= 1
        if(num_not_matched == 0): return True

        candidates = get_cand(nodes_visited, NB_u, keys_kept)
        if(len(candidates) > 0):
            for v in candidates:
                result = DFS(nodes[v])
                if(result): return True
            # end for v
        # undo this step, don't put final_key into this stall
        num_not_matched += 1
        add_dict(keys_kept, final_key)
    # end if

    if(visit_cnt == 1): # undo
        sub_dict(keys_kept, stall_key)
        if(final_key == stall_key): 
            num_not_matched -= 1
    nodes_visited[index] -= 1
    
    return False

# end DFS

res = DFS(nodes[0])
print('result: ' + str(res))


        
        

    





