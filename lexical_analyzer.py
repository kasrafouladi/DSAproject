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
        if __name__ == "__main__":
            print("The code:\n_______________")
            for line in input_lines:
                print(line, end = "")
            print("_______________")
        return lexical_analyzer(input_lines)
    except FileNotFoundError:
        print(f"~ oordak Error:\nFile not found at {dir}")
    except Exception as e:
        print(f"~ oordak Error:\nAn error occurred: {e}")    
    return []

def __main__():
    token_list = tokenize()
    for token in token_list:
        print(f"{token[0]}, in line {token[1]}")

if __name__ == "__main__":
    __main__()
