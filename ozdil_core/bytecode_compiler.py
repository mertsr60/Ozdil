# -*- coding: utf-8 -*-
from .bytecode import Bytecode
from .runtime_types import wrap_value, OzNull, OzBool, OzInt, OzFloat, OzString, OzList, OzMap
from .ast_nodes import (
    Program, Atama, Eger, Iken, Dongu, Islem, Dondur, Getir,
    IkiliIslem, TekliIslem, Degisken, Deger, Cagir, Nitelik,
    Endeks, Liste, Sozluk, Ifade, DurNode, DevamEtNode, Sinif, Dene
)

class BytecodeCompiler:
    def __init__(self, filename="<string>"):
        self.filename = filename
        self.current_bytecode = Bytecode()
        self.loop_stack = []

    def compile_program(self, ast_root):
        self.visit(ast_root)
        # Ensure we return None if no explicit return
        self.emit_const(None)
        self.emit('RETURN')
        return self.current_bytecode

    def emit(self, opcode, operand=None):
        return self.current_bytecode.add_instruction(opcode, operand)

    def emit_const(self, value):
        wrapped = wrap_value(value)
        idx = self.current_bytecode.add_constant(wrapped)
        self.emit('LOAD_CONST', idx)

    def visit(self, node):
        if node is None:
            return
        
        node_class = node.__class__
        
        if node_class is Program:
            for stmt in node.body:
                self.visit(stmt)
                
        elif node_class is Ifade:
            self.visit(node.expr)
            self.emit('POP')  # Clean up expression statement result
            
        elif node_class is Deger:
            self.emit_const(node.value)
            
        elif node_class is Degisken:
            self.emit('LOAD_VAR', node.name)
            
        elif node_class is Atama:
            self.visit(node.value)
            target = node.target
            target_class = target.__class__
            if target_class is Degisken:
                self.emit('STORE_VAR', (target.name, node.modifier))
            elif target_class is Endeks:
                self.visit(target.value)
                self.visit(target.index)
                self.emit('STORE_INDEX')
            elif target_class is Nitelik:
                self.visit(target.value)
                self.emit('STORE_ATTR', target.attr)
            else:
                raise SyntaxError(f"Geçersiz atama hedefi.", (self.filename, node.lineno, 1, ""))
                
        elif node_class is Liste:
            for elt in node.elts:
                self.visit(elt)
            self.emit('MAKE_LIST', len(node.elts))
            
        elif node_class is Sozluk:
            for k, v in zip(node.keys, node.values):
                self.visit(k)
                self.visit(v)
            self.emit('MAKE_MAP', len(node.keys))
            
        elif node_class is Endeks:
            self.visit(node.value)
            self.visit(node.index)
            self.emit('LOAD_INDEX')
            
        elif node_class is Nitelik:
            self.visit(node.value)
            self.emit('LOAD_ATTR', node.attr)
            
        elif node_class is IkiliIslem:
            op = node.op
            if op == 've':
                self.visit(node.left)
                self.emit('DUP')
                jump_idx = self.emit('JUMP_IF_FALSE', None)
                self.emit('POP')
                self.visit(node.right)
                # Resolve jump
                current_ip = len(self.current_bytecode.instructions)
                self.current_bytecode.instructions[jump_idx] = ('JUMP_IF_FALSE', current_ip)
            elif op == 'veya':
                self.visit(node.left)
                self.emit('DUP')
                jump_idx = self.emit('JUMP_IF_TRUE', None)
                self.emit('POP')
                self.visit(node.right)
                # Resolve jump
                current_ip = len(self.current_bytecode.instructions)
                self.current_bytecode.instructions[jump_idx] = ('JUMP_IF_TRUE', current_ip)
            else:
                self.visit(node.left)
                self.visit(node.right)
                self.emit('BINARY_OP', op)
                
        elif node_class is TekliIslem:
            self.visit(node.operand)
            self.emit('UNARY_OP', node.op)
            
        elif node_class is Cagir:
            for arg in node.args:
                self.visit(arg)
            self.visit(node.func)
            self.emit('CALL', len(node.args))
            
        elif node_class is Eger:
            self.visit(node.test)
            else_jump_idx = self.emit('JUMP_IF_FALSE', None)
            
            for stmt in node.body:
                self.visit(stmt)
                
            end_jump_idx = self.emit('JUMP', None)
            
            else_ip = len(self.current_bytecode.instructions)
            self.current_bytecode.instructions[else_jump_idx] = ('JUMP_IF_FALSE', else_ip)
            
            if node.orelse:
                for stmt in node.orelse:
                    self.visit(stmt)
                    
            end_ip = len(self.current_bytecode.instructions)
            self.current_bytecode.instructions[end_jump_idx] = ('JUMP', end_ip)
            
        elif node_class is Iken:
            start_loop_ip = len(self.current_bytecode.instructions)
            self.visit(node.test)
            exit_jump_idx = self.emit('JUMP_IF_FALSE', None)
            
            self.loop_stack.append({
                'continue_ip': start_loop_ip,
                'breaks': []
            })
            
            for stmt in node.body:
                self.visit(stmt)
                
            self.emit('JUMP', start_loop_ip)
            
            end_loop_ip = len(self.current_bytecode.instructions)
            self.current_bytecode.instructions[exit_jump_idx] = ('JUMP_IF_FALSE', end_loop_ip)
            
            loop_ctx = self.loop_stack.pop()
            for break_idx in loop_ctx['breaks']:
                self.current_bytecode.instructions[break_idx] = ('JUMP', end_loop_ip)
                
        elif node_class is Dongu:
            # 1. Evaluate collection/iterable
            self.visit(node.iter_expr)
            self.emit('GET_ITER')
            
            start_loop_ip = len(self.current_bytecode.instructions)
            exit_jump_idx = self.emit('FOR_ITER', None)
            
            # Store item into local variable
            self.emit('STORE_VAR', node.target.name)
            
            self.loop_stack.append({
                'continue_ip': start_loop_ip,
                'breaks': []
            })
            
            for stmt in node.body:
                self.visit(stmt)
                
            self.emit('JUMP', start_loop_ip)
            
            end_loop_ip = len(self.current_bytecode.instructions)
            self.current_bytecode.instructions[exit_jump_idx] = ('FOR_ITER', end_loop_ip)
            
            loop_ctx = self.loop_stack.pop()
            for break_idx in loop_ctx['breaks']:
                self.current_bytecode.instructions[break_idx] = ('JUMP', end_loop_ip)
                
            self.emit('POP_ITER')
            
        elif node_class is DurNode:
            if not self.loop_stack:
                raise SyntaxError("Döngü dışında 'dur' (break) kullanılamaz.", (self.filename, node.lineno, 1, ""))
            break_idx = self.emit('JUMP', None)
            self.loop_stack[-1]['breaks'].append(break_idx)
            
        elif node_class is DevamEtNode:
            if not self.loop_stack:
                raise SyntaxError("Döngü dışında 'devam et' (continue) kullanılamaz.", (self.filename, node.lineno, 1, ""))
            self.emit('JUMP', self.loop_stack[-1]['continue_ip'])
            
        elif node_class is Islem:
            # Functions are compiled to separate Bytecode blocks
            parent_compiler = self.current_bytecode
            
            func_bytecode = Bytecode(name=node.name, arg_names=node.args)
            self.current_bytecode = func_bytecode
            
            # Save outer loop stack
            outer_loop_stack = self.loop_stack
            self.loop_stack = []
            
            # Compile function body
            for stmt in node.body:
                self.visit(stmt)
                
            # Default return None at function end
            self.emit_const(None)
            self.emit('RETURN')
            
            # Restore state
            self.loop_stack = outer_loop_stack
            self.current_bytecode = parent_compiler
            
            # Load compiled function bytecode as a constant
            const_idx = self.current_bytecode.add_constant(func_bytecode)
            self.emit('MAKE_FUNCTION', const_idx)
            self.emit('STORE_VAR', node.name)
            
        elif node_class is Sinif:
            # We will handle classes in bytecode!
            # Each class statement evaluates in its own block/environment
            # For simplicity, we can compile a function that returns its namespace
            parent_compiler = self.current_bytecode
            class_bytecode = Bytecode(name=f"class_{node.name}")
            self.current_bytecode = class_bytecode
            
            outer_loop_stack = self.loop_stack
            self.loop_stack = []
            
            for stmt in node.body:
                self.visit(stmt)
                
            self.emit('RETURN_CLASS_NAMESPACE')
            
            self.loop_stack = outer_loop_stack
            self.current_bytecode = parent_compiler
            
            const_idx = self.current_bytecode.add_constant(class_bytecode)
            self.emit('MAKE_CLASS', (node.name, const_idx))
            self.emit('STORE_VAR', node.name)
            
        elif node_class is Dondur:
            if node.value:
                self.visit(node.value)
            else:
                self.emit_const(None)
            self.emit('RETURN')
            
        elif node_class is Getir:
            self.emit('IMPORT_PACKAGE', node.name)
            
        elif node_class is Dene:
            # Exceptional handling compiler targets
            # We emit try push block
            # try_block_idx = emit('SETUP_EXCEPT', handler_target_ip)
            # compile try body
            # emit('POP_EXCEPT')
            # emit('JUMP', end_ip)
            # handler_target_ip:
            # compile except handlers
            # end_ip:
            
            # For backward compatibility and simplicity in custom VM:
            # Let's support basic SETUP_EXCEPT and POP_EXCEPT!
            handler_jump_idx = self.emit('SETUP_EXCEPT', None)
            
            for stmt in node.body:
                self.visit(stmt)
                
            self.emit('POP_EXCEPT')
            end_jump_idx = self.emit('JUMP', None)
            
            handler_ip = len(self.current_bytecode.instructions)
            self.current_bytecode.instructions[handler_jump_idx] = ('SETUP_EXCEPT', handler_ip)
            
            # In handler: we can bind exception object
            # We emit Exception handler check
            for h in node.handlers:
                # h = (err_type_name, err_var_name, body_nodes)
                self.emit('CHECK_EXCEPTION_TYPE', h[0])
                match_jump_idx = self.emit('JUMP_IF_FALSE', None)
                
                if h[1]:
                    self.emit('STORE_VAR', h[1])
                else:
                    self.emit('POP') # Pop exception object
                    
                for stmt in h[2]:
                    self.visit(stmt)
                    
                self.emit('CLEAR_EXCEPTION')
                self.emit('JUMP', end_jump_idx) # Jump to end of try-except
                
                next_handler_ip = len(self.current_bytecode.instructions)
                self.current_bytecode.instructions[match_jump_idx] = ('JUMP_IF_FALSE', next_handler_ip)
                
            # If no handler matches, re-raise!
            self.emit('RERAISE_EXCEPTION')
            
            end_ip = len(self.current_bytecode.instructions)
            self.current_bytecode.instructions[end_jump_idx] = ('JUMP', end_ip)
            
        else:
            raise NotImplementedError(f"Düğüm {node_class.__name__} derlenemedi.")
