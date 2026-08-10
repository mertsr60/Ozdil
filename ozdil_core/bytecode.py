# -*- coding: utf-8 -*-

class Bytecode:
    def __init__(self, name="<main>", arg_names=None):
        self.name = name
        self.arg_names = arg_names or []
        self.instructions = []  # List of tuples: (opcode, operand)
        self.constants = []     # List of constant values (OzValue objects)
        
    def add_instruction(self, opcode, operand=None):
        self.instructions.append((opcode, operand))
        return len(self.instructions) - 1
        
    def add_constant(self, value):
        self.constants.append(value)
        return len(self.constants) - 1

    def __repr__(self):
        lines = [f"Bytecode for {self.name}:"]
        for i, (opcode, operand) in enumerate(self.instructions):
            lines.append(f"  {i:04d}: {opcode:<20} {repr(operand) if operand is not None else ''}")
        return "\n".join(lines)
