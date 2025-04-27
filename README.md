# Custom Programming Language Compiler

A fully functional compiler built for a custom imperative programming language, supporting lexical units, identifiers, integers, strings, major types of operators and control structures.
Developed using **Python** and **Flex** for lexical analysis.

## Features

- **Lexical Analysis**  
  Tokenizes source code into identifiers, reserved words, numbers, strings, and delimiters using Flex.

- **Syntax Analysis (Parsing)**  
  Constructs parse trees and detects syntax errors using a custom Python-based parser.

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

## Project Structure

```
src/
├── lexer.l           # Flex lexer specification
├── lex.yy.c          # Generated lexer code
├── lexer             # Compiled lexer executable
├── parser.py         # Python-based parser
├── tac_generator.py  # Three-Address Code generator
├── code_generator.py # Final code generator
├── utils.py          # Utility functions
├── tokens.h          # Token definitions
└── test.myLang       # Test program file
```

## How to Build and Run

1. **Install Dependencies**
   ```bash
   # For Windows (using MinGW or similar):
   # Install Flex and GCC
   
   # For Linux:
   sudo apt-get install flex gcc
   ```

2. **Generate the Lexer**
   ```bash
   cd src
   flex lexer.l
   gcc lex.yy.c -o lexer -lfl
   ```

3. **Run the Compiler**
   ```bash
   # First run the lexer
   ./lexer
   
   # Then run the Python-based compiler
   python parser.py
   ```

## Sample Input (Language Example)

Create a file named `test.myLang` in the `src` directory with the following content:

```c
int a;
int b;
a = 5;
b = 10;
if a < b and b > 5 {
    write "a is smaller and b is big";
}
```

## Development

The compiler pipeline works as follows:
1. The Flex lexer (`lexer.l`) tokenizes the input program
2. The Python parser (`parser.py`) processes the token stream
3. The TAC generator (`tac_generator.py`) creates intermediate code
4. The code generator (`code_generator.py`) produces the final output

## Testing

To test the compiler:
1. Write your test program in `test.myLang`
2. Run the lexer to generate tokens
3. Run the Python compiler to process the tokens and generate output

The compiler will output any errors or warnings during the compilation process. 
