#input, N, A, B
# a1, a2, ..., aN
# Q questions
# li, ri for i = 1,..., Q
# find all numbers that fall into [A, B]

# for each q, consider papers from li, ..., ri
# for each paper p from a_li, ..., a_ri
# add to the left or right, or nothing
# pruning at each step, if more than B

def add_paper(list_digs, p):
    #print('debug, add paper: ' + str([list_digs, p]))
    n = len(list_digs)

    for i in range(n):
        digs = list_digs[i]
        digs_left = [p] + digs
        digs_right = digs + [p]
        list_digs.append(digs_left)
        list_digs.append(digs_right)
    #print('deubg: ' + str([list_digs, res]))
    return

def add_paper_dict(dict_digs, p):
    #print('debug, add paper_dict: ' + str([dict_digs, p]))

    list_keys = list(dict_digs.keys())
    n = len(list_keys)
    
    def add_to_dict(k, cnt):
        if(k not in dict_digs): dict_digs[k] = cnt
        else: dict_digs[k] += cnt

    # handle the case of empty string
    char_p = str(p)
    add_to_dict(char_p, 2)

    for i in range(n):
        cand_str = list_keys[i]
        cnt = dict_digs[cand_str]
        cand_left = char_p + cand_str
        cand_right = cand_str + char_p
        add_to_dict(cand_left, cnt)
        add_to_dict(cand_right, cnt)

    #print('deubg, add paper dict_post: ' + str([dict_digs, p]))
    return dict_digs


def process_query(left, right, papers, A, B_digs):
    #print('debug process query: ' + str([left, right]))
    list_digs = [[]]
    
    for i in range(left-1, right):
        list_digs = add_prune(list_digs, papers[i], B_digs)
    # end for i
    
    res = count_atleast(list_digs, A)
    if(False): print(str(['debug', len(res), res]))
    return res


def process_query_2(left, right, papers, A, B):
    # store candidates in a dictionary
    dict_digs = dict()
    
    for i in range(left-1, right):
        dict_digs = add_prune_dict(dict_digs, papers[i], B)
    # end for i
    
    res = count_atleast_dict(dict_digs, A)
    if(False): print(str(['debug', len(res), res]))
    return res    



def process_query_list(left, right_list, res, papers, A, B_digs):
    list_digs = [[]]

    start = left
    for (right, i_query) in right_list:
        for i in range(start-1, right):
            list_digs = add_prune(list_digs, papers[i], B_digs)
        cnt = count_atleast(list_digs, A)
        #print('debug res i cnt: ' + str([i_query, cnt, res]))
        res[i_query] = cnt
        start = right+1
    # end for
    
    #print(str(['debug_list', left, right_list, res]))
    return res


def digs_to_value(digs):
    num = 0
    for d in digs:
        num = 10 * num + d
    return num


def smaller(V_digs, B_digs):
    if(len(V_digs) > len(B_digs)):
        return False
    elif(len(V_digs) < len(B_digs)):
         return True
    for i in range(len(V_digs)):
        if(V_digs[i] > B_digs[i]):
            return False
    return True
    

def pruning(list_digs, B_digs):
    res = []
    for digs in list_digs:
        if(smaller(digs, B_digs)):
            res.append(digs)
    return res

def pruning_dict(dict_digs, B):
    list_keys = list(dict_digs.keys())
    for cand_digs in list_keys:
        cand = int(cand_digs)
        if(cand > B):
            del dict_digs[cand_digs]
    return dict_digs

def add_prune(list_digs, p, B_digs):
    add_paper(list_digs, p) # use the same list
    list_digs = pruning(list_digs, B_digs)
    return list_digs

def add_prune_dict(dict_digs, p, B):
    #print('debug add_prune_dict: ' + str([dict_digs, p, B]))
    dict_digs = add_paper_dict(dict_digs, p) # use the same list
    dict_digs = pruning_dict(dict_digs, B)
    return dict_digs


def count_atleast(list_digs, A):
    cnt = 0
    for digs in list_digs:
        v = digs_to_value(digs)
        if(v >= A):
            cnt += 1
    return cnt

def count_atleast_dict(dict_digs, A):
    #print('debug count atleast: ' + str([A, dict_digs]))
    cnt = 0
    for cand_digs in dict_digs.keys():
        v = int(cand_digs)
        if(v >= A):
            cnt += dict_digs[cand_digs]
    return cnt

def solve(N, A, B, papers, Q, q_list):
    B_digs = [int(c) for c in str(B)]

    res = []
    
    for [left, right] in q_list:
        cnt = process_query(left, right, papers, A, B_digs)
        res.append(cnt)
    return res


def solve_2(N, A, B, papers, Q, q_list):
    

    res = []
    
    for [left, right] in q_list:
        cnt = process_query_2(left, right, papers, A, B)
        res.append(cnt)
    return res


def solve_fast(N, A, B, papers, Q, q_list):
    B_digs = [int(c) for c in str(B)]

    res = Q * [0]
    # for queries with the same left, do it together
    q_list_new = []
    for i in range(len(q_list)):
        left, right = q_list[i]    
        q_list_new.append((left, right, i))

    q_list_new.sort(key = lambda x: (x[0], x[1]))
    # for all queries with the same left, process them together
    left_0, right_0, i_0 = q_list_new[0]
    q_list_left = [(left_0, [(right_0, i_0)])]
                   
    for [left, right, i] in q_list_new[1:]:
        if(left == q_list_left[-1][0]):
            q_list_left[-1][1].append((right, i))
        else:
            item = [left, [(right, i)]]
            q_list_left.append(item)
    # end q_list_left

    if(True): print(q_list_left)
    res = Q * [0]
    
    for [left, right_list] in q_list_left:
        res = process_query_list(left, right_list, res, papers, A, B_digs)

    return res


        

if __name__ == '__main__':

    N, A, B = 5, 13, 327
    papers = [1, 2, 3, 4, 5]
    Q = 3
    q_list = [(1, 2), (1, 3), (2, 5)]
    import time
    t0 = time.time()
    res = solve(N, A, B, papers, Q, q_list)
    t = time.time() - t0
    print('time spent on solve: '+ str(t) + ' seconds')
    for item in res:
        print(item)

    
    t0 = time.time()
    res = solve_fast(N, A, B, papers, Q, q_list)
    t = time.time() - t0
    print('time spent on solve_fast: '+ str(t) + ' seconds')
    for item in res:
        print(item)
        

    t0 = time.time()
    res = solve_2(N, A, B, papers, Q, q_list)
    t = time.time() - t0
    print('time spent on solve_2: '+ str(t) + ' seconds')
    for item in res:
        print(item)



        

    
