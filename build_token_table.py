from lexical_analyzer import *
import hashlib

# O(token * lg(token)) چون روشون ایتریت می کنیم و سورت می کنیم کلا اردر هش رو هم میشه 1 در نظر گرفت

def build_token_table(token_list):
    
    partition_by_type = {
        "string": [],
        "number": [],
        "symbol": [],
        "identifier": [],
        "reservedword": []
    }
    
    token_table = []

    for token in token_list:
        partition_by_type[token['tokentype']].append(token)

    print("Token Table:")

    for tokentype, tokens in partition_by_type.items():
        hashed_tokens = []
        for token in tokens:
            token_string = str(token)
            hash_object = hashlib.sha256(token_string.encode())
            hashed_token = hash_object.hexdigest()
            hashed_tokens.append((token, hashed_token)) 
            
        sorted_tokens = sorted(
            hashed_tokens,
            key = lambda token: token[0]["value"]
        )
        
        token_table.append([tokentype, sorted_tokens])

        print(f"___________\n{tokentype}:\n")
        
        for token, hashed in sorted_tokens:
            print(f"{token}, hash = {hashed}")

    return token_table
