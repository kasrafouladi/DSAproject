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

file_path = get_file_path()

pars(file_path)