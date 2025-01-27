from lexical_analyzer import *

def build_token_table():
    global token_list, token_table
    # last part
    return []


#print("--------------------------------------------------------------")

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
    
    for token in sorted_tokens:
        print(token)

