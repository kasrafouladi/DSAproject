import re

reserved_words = ["int", "float", "break", "continue", "if", "while", "return", "main", "#include", "using", "namespace", "std", "cout", "cin", "endl"]

patterns = { 
    "#include": r"#include",
    "number": r"\b\d+(\.\d+)?(e(\+|\-)?\d+)?\b",
    "string": r'"[^"]*"',
    "identifier": r"[a-zA-Z_][a-zA-Z0-9_]*", 
    "symbol": r"[\+\-\*/%=!;,{}()\[\]<>]"
}

def is_white_space(c):
    if c == " " or c == "\t" or c == "\n":
        return True
    return False

def lexical_analyzer(code_lines):
    tokens = []  
    for line_number, line in enumerate(code_lines, start=1):
        index = 0
        while index < len(line):
            match = None
            for token_type, pattern in patterns.items():
                regex = re.compile(pattern)
                match = regex.match(line, index)
                if match:
                    value = match.group()
                    if token_type == "#include":
                        token_type = "reservedword"
                    if token_type == "identifier":
                        token_type = "reservedword" if value in reserved_words else "identifier"
                    tokens.append([[token_type, f"{value}"], line_number])
                    index = match.end()
                    break
            if not match:
                if is_white_space(line[index]):
                    index += 1  
                else:
                    print(f"goorba Error:\nIn tokenization, an unknown character founded in line {line_number}:\n\"{line[index]}\" (character number {index})")
                    exit()
    return tokens

def tokenize(dir="./sampels/code.cpp"):
    try:
        with open(dir, "r") as file:
            input_lines = file.readlines()  
        tokens = lexical_analyzer(input_lines)
        for token in tokens:
            print(f"{token[0]}, in line {token[1]}")
        return tokens
    except FileNotFoundError:
        print(f"~ oordak Error:\nFile not found at {dir}")
    except Exception as e:
        print(f"~ oordak Error:\nAn error occurred: {e}")
    exit()
    return []

if __name__ == "__main__":
    tokenize()

tokens = tokenize(dir="./sampels/code.cpp")

def modify_tokens(tokens):
    modified_tokens = []

    for i, token in enumerate(tokens):
        token_type = token[0][0]  
        token_value = token[0][1]  
        line_number = token[1]

        if token_type == "symbol" and token_value == "=":
            if i + 1 < len(tokens):
                next_token = tokens[i + 1][0]
                if next_token[1] == "=":  
                    token_suffix = "(1)"
                elif next_token[0] == "identifier":  
                    
                    if i + 2 < len(tokens) and tokens[i + 2][0][1] == "=":
                        token_suffix = "(1)"  
                    else:
                        token_suffix = "(0)"  
                else:
                    token_suffix = "(0)"  
            else:
                token_suffix = "(0)"  
            modified_token = {
                "tokentype": token_type,
                "token": f"={token_suffix}",
                "value": "=",
                "line": line_number
            }
        elif token_type == "reservedword" and token_value == "else":
            
            if i + 1 < len(tokens) and tokens[i + 1][0][1] == "if":
                token_suffix = "(1)"  
            else:
                token_suffix = "(0)"  
            modified_token = {
                "tokentype": token_type,
                "token": f"else{token_suffix}",
                "value": "else",
                "line": line_number
            }
        elif token_type == "identifier":
           
            if i + 1 < len(tokens) and tokens[i + 1][0][1] == "[":
                token_suffix = "(1)"  
            else:
                token_suffix = "(0)"  
            modified_token = {
                "tokentype": token_type,
                "token": f"{token_value}{token_suffix}",
                "value": token_value,
                "line": line_number
            }
        else:
        
            modified_token = {
                "tokentype": token_type,
                "token": token_value,
                "value": token_value,
                "line": line_number
            }

        
        modified_tokens.append(modified_token)

    return modified_tokens



modified_tokens = modify_tokens(tokens)
for token in modified_tokens:
    print(token)
