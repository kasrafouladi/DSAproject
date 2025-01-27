from lexical_analyzer import *

from build_token_table import *

class ParsNode:
    def __init__(self, ind):
        self.ind = ind
        self.adj = []
        return

n = 0
nt = 0
te = 0
productions = []
pars_table = []
pars_tree = []
token_list = []
terminal = []
symbol = []
candidates = []
par = []
symbol_dict = {}

def enum_symbols(dir="./grammers/cppiler"):
    global n, nt, te, symbol_dict, symbol, terminal
    symbol = []
    p_table = open(dir + "/symbols.txt", 'r')
    symbol = p_table.readline().split()
    n = len(symbol)
    terminal = [False for i in range(n)]
    b = False
    for i in range(n):
        if symbol[i] == 'e':
            b = True
        if b:
            te += 1
        else:
            nt += 1
        terminal[i] = b
        symbol_dict[symbol[i]] = i
    return

def prepare_productions(dir="./grammers/cppiler"):
    global productions, n
    productions = [[] for i in range(n)]
    file = open(dir + "/productions.txt", 'r').read().split()
    for i in range(len(file)):
        file[i] = int(file[i])
    idx = 0
    for i in range(n):
        m = file[idx]
        idx += 1
        productions[i] = [[] for i in range(m)]
        for ii in range(m):
            k = file[idx]
            idx += 1
            for j in range(k):
                productions[i][ii].append(file[idx])
                idx += 1
    return

def prepare_p_table(dir="./grammers/cppiler"):
    global pars_table, candidates, n
    pars_table = [[[] for j in range(n)] for i in range(n)]
    candidates = [[] for i in range(n)]
    file = open(dir + "/ll_1_pars.txt", 'r').read().split()
    for i in range(len(file)):
        file[i] = int(file[i])
    idx = 0
    while idx < len(file):
        i = file[idx]
        j = file[idx + 1]
        idx += 2
        m = file[idx]
        idx += 1
        for k in range(m):
            pars_table[i][j].append(file[idx])
            candidates[i].append(symbol[j])
            idx += 1
    return

def build_pars_tree():
    global pars_tree, candidates, n, token_list, par
    sp_char = {'tokentype': 'Special token', 'token': '$', 'value': '$', 'line': 'inf', 'rank': 'inf'}
    token_list.append(sp_char)
    par = []
    pointer = 0
    cnt = 0
    pars_tree = [ParsNode(symbol_dict["$"]), ParsNode(symbol_dict["Start"])]
    stack = [[symbol_dict["$"], cnt]]
    cnt += 1
    stack.append([symbol_dict["Start"], cnt])
    cnt += 1
    while True:
        stack_back = stack[len(stack) - 1]
        pointer_ind = symbol_dict[token_list[pointer]["token"]]
        rank = token_list[pointer]["rank"]
        line = token_list[pointer]["line"]
        if terminal[stack_back[0]]:
            if pointer_ind == stack_back[0] or symbol[stack_back[0]] == "e":
                stack.pop()
                if symbol[stack_back[0]] != "e":
                    pointer += 1
                if symbol[stack_back[0]] == "$" and pointer == len(token_list):
                    print("\n______________\nDone Parsing!\n______________\n")
                    break
            else:
                print("Hamta Error:")
                if symbol[stack_back[0]] == "$":
                    print(f"In parsing, an eror accoured. An extra token \"{symbol[pointer_ind]}\" is found in line {line}")
                    print(f"Something is wrong about token numebr {rank}")
                else:
                    print(f"In parsing, an eror accoured. Token: \"{symbol[stack_back[0]]}\" is missing in line {line} before \"{pointer_ind}\"")
                    print(f"Something is wrong about token numebr {rank}")
                exit()
        else:
            if len(pars_table[stack_back[0]][pointer_ind]) > 0:
                # reason behind [0]: this is a ll(1) parser but i wrote it in a generalized way
                prod = pars_table[stack_back[0]][pointer_ind][0]
                # [::-1] reverses the string but its like called by value and the list doesn't change
                lst = productions[stack_back[0]][prod][::-1]
                stack.pop()
                for e in lst:
                    stack.append([e, cnt])
                    pars_tree[stack_back[1]].adj.append([e, cnt])
                    pars_tree.append(ParsNode(e))
                    par.append(stack_back[1])
                    cnt += 1
                pars_tree[stack_back[1]].adj.reverse()
            else:
                print("Hamta Error:")
                print(f"In parsing, an eror accoured. One of the token(s): {candidates[stack_back[0]]} are missing in line {line}.")
                print("* $ is a special token which means the end of the file")
                print(f"Something is wrong about token numebr {rank}")
                exit()
    print("----------------------------")
    print("Adjancy list of pars tree:")
    for i in range(len(pars_tree)):
        if len(pars_tree[i].adj) > 0:
            print(f"[{i}, {symbol[pars_tree[i].ind]}]: ( ", end="")
            for e in pars_tree[i].adj:
                print(f"[{e[1]}, {symbol[e[0]]}]", end = " ")
            print(")\n")
    print("----------------------------")
    return

def pars(dir="./sampels/code.cpp", grammer="./grammers/cppiler"):
    global token_list
    print("Loading data ...")
    enum_symbols(grammer)
    prepare_productions(grammer)
    prepare_p_table(grammer)
    print("-----------------\nTokenizing the sampel ...")
    token_list = tokenize(dir)
    print("-----------------\nBuilding the token table ...")
    sort_tokens(token_list)
    print("-----------------\nBuilding the pars tree ...")
    build_pars_tree()
    print("-----------------\nDone!")
    print("byebye")
    return

if __name__ == "__main__":
    pars()