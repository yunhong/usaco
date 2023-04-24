
class Mootel(object):
    # instance variables
    def init(self, instance):
        [C, S, F, edges] = instance
        self.C, self.S, self.F, self.edges = C, S, F, edges
        self.N = len(self.C)
        self.M = len(self.edges)
        self.NBs = None
        self.node_visit_cnt = self.N * [0] # global variable
        self.keys_kept = dict() # global variable
        
        # keep track of number of nodes that need to be matched
        self.num_not_matched = 0
        for i in range(self.N):
            if(self.F[i] != self.S[i]):
                self.num_not_matched += 1
                
        
    #print(str([C, S, F, edges]))
    # after getting C, S, F, edges, for each node, (color, start_key, final_key)
    # and build the adjacency graph
    def build_graph(self):
        NBs = [[] for i in range(self.N)]
        
        for edge in self.edges:
            (u, v) = edge
            u, v = u - 1, v - 1
            NBs[u].append(v)
            NBs[v].append(u)
        # end for

        self.NBs = NBs
        #print('debug NBs: ' + str(NBs))
        #print('debug edges: ' + str(self.edges))
    # end for build_graph

    def parse_infile(self, fin):
        fp = open(fin)
        T = int(fp.readline().strip())
        instances = []
        for i in range(T):
            instance = self.parse_read_one(fp)
            instances.append(instance)
        # end for
        return instances
            
    def parse_read_one(self, fp):
        fp.readline()
        line = fp.readline()
        N, M = [int(x) for x in line.strip().split()]
        
        line = fp.readline()
        C = [int(x) for x in line.strip().split()]
        
        line = fp.readline()
        S = [int(x) for x in line.strip().split()]
        
        line = fp.readline()
        F = [int(x) for x in line.strip().split()]

        edges = []
        for i in range(M):
            line = fp.readline()
            ui, vi = [int(x) for x in line.strip().split()]
            edges.append((ui, vi))
        # end for
        return [C, S, F, edges]


    def read_inputs(self, inputs): # manual input, not needed for the final one
        i = 0; line = inputs[i]
        N, M = line
                
        i+=1; line = inputs[i]
        C = list(second_line)

        i+=1; line = inputs[i]
        S = list(third_line)

        i+=1; line = inputs[i]
        F = list(line)

        edges = []
        for m in range(M):
            i+=1; line = inputs[i]
            ui, vi = line
            edges.append((ui, vi))
        # end for
        return [C, S, F, edges]


    def add_key(self, key):
        if(key not in self.keys_kept):
            self.keys_kept[key] = 1
        else:
            self.keys_kept[key] += 1
        
    def sub_key(self, key):
        if(self.keys_kept[key] > 1):
            self.keys_kept[key] -= 1
        else:
            del self.keys_kept[key]

    def get_cand(self, NB_u):
        candidates = []
        for v in NB_u:
            #print('debug get cand: ' + str([v, self.C[v], self.keys_kept]))
            if(v == 0): #and (self.node_visit_cnt[v] < 10):
                candidates.append(v)
            elif(self.node_visit_cnt[v] < 2) and (self.C[v] in self.keys_kept):
                candidates.append(v)
        # end for v
        
        return candidates

    # when a node is visited twice, it must be true, otherwise False
    def DFS(self, index):
        DEBUG = False
        if(self.num_not_matched == 0): return True
        # keep track of keys maintained during the walk process
        stall_key = self.S[index]
        final_key = self.F[index]
        color = self.C[index]
        NB_u = self.NBs[index]
        
        self.node_visit_cnt[index] += 1
        visit_cnt = self.node_visit_cnt[index] # at least 1

        if(visit_cnt == 1): # first time visit, pick the stall key
            self.add_key(stall_key)
            if(final_key == stall_key): # break a good match, add one of unmatched
                self.num_not_matched += 1

        if(visit_cnt == 1) or (index == 0):
            candidates = self.get_cand(NB_u)
            if(len(candidates) > 0):
                if(DEBUG):
                    print('debug: ' + str([index, color, stall_key, final_key,
                                       candidates, self.keys_kept, self.node_visit_cnt, self.num_not_matched]))
                for v in candidates:
                    result = self.DFS(v)
                    if(result): return True
                # end for v

        
        # consider the case to put final_key into stall
        if(final_key in self.keys_kept):
            self.sub_key(final_key)
            self.num_not_matched -= 1
            if(self.num_not_matched == 0): return True

            candidates = self.get_cand(NB_u)
            if(len(candidates) > 0):
                for v in candidates:
                    result = self.DFS(v)
                    if(result): return True
                # end for v
            # undo this step, don't put final_key into this stall
            self.num_not_matched += 1
            self.add_key(final_key)
        # end if

        if(visit_cnt == 1): # undo
            self.sub_key(stall_key)
            if(final_key == stall_key): 
                self.num_not_matched -= 1
        self.node_visit_cnt[index] -= 1
        
        return False

    # end DFS

    def mootel_stall(self, fin, fout): 
        instances = self.parse_infile(fin)
        
        T = len(instances)
        fp_write = open(fout, 'w')
        
        for t in range(T):
            instance = instances[t]
            res = self.process_instance(instance)
            if(res): fp_write.write('YES\n')
            else: fp_write.write('NO\n')
            
        # end for t
        fp_write.close()
    # end mootel_stall

    def process_instance(self, instance):
        self.init(instance)
        self.build_graph()

        #for node in nodes: print(str(node))
        res = self.DFS(0)
        return res


    def check(self, f1, f2):
        DEBUG = False
        fp1 = open(f1)
        fp2 = open(f2)
        line_cnt, err_cnt = 0, 0
        while(True):
            r1 = fp1.readline().strip()
            r2 = fp2.readline().strip()
            if(r1 == '') or (r2 == ''): break
            line_cnt += 1
            if(r1 != r2):
                if(DEBUG):
                    print('error: ' + str([f1, f2]) + ', line ' + str(line_cnt) + ': ' + str(r1) + ' != ' + str(r2))
                err_cnt += 1
        # end while
        p = f1.split('.')[0]
        err_rate = str(int(float(err_cnt) / line_cnt * 1000) / 10.0) + '%'
        if(err_cnt == 0):
            print('passed: ' + p + ', num_instances: ' + str(line_cnt))
        else:
            print('failed: ' + p + ', error rate: ' + str([err_cnt, line_cnt, err_rate]))
            
        return True
    
    def main(self):
        in1 = [[2, 0], [1, 2], [2, 2], [2, 2]]
        in2 = [[2, 1], [1, 1], [2, 1], [2, 1], [1, 2]]
        in3 = [[2, 1], [1, 1], [2, 1], [1, 2], [1, 2]]
        in4 = [[2, 1], [1, 1], [1, 2], [2, 1], [1, 2]]
        in5 = [[5, 4], [1, 2, 3, 4, 4], [2, 3, 5, 4, 2], [5, 3, 2, 4, 2], [1, 2], [1, 3], [1, 4], [4, 5]]
        in6 = [[5, 5], [4, 3, 2, 4, 3], [3, 4, 3, 4, 2], [2, 3, 4, 4, 3], [1, 2], [2, 3], [3, 1], [4, 1], [4, 5]]
        in7 = [[4, 3], [3, 2, 4, 1], [2, 3, 4, 4], [4, 2, 3, 4], [4, 2], [4, 1], [4, 3]]
        in8 = [[6, 6], [1, 2, 3, 4, 2, 2], [2, 3, 5, 4, 4, 2], [5, 3, 2, 4, 4, 2], [1, 2], [2, 3], [3, 1], [1, 4], [4, 5], [1, 6]]


        fnames = ['3_1'] #'2_1', '2_2', '2_3', '2_4', '2_5', '1', '2'
        #fnames = [str(p) for p in range(1, 19)]
        for fname in fnames:
            fin = fname + '.in'
            fout = fname + '.out'
            fout_temp = fout + '_temp'
            self.mootel_stall(fin, fout_temp)
            self.check(fout, fout_temp)
        # end for i
            
if __name__ == "__main__":
    obj = Mootel()
    obj.main()
        


        

    





