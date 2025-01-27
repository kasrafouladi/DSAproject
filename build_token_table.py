from lexical_analyzer import *

class Token:
    def __init__(self, cat, val, id, rank, line, ind):
        self.cat = cat
        self.val = val
        self.id = id
        self.rank = rank
        self.line = line
        self.ind = ind
        return

token_list = []
token_table = []

def build_token_table(tokens):
    global token_list, token_table
    # last part
    return []


print("--------------------------------------------------------------")

def sort_tokens(modified_tokens):
    type_order = {
        "string": 0,
        "number": 1,
        "symbol": 2,
        "identifier": 3,
        "reservedword": 4
    }
    
    sorted_tokens = sorted(
        modified_tokens,
        key=lambda token: (type_order[token["tokentype"]], token["value"])
    )
    return sorted_tokens

sorted_tokens = sort_tokens(modified_tokens)

for token in sorted_tokens:
    print(token)

