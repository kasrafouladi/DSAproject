from parser import *

def get_file_path():
    print("Hello! Welcome to the Code Processing Program 😊")
    print("Please enter the file path of your code below.")
    print("-" * 40)  

    file_path = input("File path: ")
    
    print("-" * 40)
    print("Thank you! Your file path has been received.")
    print("Processing your file...")
    print("-" * 40)
    
    return file_path

def __main__():
    file_path = get_file_path()
    pars(dir=file_path, grammer='./grammers/cppiler')
    while True:
        response = input("Do you want to search an identifier to find it's declaretion?(yes:enter the index/no: enter -1)\n")
        if response == '-1':
            break
        try:
            print_declartion(int(response))
        except Exception as e:
            print("invalid input")
    print("byebye")
    return

if __name__ == "__main__":
    __main__()