
import sys
N = int(sys.argv[1])

def get_factorization(N):
    dict_p = {}

    import math
    max_p = int(math.sqrt(N))
    p = 2

    while(p <= max_p):
        if(N % p == 0): 
            if(p in dict_p): 
                dict_p[p] += 1
            else:
                dict_p[p] = 1
            N /= p
            max_p = int(math.sqrt(N))
        else:
            if(p == 2): p = 3
            else: p += 2
    # end while
    if(N in dict_p): dict_p[N] += 1
    else: dict_p[N] = 1
    
    #print(str(dict_p))
    return dict_p


import math
def cnt_mutual_prime(factors):
    m = 1
    for p in factors.keys():
        v = factors[p]
        factor = math.pow(p, v-1) * (p-1)
    # end for
    return m

def get_list_factors(dict_p):
    list_dict = []
    list_dict.append(dict())

    for (k, v) in dict_p.items():
        n = len(list_dict)
        for i in range(n):
            dict_sub = list_dict[i]
            for v_sub in range(1, v+1):
                dict_sub_exp = dict(dict_sub)
                dict_sub_exp[k] = v_sub
                list_dict.append(dict_sub_exp)
            # end for
        # end for
    # end for (k,v)
    #print(list_dict)
    return list_dict

def get_value(dict_p):
    res = 1

    for (k, v) in dict_p.items():
        #print('debug 62' + str([k, v]))
        res *= pow(k, v)
    # end for
    #print('debug get_value:' + str([dict_p, res, dict_p.items()]))

    return res

def get_num_mutual_prime(dict_p, factor_dict_p):
    dict_new = dict(dict_p)

    for (p, v) in factor_dict_p.items():
        if(dict_new[p] == v): 
            del dict_new[p]
        else:
            dict_new[p] -= v
    
    num_mutual_prime = 1

    for (p, v) in dict_new.items():
        num_mutual_prime *= pow(p, v-1) * (p-1)
    
    return num_mutual_prime


import time

M = 1000000007

def run_faster(N):
    ans = N

    # store 2**gcd(i, N)
    dict_pow = {}

    dict_p = get_factorization(N)
    list_factor_dict_p = get_list_factors(dict_p)
    #print(list_factor_dict_p)

    for factor_dict_p in list_factor_dict_p[0:-1]: # the last element is N, excluded
        d = get_value(factor_dict_p)
        if(d == 1): continue
        
        num_mutual_prime = get_num_mutual_prime(dict_p, factor_dict_p)
        #print('debug d -> get_value:\t' + str([d, factor_dict_p, num_mutual_prime]))
        
        if(d not in dict_pow):
            v = (pow(2, d) - 2) % M
            dict_pow[d] = v

        # exclude N
        ans += (dict_pow[d] * num_mutual_prime) % M
    # end for

    return ans % M


def run(N):
    ans = N

    # store 2**gcd(i, N)
    dict_pow = {}

    for i in range(1, N):
        x = gcd(i, N)
        if(x > 1):
            if(x in dict_pow):
                ans += dict_pow[x]
            else:
                v = (pow(2, x) - 2) % M
                dict_pow[x] = v
                ans += v
            ans %= M
    # end for
    return ans % M

def gcd(i, N): 
    if (i == 0): return N
    return gcd(N % i, i)


t0 = time.time()
res = run(N)

t1 = time.time() 
print('time spent(s):\t' + str(t1 - t0))

res_faster = run_faster(N)

t2 = time.time() 
print('faster time(s):\t' + str(t2 - t1) + ', speedup:' + str((t1 - t0) / (t2 - t1)))

print(str(res))
if(res != res_faster): 
    print('error, result, res_faster different:' + str([res, res_faster]))
