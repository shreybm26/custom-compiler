class TACGenerator:
    def __init__(self):
        self.code = []
        self.temp_counter = 0
        self.label_counter = 0

    def emit(self, line):
        self.code.append(line)

    def new_temp(self):
        temp = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp

    def new_label(self):
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label

    def emit_label(self, label):
        self.code.append(f"{label}:")
