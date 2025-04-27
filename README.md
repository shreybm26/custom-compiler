
# Custom Programming Language Compiler

A fully functional compiler built for a custom imperative programming language, supporting lexical units, indentifiers, integers, strings, major types of operators and control structures.
Developed using **Python** and **Flex** for lexical analysis.

## Features

- **Lexical Analysis**  
  Tokenizes source code into identifiers, reserved words, numbers, strings, and delimiters using Flex.

- **Syntax Analysis (Parsing)**  
  Constructs parse trees and detects syntax errors using Bison based on a formally defined grammar.

- **Semantic Analysis**  
  Ensures type consistency, validates identifiers, and detects semantic errors like undeclared variables or type mismatches.

- **Intermediate Code Generation**  
  Translates source programs into optimized Three-Address Code (TAC) with constant folding and dead code elimination.

- **Code Generation**  
  Converts intermediate code to assembly/virtual machine code, applying register allocation and memory management optimizations.

## Language Specification

- **Data Types**: Integer, String
- **Operators**: Arithmetic (+, -, *, /), Relational (<, <=, >, >=, =), Logical (and, or, not)
- **Control Structures**:  
  - Conditional Statements (`if-else`)  
  - Loops (`while`)  

## How to Build and Run

1. **Install Dependencies**
   ```bash
   sudo apt-get install flex bison python3
   ```

2. **Generate the Lexer**
   ```bash
   flex lexer.l
   gcc lex.yy.c parser.tab.c -o compiler -lfl
   ```

3. **Run the Compiler**
   ```bash
   ./compiler < input_program.txt
   ```

4. **(Optional) Intermediate and Final Code Generation**
   - Run Python scripts for IR and code generation if separated:
     ```bash
     python3 main.py input_program.txt
     ```

## Sample Input (Language Example)

```c
int a;
int b;
a = 5;
b = 10;
if a < b and b > 5 {
    write "a is smaller and b is big";
}

```
