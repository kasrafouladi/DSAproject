from lexical_analizer import *

class Token:
    def __init__(self, cat, val, id, rank, line, ind):
        self.cat = cat
        self.val = val
        self.id = id
        self.rank = rank
        self.line = line
        self.ind = ind
        return

class ParsNode:
    def __init__(self, ind):
        self.ind = ind
        self.adj = []
        return

n = 0
nt = 0
te = 0
token_list = []
productions = []
pars_table = []
token_table = []
pars_tree = []
terminal = []
symbol = []
childs = []
symbol_dict = {}

def enum_symbols(dir="./grammers/cppiler"):
    global n, nt, te, symbol_dict, symbol
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
    global pars_table, childs, n
    pars_table = [[[] for j in range(n)] for i in range(n)]
    childs = [[] for i in range(n)]
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
            childs[i].append(symbol[j])
            idx += 1
    return

def build_token_table():
    global token_list
    t_list = token_list
    # last part
    return

def build_pars_tree():
    global pars_tree, childs, n
    sp_char = Token("Special", "$", -1, len(token_list) + 1, "EOF", symbol_dict["$"])
    token_list.append(sp_char)
    pars_tree = []
    pointer = 0
    cnt = 0
    stack = [[symbol_dict["$"], cnt]]
    cnt += 1
    stack.append([symbol_dict["Start"], cnt])
    cnt += 1
    while True:
        stack_back = stack[len(stack) - 1]
        if terminal[stack_back[0]]:
            if token_list[pointer].ind == stack_back[0] or symbol[stack_back[0]] == "e":
                stack.pop()
                if symbol[stack_back[0]] != "e":
                    pointer += 1
                if symbol[stack_back[0]] == "$" and pointer == len(stack):
                    print("\n______________\nDone Parsing!\n______________\n")
                    break
            else:
                print("Hamta Error:")
                if symbol[stack_back[0]] == "$":
                    print(f"In parsing, a compilation eror accoured. An extra token \"{symbol[token_list[pointer].ind]}\" is found in line {token_list[pointer].line}")
                    print(f"Something is wrong about token numebr {token_list[pointer].rank}")
                else:
                    print(f"In parsing, a compilation eror accoured. Token: [{symbol[stack_back[0]]}] is missing in line {token_list[pointer].line} before \"{token_list[pointer].ind}\"")
                    print(f"Something is wrong about token numebr {token_list[pointer].rank}")
                break
        else:
            if len(pars_table[stack_back[0]][token_list[pointer]]) > 0:
                # reason behind [0]: this is a ll(1) parser but i wrote it more generalized
                prod = pars_table[stack_back[0]][token_list[pointer]][0]
                # [::-1] reverses the string but its like called by value and the list doesn't change
                lst = productions[stack_back[0]][prod][::-1]
                stack.pop()
                for e in lst:
                    stack.append([e, cnt])
                    pars_tree[stack_back[1]].adj.append([e, cnt])
                    pars_tree.append(ParsNode(e))
                    cnt += 1
                pars_tree[stack_back[1]].adj.reverse()
            else:
                print("Hamta Error:")
                print(f"In parsing, a compilation eror accoured. One of the token(s): {childs[stack_back[0]]} are missing in line {token_list[pointer].line}.")
                print("- $ is a special token which means the end of the file")
                print(f"Something is wrong about token numebr {token_list[pointer].rank}")
                break
    if __name__ == "__main__":
        print("Adjancy list of pars tree:")
        for i in range(len(pars_tree)):
            if len(pars_tree[i].adj) > 0:
                print(f"{symbol[pars_tree[i].ind]}: ( ", end="")
                for e in pars_tree[i].adj:
                    print(symbol[e[0]], end = " ")
                print(")\n")
    return

def __main__():
    global token_list, token_table, terminal, n
    print("Loading data ...")
    enum_symbols()
    prepare_productions()
    prepare_p_table()
    print("-----------------\nTokenizing the sampel ...")
    token_list = tokenize()
    print("-----------------\nBuilding the token table ...")
    build_token_table()
    print("-----------------\nBuilding the pars tree ...")
    build_pars_tree()
    print("-----------------\nDone!")
    return

if __name__ == "__main__":
    __main__()