dfa_graph = {
    "start": {
        "num1": lambda c: c.isdigit(),
        "str1": lambda c: c == '"',
        "id1": lambda c: c.isalpha() or c == "_",
        "sym1": lambda c: c in "(),|[];:+-*",
        "sym3": lambda c: c in "<>=",
    },
    "num1": {
        "num1": lambda c: c.isdigit(),
        #"num2": lambda c: not c.isalnum() and not c == "_"
    },
    "str1": {
        "str1": lambda c: True,  
        "str2": lambda c: c == '"'
    },
    "id1": {
        "id1": lambda c: c.isalnum() or c == "_",
        "check_word": lambda c: not c.isalnum() and c != "_"
    },
    "check_word": {
        "rw": lambda reserved: reserved is True,
        "id": lambda reserved: reserved is False
    },
    "sym1": {
        "sym2": lambda c: c == "="  
    },
    "sym3": {
        "sym2": lambda c: c == "="  
    }
}

accept_states = {
    "num1": "Number",
    "str2": "String",
    "id": "Identifier",
    "rw": "ReservedWord",
    "sym1": "Symbol",
    "sym2": "Symbol",
    "sym3": "Symbol"
}

start_state = "start"

reserved_words = {
    "if", "else", "while", "return", "int", "float", "char",
    "#include", "using", "namespace", "iostream", "std", "main" ,"void"
}

def check_reserved_word(word):
    return word in reserved_words

def run_dfa(dfa_graph, accept_states, start_state, text):
    current_state = start_state
    current_word = ""
    tokens = []
    in_string = False  
    
    skip_next = False

    for i, char in enumerate(text):
        
        if skip_next :
            skip_next = False
            continue
        
        
        if not in_string and char.isspace():  
            if current_word:
                if current_state == "id1":   
                    reserved = check_reserved_word(current_word)
                    next_state = "rw" if reserved else "id"
                    tokens.append((accept_states[next_state], current_word))
                elif current_state in accept_states:
                    tokens.append((accept_states[current_state], current_word))
                else:
                    tokens.append(("Unknown", current_word))
                current_word = ""
                current_state = start_state
            continue

        if not in_string and char in "(),|[];:+-*<>=":
            if i + 1 < len(text) and char in "<>=+-!" and text[i + 1] in "<>=+-" :
                if current_word: 
                    if current_state == "id1":  
                        reserved = check_reserved_word(current_word)
                        next_state = "rw" if reserved else "id"
                        tokens.append((accept_states[next_state], current_word))
                        
                    #elif current_state == "num1":
                     #   current_state = "num2"
                      #  tokens.append((accept_states[current_state], current_word))
         
                    elif current_state in accept_states:
                        tokens.append((accept_states[current_state], current_word))
                    else:
                        tokens.append(("Unknown", current_word))
                    current_word = ""
                    current_state = start_state

                tokens.append(("Symbol", char + text[i + 1]))
                current_state = start_state
                skip_next = True
                continue

            if current_word:  
                if current_state == "id1":  
                    reserved = check_reserved_word(current_word)
                    next_state = "rw" if reserved else "id"
                    tokens.append((accept_states[next_state], current_word))
                elif current_state in accept_states:
                    tokens.append((accept_states[current_state], current_word))
                else:
                    tokens.append(("Unknown", current_word))
                current_word = ""
                current_state = start_state

            tokens.append(("Symbol", char))
            continue

        transition_found = False

        if current_state in dfa_graph:
            for next_state, condition in dfa_graph[current_state].items():
                if condition(char):
                    current_state = next_state
                    current_word += char
                    transition_found = True
                    if current_state == "str1":
                        in_string = True
                    elif current_state == "str2":
                        in_string = False
                    break

        if not transition_found:
            if current_state in accept_states and current_word:
                tokens.append((accept_states[current_state], current_word))
            current_word = ""
            current_state = start_state

            if not char.isspace():
                for next_state, condition in dfa_graph[start_state].items():
                    if condition(char):
                        current_state = next_state
                        current_word = char
                        if current_state == "str1":
                            in_string = True
                        elif current_state == "str2":
                            in_string = False
                        break

    if current_word:
        if current_state == "id1":  
            reserved = check_reserved_word(current_word)
            next_state = "rw" if reserved else "id"
            tokens.append((accept_states[next_state], current_word))
        elif current_state in accept_states:
            tokens.append((accept_states[current_state], current_word))
        else:
            tokens.append(("Unknown", current_word))

    return tokens
def process_cpp_code(cpp_code):
    
    all_tokens = [] 
    lines = cpp_code.splitlines()
    for line in lines:
        line = line.strip() 
        if line:  
            tokens = run_dfa(dfa_graph, accept_states, start_state, line)
            all_tokens.extend(tokens)

    return all_tokens

import sys
cpp_code = sys.stdin.read()

tokens = process_cpp_code(cpp_code)

#for token in tokens:
#    print(token)
