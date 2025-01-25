fsm_graph = {
    "start": {
        "num1": lambda c: c.isdigit(),
        "str1": lambda c: c == '"',
        "id1": lambda c: c.isalpha() or c == "_",
        "sym1": lambda c: c in "{()},[];+-*/%",
        "sym3": lambda c: c in "<>!="
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
    "if", "else", "while", "return", "break", "continue", "int", "float",
    "#include", "using", "namespace", "iostream", "std", "main"
}

def check_reserved_word(word):
    return word in reserved_words

def run_fsm(text):
    global fsm_graph, accept_states, start_state
    current_state = start_state
    current_word = ""
    tokens = []
    in_string = skip_next = False
    for i, char in enumerate(text):
        if skip_next:
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
        if not in_string and char in "{()},[];+-*/":
            if i + 1 < len(text) and char in "<>=+-" and text[i + 1] in "<>=+-" :
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
        if current_state in fsm_graph:
            for next_state, condition in fsm_graph[current_state].items():
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
                for next_state, condition in fsm_graph[start_state].items():
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

def tokenize(dir = './sampels/code.cpp'):    
    all_tokens = []
    cpp_code = open(dir, 'r').read().replace("\n", " $ ")
    cpp_code = cpp_code.split()
    cpp_code.append("$")
    if __name__ == "__main__":
        print(cpp_code)
    all_tokens = run_fsm(cpp_code)
    return all_tokens

# All of functions complexity = O(n), n is lenght of the string that they get as argumnet
def __main__():
    tokens = tokenize()
    for token in tokens:
        print(token, flush = True)

if __name__ == "__main__":
    __main__()