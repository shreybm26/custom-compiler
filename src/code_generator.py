# code_generator.py

def generate_code(tac_lines):
    vm_code = []

    for line in tac_lines:
        line = line.strip()

        # Case 0: Label (e.g., L1:)
        if line.endswith(":"):
            vm_code.append(line)
            continue

        # Case 1: if_false x GT y goto L1
        if line.startswith("if_false"):
            parts = line.split()
            if len(parts) == 6:
                _, left, op, right, _, label = parts
                vm_code.append(f"LOAD {left}")
                vm_code.append(f"PUSH {right}")
                if op == "GT": vm_code.append("GT")
                elif op == "LT": vm_code.append("LT")
                elif op == "EQ": vm_code.append("EQ")
                elif op == "GE": vm_code.append("GE")
                elif op == "LE": vm_code.append("LE")
                elif op == "NE": vm_code.append("NE")
                vm_code.append(f"JZ {label}")
            elif len(parts) == 4:
                _, condition_temp, _, label = parts
                vm_code.append(f"LOAD {condition_temp}")
                vm_code.append(f"JZ {label}")
            else:
                raise ValueError(f"Invalid if_false format: {line}")
            continue


            vm_code.append(f"LOAD {left}")
            vm_code.append(f"PUSH {right}")

            if op == "GT": vm_code.append("GT")
            elif op == "LT": vm_code.append("LT")
            elif op == "EQ": vm_code.append("EQ")
            elif op == "GE": vm_code.append("GE")
            elif op == "LE": vm_code.append("LE")
            elif op == "NE": vm_code.append("NE")

            # if_false → jump if condition is false (i.e. result is 0)
            vm_code.append(f"JZ {label}")
            continue

        # Case 2: Goto (unconditional jump)
        if line.startswith("goto"):
            _, label = line.split()
            vm_code.append(f"JMP {label}")
            continue

        # Case 3: Assignment (x = ...)
        if " = " in line:
            lhs, rhs = line.split(" = ")
            rhs = rhs.strip()

            # Case: Unary NOT
            if rhs.startswith("NOT "):
                operand = rhs[4:]
                vm_code.append(f"LOAD {operand}")
                vm_code.append("NOT")
                vm_code.append(f"STORE {lhs}")
                continue

            # 3a. String literal
            if rhs.startswith('"') and rhs.endswith('"'):
                vm_code.append(f'PUSH {rhs}')
                vm_code.append(f'STORE {lhs}')

            # 3b. Simple assignment (x = y or x = 5)
            elif len(rhs.split()) == 1:
                value = rhs
                if value.isdigit():
                    vm_code.append(f'PUSH {value}')
                else:
                    vm_code.append(f'LOAD {value}')
                vm_code.append(f'STORE {lhs}')

            # 3c. Expression (x = a + b)
            elif len(rhs.split()) == 3:
                left, op, right = rhs.split()
                vm_code.append(f"PUSH {left}" if left.isdigit() else f"LOAD {left}")
                vm_code.append(f"PUSH {right}" if right.isdigit() else f"LOAD {right}")
                op_map = {
                    "+": "ADD", "PLUS": "ADD",
                    "-": "SUB", "MINUS": "SUB",
                    "*": "MUL", "MUL": "MUL",
                    "/": "DIV", "DIV": "DIV",
                    "<": "LT", "LT": "LT",
                    "<=": "LE", "LE": "LE",
                    ">": "GT", "GT": "GT",
                    ">=": "GE", "GE": "GE",
                    "==": "EQ", "EQ": "EQ",
                    "!=": "NE", "NE": "NE",
                    "AND": "AND", "and": "AND",
                    "OR": "OR", "or": "OR",
                }
                if op in op_map:
                    vm_code.append(op_map[op])

            continue

        # Case 4: print x, or print 0, or print "hello"
        if line.startswith("print "):
            val = line.split(" ", 1)[1]

            if val.isdigit():
                vm_code.append(f'PUSH {val}')
            elif val.startswith('"') and val.endswith('"'):
                vm_code.append(f'PUSH {val}')
            else:
                vm_code.append(f'LOAD {val}')
            
            vm_code.append("PRINT")
            continue

        # (Optional) Catch-all for debugging:
        # vm_code.append(f"# Unhandled line: {line}")

    return vm_code


if __name__ == "__main__":
    from parser import Parser
    from utils import get_token_stream

    tokens = get_token_stream("token_stream.txt")
    parser = Parser(tokens)
    parser.parse_program()

    print("Parsing successful ✅\n")
    print("Generated TAC:")
    for tac in parser.tac.code:
        print(tac)

    print("\n🔧 Stack-Based VM Code:")
    vm_code = generate_code(parser.tac.code)
    for line in vm_code:
        print(line)
