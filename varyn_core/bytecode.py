# -*- coding: utf-8 -*-

class Bytecode:
    def __init__(self, name="", arg_names=None):
        self.name = name
        self.arg_names = arg_names if arg_names is not None else []
        self.instructions = []  # list of (opcode, operand)
        self.constants = []     # list of constants
        
    def __repr__(self):
        return f"Bytecode(name={repr(self.name)}, arg_names={self.arg_names}, insts={len(self.instructions)}, consts={len(self.constants)})"
