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