# -*- coding: utf-8 -*-
from .bytecode import Bytecode
from .ast_nodes import (
    Program, Atama, Eger, Iken, Dongu, Islem, Dondur, Getir,
    IkiliIslem, TekliIslem, Degisken, Deger, Cagir, Nitelik,
    Endeks, Liste, Sozluk, Ifade, DurNode, DevamEtNode, Sinif, Dene
)
from .runtime_types import wrap_value, OzNull

class BytecodeCompiler:
    def __init__(self):
        self.instructions = []
        self.constants = []
        self.loops = []

    def add_const(self, val):
        self.constants.append(val)
        return len(self.constants) - 1

    def emit(self, opcode, operand=None):
        self.instructions.append((opcode, operand))
        return len(self.instructions) - 1

    def patch(self, ip, target):
        self.instructions[ip] = (self.instructions[ip][0], target)

    def compile_program(self, ast_root):
        bytecode = Bytecode()
        self.compile(ast_root)
        bytecode.instructions = self.instructions
        bytecode.constants = self.constants
        return bytecode

    def compile(self, node):
        if node is None:
            return

        cls = node.__class__
        
        if cls is Program:
            for stmt in node.body:
                self.compile(stmt)

        elif cls is Ifade:
            self.compile(node.expr)
            self.emit('POP')

        elif cls is Deger:
            wrapped = wrap_value(node.value)
            idx = self.add_const(wrapped)
            self.emit('LOAD_CONST', idx)

        elif cls is Degisken:
            self.emit('LOAD_VAR', node.name)

        elif cls is Atama:
            self.compile(node.value)
            target = node.target
            tcls = target.__class__
            if tcls is Degisken:
                self.emit('STORE_VAR', (target.name, node.modifier))
            elif tcls is Endeks:
                self.compile(target.value)
                self.compile(target.index)
                self.emit('STORE_INDEX')
            elif tcls is Nitelik:
                self.compile(target.value)
                self.emit('STORE_ATTR', target.attr)
            else:
                raise SyntaxError("Geçersiz atama hedefi.")

        elif cls is Liste:
            for elt in node.elts:
                self.compile(elt)
            self.emit('MAKE_LIST', len(node.elts))

        elif cls is Sozluk:
            for k, v in zip(node.keys, node.values):
                self.compile(k)
                self.compile(v)
            self.emit('MAKE_MAP', len(node.keys))

        elif cls is Endeks:
            self.compile(node.value)
            self.compile(node.index)
            self.emit('LOAD_INDEX')

        elif cls is Nitelik:
            self.compile(node.value)
            self.emit('LOAD_ATTR', node.attr)

        elif cls is IkiliIslem:
            op = node.op
            if op in ('veya', 'or'):
                self.compile(node.left)
                self.emit('DUP')
                jump_ip = self.emit('JUMP_IF_TRUE', 0)
                self.emit('POP')
                self.compile(node.right)
                self.patch(jump_ip, len(self.instructions))
            elif op in ('ve', 'and'):
                self.compile(node.left)
                self.emit('DUP')
                jump_ip = self.emit('JUMP_IF_FALSE', 0)
                self.emit('POP')
                self.compile(node.right)
                self.patch(jump_ip, len(self.instructions))
            else:
                self.compile(node.left)
                self.compile(node.right)
                self.emit('BINARY_OP', op)

        elif cls is TekliIslem:
            self.compile(node.operand)
            self.emit('UNARY_OP', node.op)

        elif cls is Cagir:
            for arg in node.args:
                self.compile(arg)
            self.compile(node.func)
            self.emit('CALL', len(node.args))

        elif cls is Eger:
            self.compile(node.test)
            jump_false = self.emit('JUMP_IF_FALSE', 0)
            for stmt in node.body:
                self.compile(stmt)
            if node.orelse:
                jump_end = self.emit('JUMP', 0)
                self.patch(jump_false, len(self.instructions))
                for stmt in node.orelse:
                    self.compile(stmt)
                self.patch(jump_end, len(self.instructions))
            else:
                self.patch(jump_false, len(self.instructions))

        elif cls is Iken:
            start_ip = len(self.instructions)
            self.compile(node.test)
            jump_false = self.emit('JUMP_IF_FALSE', 0)
            
            loop_ctx = {'break_jumps': [], 'continue_jumps': [], 'start_ip': start_ip}
            self.loops.append(loop_ctx)
            
            for stmt in node.body:
                self.compile(stmt)
                
            self.emit('JUMP', start_ip)
            end_ip = len(self.instructions)
            self.patch(jump_false, end_ip)
            
            for j in loop_ctx['break_jumps']:
                self.patch(j, end_ip)
            for j in loop_ctx['continue_jumps']:
                self.patch(j, start_ip)
                
            self.loops.pop()

        elif cls is Dongu:
            self.compile(node.iter_expr)
            self.emit('GET_ITER')
            start_ip = len(self.instructions)
            jump_end = self.emit('FOR_ITER', 0)
            
            self.emit('STORE_VAR', (node.target.name, None))
            
            loop_ctx = {'break_jumps': [], 'continue_jumps': [], 'start_ip': start_ip, 'is_for': True}
            self.loops.append(loop_ctx)
            
            for stmt in node.body:
                self.compile(stmt)
                
            self.emit('JUMP', start_ip)
            end_ip = len(self.instructions)
            self.patch(jump_end, end_ip)
            
            for j in loop_ctx['break_jumps']:
                self.patch(j, end_ip)
            for j in loop_ctx['continue_jumps']:
                self.patch(j, start_ip)
                
            self.loops.pop()
            self.emit('POP_ITER')

        elif cls is DurNode:
            if not self.loops:
                raise SyntaxError("'dur' döngü dışında kullanılamaz.")
            loop_ctx = self.loops[-1]
            j = self.emit('JUMP', 0)
            loop_ctx['break_jumps'].append(j)

        elif cls is DevamEtNode:
            if not self.loops:
                raise SyntaxError("'devam_et' döngü dışında kullanılamaz.")
            loop_ctx = self.loops[-1]
            j = self.emit('JUMP', 0)
            loop_ctx['continue_jumps'].append(j)

        elif cls is Islem:
            fn_compiler = BytecodeCompiler()
            fn_bytecode = fn_compiler.compile_function_body(node)
            idx = self.add_const(fn_bytecode)
            self.emit('MAKE_FUNCTION', idx)
            self.emit('STORE_VAR', (node.name, None))

        elif cls is Sinif:
            class_compiler = BytecodeCompiler()
            class_bytecode = class_compiler.compile_class_body(node)
            idx = self.add_const(class_bytecode)
            self.emit('MAKE_CLASS', (node.name, idx))
            self.emit('STORE_VAR', (node.name, None))

        elif cls is Dene:
            setup_ip = self.emit('SETUP_EXCEPT', 0)
            for stmt in node.body:
                self.compile(stmt)
            self.emit('POP_EXCEPT')
            jump_end = self.emit('JUMP', 0)
            
            self.patch(setup_ip, len(self.instructions))
            
            for idx, (err_type, err_var, handler_body) in enumerate(node.handlers):
                self.emit('CHECK_EXCEPTION_TYPE', err_type)
                jmp_next = self.emit('JUMP_IF_FALSE', 0)
                
                if err_var:
                    self.emit('STORE_VAR', (err_var, None))
                else:
                    self.emit('POP')
                
                for stmt in handler_body:
                    self.compile(stmt)
                
                self.emit('CLEAR_EXCEPTION')
                self.emit('JUMP', jump_end)
                
                self.patch(jmp_next, len(self.instructions))
                
            self.emit('RERAISE_EXCEPTION')
            self.patch(jump_end, len(self.instructions))

        elif cls is Dondur:
            if node.value:
                self.compile(node.value)
            else:
                self.emit('LOAD_CONST', self.add_const(OzNull()))
            self.emit('RETURN')

        elif cls is Getir:
            self.emit('IMPORT_PACKAGE', node.name)

    def compile_function_body(self, fn_node):
        bytecode = Bytecode(name=fn_node.name, arg_names=fn_node.args)
        for stmt in fn_node.body:
            self.compile(stmt)
        self.emit('LOAD_CONST', self.add_const(OzNull()))
        self.emit('RETURN')
        bytecode.instructions = self.instructions
        bytecode.constants = self.constants
        return bytecode

    def compile_class_body(self, class_node):
        bytecode = Bytecode(name=class_node.name)
        for stmt in class_node.body:
            self.compile(stmt)
        self.emit('RETURN_CLASS_NAMESPACE')
        bytecode.instructions = self.instructions
        bytecode.constants = self.constants
        return bytecode
