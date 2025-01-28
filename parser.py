from lexical_analyzer import *

from build_token_table import *

class ParsNode:
    def __init__(self, ind, par):
        self.ind = ind
        self.rank = -1
        self.par = par
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
symbol_dict = {}

#O(n) فقط ورودی میخونه
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

# O(G * n) فقط می خونیم میریم جلو و خب هر پروداکشن می تونه ان تا نماد داشته باشه جی هم منظورم تعداد پروداکشن هاست
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

# O(te * nt) حاصل ضرب نماد های ترمینال و نماد های غیر ترمینال
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

# O(توکن ها کد) چون هیچ پروداکشنی نداریم که از یک سمبل غیر ترمینال به یدونه غیر ترمینال دیگه باشه پس تعداد همه راس ها از اردر تعداد توکن های کده و کمتر از دو برابر تعداد توکن های کده
def build_pars_tree():
    global pars_tree, candidates, n, token_list
    sp_char = {'tokentype': 'Special token', 'token': '$', 'value': '$', 'line': 'inf', 'rank': 'inf'}
    token_list.append(sp_char)
    pointer = 0
    cnt = 0
    pars_tree = [ParsNode(symbol_dict["$"], -1), ParsNode(symbol_dict["Start"], -1)]
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
                    if symbol[stack_back[0]] != "$":
                        pars_tree[stack_back[1]].rank = pointer
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
                    pars_tree[stack_back[1]].adj.append(cnt)
                    pars_tree.append(ParsNode(e, stack_back[1]))
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
            print(f"[index: {i}, token: {symbol[pars_tree[i].ind]}]: ( ", end="")
            for e in pars_tree[i].adj:
                if pars_tree[e].rank == -1:
                    print(f"[index: {e}, token: {symbol[pars_tree[e].ind]}]", end = " ")
                else:
                    value = token_list[pars_tree[e].rank]["value"]
                    print(f"[index: {e}, token: {symbol[pars_tree[e].ind]}, value: {value}]", end = " ")
            print(")\n")
    print("----------------------------")
    return

#  حاصل جمع همه تابع هایی که توش کال شده که میشه برابر تعداد توکن های کد به علاوه تعداد پروداکشن ها در نماد ها به علاوه ضرب نماد های ترمینال در غیر ترمینال
def pars(dir="./sampels/code.cpp", grammer="./grammers/cppiler"):
    global token_list
    print("Loading data ...")
    enum_symbols(grammer)
    prepare_productions(grammer)
    prepare_p_table(grammer)
    print("-----------------\nTokenizing the sampel ...")
    token_list = tokenize(dir)
    print("-----------------\nBuilding the token table ...")
    build_token_table(token_list)
    print("-----------------\nBuilding the pars tree ...")
    build_pars_tree()
    print("-----------------\nDone Parsing!")
    return

target_stack = [[-1, -1]]
id_stack = []

depth = 0

# simpel dfs in tree and a stack so its in O(pars tree nodes) = O(tokens in the code)
def search(u, target, target_ind, in_id):
    global pars_tree, target_stack, id_stack, token_list, depth
    
    if symbol[pars_tree[u].ind] == "{":
        depth += 1
    
    if not in_id and symbol[pars_tree[u].ind] == "Id":
        in_id = True
        id_stack = ['$']
    
    if in_id and pars_tree[u].rank != -1:
        token = token_list[pars_tree[u].rank]
        back = id_stack[len(id_stack) - 1]
        if back == ',' or back == 'int' or back == "float":
            if token["value"] == target["value"]:
                target_stack.append([depth, token["line"]])
        id_stack.append(token["value"])
    
    for v in pars_tree[u].adj:
        if search(v, target, target_ind, in_id):
            return True
    
    if symbol[pars_tree[u].ind] == "Id":
        id_stack = ['$']
    
    if symbol[pars_tree[u].ind] == "}":
        while True:
            back = target_stack[len(target_stack) - 1]
            if back[0] == depth:
                target_stack.pop()
            else:
                break
        depth -= 1
    
    return u == target_ind

def print_declartion(index):
    global pars_tree, target_stack, token_list

    if index not in range(len(pars_tree)):
        print("It's not an identifier, try again ...")
        return

    if not symbol[pars_tree[index].ind].startswith("identifier"):
        print("It's not an identifier, try again ...")
        return

    search(1, token_list[pars_tree[index].rank], index, False)

    if len(target_stack) > 0:
        back = target_stack[len(target_stack) - 1]
        print(f"It was declared in the line number {back[1]}:\n --> ", end = "")
        for token in token_list:
            if token["line"] == back[1]:
                print(token["value"], end = " ")
        print("\n____________")
    
    else:
        print("It wasn't declared in this scope\n____________")
    
    return

if __name__ == "__main__":
    pars()