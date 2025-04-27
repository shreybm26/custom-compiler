from utils import get_token_stream
from tac_generator import TACGenerator

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current = tokens[0] if tokens else None
        self.symbol_table = set()
        self.tac = TACGenerator()
        self.temp_counter = 0

    def advance(self):
        self.pos += 1
        self.current = self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def match(self, token_type):
        if self.current and self.current[0] == token_type:
            val = self.current[1]
            self.advance()
            return val
        else:
            raise SyntaxError(f"Expected {token_type}, got {self.current}")

    def new_temp(self):
        name = f"t{self.temp_counter}"
        self.temp_counter += 1
        return name

    def parse_program(self):
        while self.current:
            self.parse_stmt()

    def parse_stmt(self):
        if self.current[0] in ("INT_TYPE", "STRING_TYPE"):
            self.advance()
            var_name = self.match("IDENTIFIER")
            self.match("SEMICOLON")
            self.symbol_table.add(var_name)

        elif self.current[0] == "WHILE":
            self.advance()
            start_label = self.tac.new_label()
            end_label = self.tac.new_label()
            self.tac.emit_label(start_label)
            cond_temp = self.parse_expr()
            self.match("LBRACE")
            self.tac.emit(f"if_false {cond_temp} goto {end_label}")
            while self.current and self.current[0] != "RBRACE":
                self.parse_stmt()
            self.match("RBRACE")
            self.tac.emit(f"goto {start_label}")
            self.tac.emit_label(end_label)

        elif self.current[0] == "IF":
            self.advance()
            cond_temp = self.parse_expr()
            self.match("LBRACE")
            label_else = self.tac.new_label()
            label_end = self.tac.new_label()
            self.tac.emit(f"if_false {cond_temp} goto {label_else}")
            while self.current and self.current[0] != "RBRACE":
                self.parse_stmt()
            self.match("RBRACE")
            self.tac.emit(f"goto {label_end}")
            self.tac.emit_label(label_else)
            if self.current and self.current[0] == "ELSE":
                self.advance()
                self.match("LBRACE")
                while self.current and self.current[0] != "RBRACE":
                    self.parse_stmt()
                self.match("RBRACE")
            self.tac.emit_label(label_end)

        elif self.current[0] == "IDENTIFIER":
            var_name = self.match("IDENTIFIER")
            self.match("ASSIGN")
            val = self.parse_expr()
            self.match("SEMICOLON")
            if var_name not in self.symbol_table:
                raise Exception(f"Undeclared variable: {var_name}")
            self.tac.emit(f"{var_name} = {val}")

        elif self.current[0] == "WRITE":
            self.advance()
            if self.current[0] == "IDENTIFIER":
                val = self.match("IDENTIFIER")
                if val not in self.symbol_table:
                    raise Exception(f"Undeclared variable: {val}")
            elif self.current[0] in ("INTEGER_LITERAL", "STRING_LITERAL"):
                val = self.match(self.current[0])
            else:
                raise SyntaxError(f"Invalid argument to write: {self.current}")
            self.match("SEMICOLON")
            self.tac.emit(f"print {val}")

        else:
            raise SyntaxError(f"Unknown statement start: {self.current}")

    def parse_expr(self):
        return self.parse_or_expr()

    def parse_or_expr(self):
        left = self.parse_and_expr()
        while self.current and self.current[0] == "OR":
            self.advance()
            right = self.parse_and_expr()
            temp = self.new_temp()
            self.tac.emit(f"{temp} = {left} OR {right}")
            left = temp
        return left

    def parse_and_expr(self):
        left = self.parse_rel_expr()
        while self.current and self.current[0] == "AND":
            self.advance()
            right = self.parse_rel_expr()
            temp = self.new_temp()
            self.tac.emit(f"{temp} = {left} AND {right}")
            left = temp
        return left

    def parse_rel_expr(self):
        left = self.parse_term()
        if self.current and self.current[0] in ("LT", "LE", "GT", "GE", "EQ", "NE"):
            op = self.current[0]
            self.advance()
            right = self.parse_term()
            temp = self.new_temp()
            self.tac.emit(f"{temp} = {left} {op} {right}")
            return temp
        return left

    def parse_term(self):
        if self.current[0] == "NOT":
            self.advance()
            operand = self.parse_term()
            temp = self.new_temp()
            self.tac.emit(f"{temp} = NOT {operand}")
            return temp
        elif self.current[0] in ("IDENTIFIER", "INTEGER_LITERAL", "STRING_LITERAL"):
            return self.match(self.current[0])
        else:
            raise SyntaxError("Invalid expression")


if __name__ == "__main__":
    tokens = get_token_stream("token_stream.txt")
    parser = Parser(tokens)
    parser.parse_program()
    print("Parsing successful ✅\n")
    print("Generated TAC:")
    for line in parser.tac.code:
        print(line)
