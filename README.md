Basic Compiler Design Project
This project is a comprehensive implementation of the fundamental components of a basic compiler. The main goal is to design and build various modules, including a lexical analyzer, a syntax parser, token and parse tables, and additional features such as error handling and search functionality.

📖 Overview
A compiler is a program that translates high-level programming code into low-level machine or assembly code. This project focuses on creating a compiler for a simplified programming language inspired by C++. By dividing the project into multiple phases, we aim to provide a step-by-step understanding of the process involved in building a compiler.

The project involves:

Lexical Analysis: Tokenizing the input source code.
Syntax Parsing: Using context-free grammars (CFG) to validate and build the syntactic structure.
Table Construction: Creating token and parse tables for efficient processing.
Error Handling: Identifying and reporting syntax errors.
Parse Tree Generation: Building a tree that represents the hierarchical structure of the code.

📌 Key Features
Tokenizes input source code using lexical analysis.
Constructs a sorted token table with hashed values.
Generates a parse tree based on a provided CFG.
Includes error handling and debugging tools for syntax issues.
Allows searching for identifiers in the parse tree.