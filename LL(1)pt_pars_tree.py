from lexical_analizer import *

#######

mark = []
par = []
terminal = []
first = []
productions = []

def dfs_first(u):
    par[u] = True
    if terminal[u]:
        first[u].insert(u)
    for v in productions[u]:
        if not par[v[0]]:
            dfs_first(v[0])
        for e in first[v[0]]:
            first[u].insert(e)
    par[u] = False
    return

