import re

reserved_words = ["int", "float", "void", "if", "while", "return", "main", "#include", "using", "namespace", "std", "cout", "cin" , "endl"]

patterns = { 
    "#include": r"#include",
    "number": r"\b\d+(\.\d+)?\b",
    "string": r'"[^"]*"',  
    "identifier": r"[a-zA-Z_][a-zA-Z0-9_]*", 
    "symbol": r"==|!=|<=|>=|>>|<<|[+\-*/=;,{}()[\]<>]", 
}

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
                if line[index].isspace():
                    index += 1  
                else:
                    print(f"{line_number}: {line[index]}")
                    index += 1
    return tokens

def __main__():
    input_file_path = "./Samples/code.cpp"  
    try:
        with open(input_file_path, "r") as file:
            input_lines = file.readlines()  
        
        tokens = lexical_analyzer(input_lines)

        token_list = [] 
        for token in tokens:
            token_list.append(token)
        #print(token_list)
        return token_list

    except FileNotFoundError:
        print(f"Error: File not found at {input_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")



if __name__ == "__main__":
    tokens = __main__()
