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

token_list = []
token_table = []

def create_token_table(t_list):
    global token_list, token_table
    t_list
    # last part
    return