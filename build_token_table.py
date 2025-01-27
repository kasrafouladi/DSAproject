from lexical_analyzer import *
import hashlib

def build_token_table(token_list):
    
    partition_by_type = {
        "string": [],
        "string": [],
        "number": [],
        "symbol": [],
        "identifier": [],
        "reservedword": []
    }
    
    token_table = []

    for token in token_list:
        partition_by_type[token['tokentype']].append(token)

    for tokentype, tokens in partition_by_type.items():
        hashed_tokens = []
        for token in tokens:
            token_string = str(token)
            hash_object = hashlib.sha256(token_string.encode())
            hashed_token = hash_object.hexdigest()
            hashed_tokens.append((token, hashed_token)) # ذخیره توکن اصلی همراه با هش
        
        sorted_tokens = sorted(
            hashed_tokens,
            key = lambda token: token[1]
        )
        
        token_table.append([tokentype, sorted_tokens])

        print(f"___________\n{tokentype}:\n")
        
        # نمایش هش‌هاو توکن ها

        for token, hashed in sorted_tokens:
            print(f"{token}\n{hashed}\n")

    return token_table

