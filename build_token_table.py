from lexical_analyzer import *
import hashlib


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
    
    hashed_tokens = []
    for token in sorted_tokens:
        token_string = f"{token['tokentype']}:{token['value']}"
        hash_object = hashlib.sha256(token_string.encode())
        hashed_token = hash_object.hexdigest()
        hashed_tokens.append((token, hashed_token))  # ذخیره توکن اصلی همراه با هش
    
    # نمایش هش‌ها
    for token, hashed in hashed_tokens:
        print(f"{hashed}\n")

    
    #for token in sorted_tokens:
    #    print(token)

