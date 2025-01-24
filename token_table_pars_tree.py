from lexical_analizer import *

#######

def get_first():

    n = 10 # n = number of symbols

    mark = [False for i in range(n)]
    is_par = [False for i in range(n)]
    
    par = [-1 for i in range(n)]

    productions = [[] for i in range(n)]
    terminal = [False for i in range(n)]


    ind = {}
#######################
# initialization of productions
#
# and terminal
#
# it gives a cfg and enumerate it
#######################

    ep = ind["epsilon"]

    first = [set() for i in range(n)]

    back_edge = [[] for i in range(n)]

# time: O(G * T + NT)
    def dfs_first(u, prv = -1):
        # sum of all of this section in the function, time: O(T + NT)
        par[u] = prv
        mark[u] = is_par[u] = True
        if terminal[u]:
            first[u].insert(u)
        # sum of all of this section in the function (we can ignore recurrences becuse we considered all of possible u s), time: O(G * T)
        for v in productions[u]:
            for i in range(len(v)):
                br = True
                if is_par[v[i]]:
                    back_edge[v[i]].append(u)
                else:
                    if not mark[v[i]]:
                        dfs_first(v[i], u)
                    for e in first[v[i]]:
                        if e != ep or i == len(v) - 1: 
                            first[u].insert(e)
                        else:
                            br = False
                if br:
                    break
        is_par[u] = False
        return

# time: O(G * T + NT)
    def dfs_back_edge(u):
        # sum of all of this section in the function, time: O(G * T)
        for v in back_edge[u]:
            while v != u:
                for e in first[u]:
                    first[v].append(e)
                v = par[v]
        # regular dfs, time: O(G + NT)
        mark[u] = True
        for v in productions(u):
            if not mark[v[0]]:
                dfs_back_edge(v[0])
        return
    
    dfs_first(0)
    mark = [False for i in range(n)]
    dfs_back_edge(0)

    return first

def get_follow():
    
    return "goorba"