# -*- coding: utf-8 -*-
import sys
import json
import traceback
import math
import random
import time

class OzdilError(Exception):
    def __init__(self, friendly_type, message, lineno):
        super().__init__(message)
        self.friendly_type = friendly_type
        self.message = message
        self.lineno = lineno

class Token:
    def __init__(self, type_, value, lineno, col):
        self.type = type_
        self.value = value
        self.lineno = lineno
        self.col = col
        
    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)}, {self.lineno}:{self.col})"

def tokenize_line(line_str, lineno):
    tokens = []
    i = 0
    n = len(line_str)
    
    while i < n:
        c = line_str[i]
        
        # Skip spaces
        if c in ' \t':
            i += 1
            continue
            
        # Comment
        if c == '#':
            break # Discard comment for rest of the line
            
        # Numbers (floats and ints)
        if c.isdigit():
            start_col = i + 1
            val = ""
            while i < n and (line_str[i].isdigit() or line_str[i] == '.'):
                val += line_str[i]
                i += 1
            if '.' in val:
                tokens.append(Token('NUM_FLOAT', val, lineno, start_col))
            else:
                tokens.append(Token('NUM_INT', val, lineno, start_col))
            continue
            
        # Strings
        if c in ('"', "'"):
            start_col = i + 1
            quote = c
            val = c
            i += 1
            closed = False
            while i < n:
                val += line_str[i]
                if line_str[i] == quote and line_str[i-1] != '\\':
                    i += 1
                    closed = True
                    break
                i += 1
            if not closed:
                raise SyntaxError(f"Kapatılmamış metin ifadesi: '{val}'")
            tokens.append(Token('STRING', val, lineno, start_col))
            continue
            
        # Identifiers and keywords (including Turkish letters)
        if c.isalpha() or c in 'çğıöşüÇĞİÖŞÜ_':
            start_col = i + 1
            val = ""
            while i < n and (line_str[i].isalnum() or line_str[i] in 'çğıöşüÇĞİÖŞÜ_'):
                val += line_str[i]
                i += 1
                
            keywords_list = (
                'eğer', 'eger', 'değişken_eğer', 'degilse_eger', 'değilse_eğer', 'degilse_eğer', 'değilse_eger', 
                'değilse', 'degilse', 'iken', 'döngü', 'dongu', 'her', 'işlem', 'islem', 'fonksiyon', 
                'döndür', 'dondur', 'doğru', 'dogru', 'yanlış', 'yanlis', 've', 'veya', 'değil', 'degil', 
                'içinde', 'icinde', 'in', 'getir', 'dur', 'devam_et', 'yok', 'boş', 'bos', 
                'değişken', 'degisken', 'sabit', 'tam_sayı', 'tam_sayi', 'ondalık', 'ondalik', 
                'metin', 'liste', 'sözlük', 'sozluk', 'break', 'continue', 'and', 'or', 'not'
            )
            if val in keywords_list:
                tokens.append(Token('KEYWORD', val, lineno, start_col))
            else:
                tokens.append(Token('ID', val, lineno, start_col))
            continue
            
        # Multi-char operators
        if i + 1 < n and line_str[i:i+2] in ('==', '!=', '<=', '>=', '**'):
            tokens.append(Token('OP', line_str[i:i+2], lineno, i + 1))
            i += 2
            continue
            
        # Single-char operators
        if c in '+-*/%=<>()[]{}:,.:':
            tokens.append(Token('OP', c, lineno, i + 1))
            i += 1
            continue
            
        raise SyntaxError(f"Geçersiz karakter: '{c}'")
        
    return tokens

def lex_ozdil(code_str):
    lines = code_str.splitlines()
    all_tokens = []
    indent_stack = [0]
    
    for idx, line in enumerate(lines):
        lineno = idx + 1
        
        # Strip trailing whitespaces
        stripped = line.rstrip()
        
        # Check if empty or only a comment
        if not stripped.strip() or stripped.strip().startswith('#'):
            continue
            
        # Count leading whitespace
        indent_level = 0
        for char in line:
            if char == ' ':
                indent_level += 1
            elif char == '\t':
                indent_level += 4
            else:
                break
                
        # Tokenize the line
        line_tokens = tokenize_line(stripped[indent_level:], lineno)
        if not line_tokens:
            continue
            
        # Determine indent/dedent
        if indent_level > indent_stack[-1]:
            indent_stack.append(indent_level)
            all_tokens.append(Token('INDENT', '    ', lineno, 1))
        elif indent_level < indent_stack[-1]:
            while indent_level < indent_stack[-1]:
                indent_stack.pop()
                all_tokens.append(Token('DEDENT', '', lineno, 1))
            if indent_level != indent_stack[-1]:
                raise IndentationError("Girinti düzeyleri eşleşmiyor.")
                
        # Extend line tokens and add newline
        all_tokens.extend(line_tokens)
        all_tokens.append(Token('NEWLINE', '\n', lineno, len(line) + 1))
        
    # Add any remaining dedents
    while len(indent_stack) > 1:
        indent_stack.pop()
        all_tokens.append(Token('DEDENT', '', len(lines), 1))
        
    return all_tokens

# --- AST CLASSES ---

class ASTNode:
    def to_dict(self):
        raise NotImplementedError()

class Program(ASTNode):
    def __init__(self, body):
        self.body = body
    def to_dict(self):
        return {
            "type": "Program",
            "body": [node.to_dict() for node in self.body]
        }

class Atama(ASTNode):
    def __init__(self, target, value, lineno, modifier=None):
        self.target = target
        self.value = value
        self.lineno = lineno
        self.modifier = modifier
    def to_dict(self):
        return {
            "type": "Atama (Atama)",
            "lineno": self.lineno,
            "hedef": self.target.to_dict(),
            "değer": self.value.to_dict(),
            "belirleyici": self.modifier
        }

class Eger(ASTNode):
    def __init__(self, test, body, orelse, lineno):
        self.test = test
        self.body = body
        self.orelse = orelse
        self.lineno = lineno
    def to_dict(self):
        return {
            "type": "Eger (Koşul)",
            "lineno": self.lineno,
            "test": self.test.to_dict(),
            "gövde": [node.to_dict() for node in self.body],
            "değilse": [node.to_dict() for node in self.orelse] if self.orelse else None
        }

class Iken(ASTNode):
    def __init__(self, test, body, lineno):
        self.test = test
        self.body = body
        self.lineno = lineno
    def to_dict(self):
        return {
            "type": "Iken (Döngü)",
            "lineno": self.lineno,
            "test": self.test.to_dict(),
            "gövde": [node.to_dict() for node in self.body]
        }

class Dongu(ASTNode):
    def __init__(self, target, iter_expr, body, lineno):
        self.target = target
        self.iter_expr = iter_expr
        self.body = body
        self.lineno = lineno
    def to_dict(self):
        return {
            "type": "Dongu (For)",
            "lineno": self.lineno,
            "değişken": self.target.to_dict(),
            "aralık_veri": self.iter_expr.to_dict(),
            "gövde": [node.to_dict() for node in self.body]
        }

class Islem(ASTNode):
    def __init__(self, name, args, body, lineno):
        self.name = name
        self.args = args
        self.body = body
        self.lineno = lineno
    def to_dict(self):
        return {
            "type": "Islem (Fonksiyon)",
            "lineno": self.lineno,
            "ad": self.name,
            "parametreler": self.args,
            "gövde": [node.to_dict() for node in self.body]
        }

class Dondur(ASTNode):
    def __init__(self, value, lineno):
        self.value = value
        self.lineno = lineno
    def to_dict(self):
        return {
            "type": "Dondur (Return)",
            "lineno": self.lineno,
            "değer": self.value.to_dict() if self.value else None
        }

class Getir(ASTNode):
    def __init__(self, name, lineno):
        self.name = name
        self.lineno = lineno
    def to_dict(self):
        return {
            "type": "Getir (Kütüphane)",
            "lineno": self.lineno,
            "kütüphane": self.name
        }

class IkiliIslem(ASTNode):
    def __init__(self, op, left, right, lineno):
        self.op = op
        self.left = left
        self.right = right
        self.lineno = lineno
    def to_dict(self):
        return {
            "type": "IkiliIslem",
            "lineno": self.lineno,
            "işleç": self.op,
            "sol": self.left.to_dict(),
            "sağ": self.right.to_dict()
        }

class TekliIslem(ASTNode):
    def __init__(self, op, operand, lineno):
        self.op = op
        self.operand = operand
        self.lineno = lineno
    def to_dict(self):
        return {
            "type": "TekliIslem",
            "lineno": self.lineno,
            "işleç": self.op,
            "sağ": self.operand.to_dict()
        }

class Degisken(ASTNode):
    def __init__(self, name, lineno):
        self.name = name
        self.lineno = lineno
    def to_dict(self):
        return {
            "type": "Degisken (Değişken)",
            "lineno": self.lineno,
            "ad": self.name
        }

class Deger(ASTNode):
    def __init__(self, value, lineno):
        self.value = value
        self.lineno = lineno
    def to_dict(self):
        return {
            "type": "Deger (Sabit)",
            "lineno": self.lineno,
            "değer": self.value
        }

class Cagir(ASTNode):
    def __init__(self, func, args, lineno):
        self.func = func
        self.args = args
        self.lineno = lineno
    def to_dict(self):
        return {
            "type": "Cagir (Çağrı)",
            "lineno": self.lineno,
            "fonksiyon": self.func.to_dict(),
            "parametreler": [node.to_dict() for node in self.args]
        }

class Nitelik(ASTNode):
    def __init__(self, value, attr, lineno):
        self.value = value
        self.attr = attr
        self.lineno = lineno
    def to_dict(self):
        return {
            "type": "Nitelik (Özellik)",
            "lineno": self.lineno,
            "nesne": self.value.to_dict(),
            "nitelik": self.attr
        }

class Endeks(ASTNode):
    def __init__(self, value, index, lineno):
        self.value = value
        self.index = index
        self.lineno = lineno
    def to_dict(self):
        return {
            "type": "Endeks (Erişim)",
            "lineno": self.lineno,
            "nesne": self.value.to_dict(),
            "indeks": self.index.to_dict()
        }

class Liste(ASTNode):
    def __init__(self, elts, lineno):
        self.elts = elts
        self.lineno = lineno
    def to_dict(self):
        return {
            "type": "Liste",
            "lineno": self.lineno,
            "elemanlar": [node.to_dict() for node in self.elts]
        }

class Sozluk(ASTNode):
    def __init__(self, keys, values, lineno):
        self.keys = keys
        self.values = values
        self.lineno = lineno
    def to_dict(self):
        return {
            "type": "Sozluk",
            "lineno": self.lineno,
            "anahtarlar": [node.to_dict() for node in self.keys],
            "değerler": [node.to_dict() for node in self.values]
        }

class Ifade(ASTNode):
    def __init__(self, expr, lineno):
        self.expr = expr
        self.lineno = lineno
    def to_dict(self):
        return {
            "type": "Ifade",
            "lineno": self.lineno,
            "ifade": self.expr.to_dict()
        }

class DurNode(ASTNode):
    def __init__(self, lineno):
        self.lineno = lineno
    def to_dict(self):
        return {"type": "Dur (Break)", "lineno": self.lineno}

class DevamEtNode(ASTNode):
    def __init__(self, lineno):
        self.lineno = lineno
    def to_dict(self):
        return {"type": "DevamEt (Continue)", "lineno": self.lineno}

# --- PARSER ---

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        
    def current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        last_line = self.tokens[-1].lineno if self.tokens else 1
        return Token('EOF', '', last_line, 1)
        
    def peek(self, offset=1):
        if self.pos + offset < len(self.tokens):
            return self.tokens[self.pos + offset]
        last_line = self.tokens[-1].lineno if self.tokens else 1
        return Token('EOF', '', last_line, 1)
        
    def eat(self, type_, value=None):
        tok = self.current()
        if tok.type == type_:
            if value is None or tok.value == value:
                self.pos += 1
                return tok
        val_desc = f"'{value}'" if value else type_
        raise SyntaxError(f"Yazım hatası: Beklenen {val_desc}, fakat '{tok.value}' bulundu.")
        
    def expect_statement_end(self):
        if self.current().type == 'NEWLINE':
            self.eat('NEWLINE')
        elif self.current().type not in ('DEDENT', 'EOF'):
            raise SyntaxError(f"Beklenmeyen ifade sonu veya yeni satır eksik: '{self.current().value}'")

    def parse_program(self):
        body = []
        while self.pos < len(self.tokens):
            while self.current().type == 'NEWLINE':
                self.eat('NEWLINE')
            if self.pos >= len(self.tokens) or self.current().type == 'EOF':
                break
            body.append(self.parse_statement())
        return Program(body)
        
    def parse_statement(self):
        curr = self.current()
        if curr.type == 'KEYWORD':
            if curr.value in ('eğer', 'eger'):
                return self.parse_eger()
            elif curr.value == 'iken':
                return self.parse_iken()
            elif curr.value in ('döngü', 'dongu', 'her'):
                return self.parse_dongu()
            elif curr.value in ('işlem', 'islem', 'fonksiyon'):
                return self.parse_islem()
            elif curr.value in ('döndür', 'dondur'):
                return self.parse_dondur()
            elif curr.value in ('dur', 'break'):
                self.eat('KEYWORD')
                self.expect_statement_end()
                return DurNode(curr.lineno)
            elif curr.value in ('devam_et', 'continue'):
                self.eat('KEYWORD')
                self.expect_statement_end()
                return DevamEtNode(curr.lineno)
            elif curr.value in ('getir', 'import'):
                return self.parse_getir()
                
        return self.parse_atama_or_expr()

    def parse_eger(self):
        tok = self.eat('KEYWORD')
        test = self.parse_expression()
        self.eat('OP', ':')
        self.eat('NEWLINE')
        self.eat('INDENT')
        body = []
        while self.current().type != 'DEDENT' and self.current().type != 'EOF':
            while self.current().type == 'NEWLINE':
                self.eat('NEWLINE')
            if self.current().type in ('DEDENT', 'EOF'):
                break
            body.append(self.parse_statement())
        self.eat('DEDENT')
        
        elif_nodes = []
        while self.current().type == 'KEYWORD' and self.current().value in ('değişken_eğer', 'degilse_eger', 'değilse_eğer', 'degilse_eğer', 'değilse_eger'):
            elif_tok = self.eat('KEYWORD')
            elif_test = self.parse_expression()
            self.eat('OP', ':')
            self.eat('NEWLINE')
            self.eat('INDENT')
            elif_body = []
            while self.current().type != 'DEDENT' and self.current().type != 'EOF':
                while self.current().type == 'NEWLINE':
                    self.eat('NEWLINE')
                if self.current().type in ('DEDENT', 'EOF'):
                    break
                elif_body.append(self.parse_statement())
            self.eat('DEDENT')
            elif_nodes.append(Eger(elif_test, elif_body, [], elif_tok.lineno))
            
        else_body = []
        if self.current().type == 'KEYWORD' and self.current().value in ('değilse', 'degilse'):
            self.eat('KEYWORD')
            self.eat('OP', ':')
            self.eat('NEWLINE')
            self.eat('INDENT')
            while self.current().type != 'DEDENT' and self.current().type != 'EOF':
                while self.current().type == 'NEWLINE':
                    self.eat('NEWLINE')
                if self.current().type in ('DEDENT', 'EOF'):
                    break
                else_body.append(self.parse_statement())
            self.eat('DEDENT')
            
        current_orelse = else_body
        for elif_node in reversed(elif_nodes):
            elif_node.orelse = current_orelse
            current_orelse = [elif_node]
            
        return Eger(test, body, current_orelse, tok.lineno)
        
    def parse_iken(self):
        tok = self.eat('KEYWORD')
        test = self.parse_expression()
        self.eat('OP', ':')
        self.eat('NEWLINE')
        self.eat('INDENT')
        body = []
        while self.current().type != 'DEDENT' and self.current().type != 'EOF':
            while self.current().type == 'NEWLINE':
                self.eat('NEWLINE')
            if self.current().type in ('DEDENT', 'EOF'):
                break
            body.append(self.parse_statement())
        self.eat('DEDENT')
        return Iken(test, body, tok.lineno)
        
    def parse_dongu(self):
        tok = self.eat('KEYWORD')
        target_tok = self.eat('ID')
        target = Degisken(target_tok.value, target_tok.lineno)
        
        # 'içinde' / 'icinde' / 'in' is optional
        next_tok = self.current()
        if next_tok.type == 'KEYWORD' and next_tok.value in ('içinde', 'icinde', 'in'):
            self.pos += 1
            
        iter_expr = self.parse_expression()
        self.eat('OP', ':')
        self.eat('NEWLINE')
        self.eat('INDENT')
        body = []
        while self.current().type != 'DEDENT' and self.current().type != 'EOF':
            while self.current().type == 'NEWLINE':
                self.eat('NEWLINE')
            if self.current().type in ('DEDENT', 'EOF'):
                break
            body.append(self.parse_statement())
        self.eat('DEDENT')
        return Dongu(target, iter_expr, body, tok.lineno)
        
    def parse_islem(self):
        tok = self.eat('KEYWORD')
        name_tok = self.eat('ID')
        name = name_tok.value
        
        self.eat('OP', '(')
        args = []
        if self.current().type == 'ID':
            args.append(self.eat('ID').value)
            while self.current().type == 'OP' and self.current().value == ',':
                self.eat('OP')
                args.append(self.eat('ID').value)
        self.eat('OP', ')')
        
        self.eat('OP', ':')
        self.eat('NEWLINE')
        self.eat('INDENT')
        body = []
        while self.current().type != 'DEDENT' and self.current().type != 'EOF':
            while self.current().type == 'NEWLINE':
                self.eat('NEWLINE')
            if self.current().type in ('DEDENT', 'EOF'):
                break
            body.append(self.parse_statement())
        self.eat('DEDENT')
        return Islem(name, args, body, tok.lineno)
        
    def parse_dondur(self):
        tok = self.eat('KEYWORD')
        value = None
        if self.current().type != 'NEWLINE':
            value = self.parse_expression()
        self.expect_statement_end()
        return Dondur(value, tok.lineno)
        
    def parse_getir(self):
        tok = self.eat('KEYWORD')
        name_tok = self.eat('ID')
        name = name_tok.value
        self.expect_statement_end()
        return Getir(name, tok.lineno)

    def parse_atama_or_expr(self):
        curr = self.current()
        type_modifiers = (
            'değişken', 'degisken', 'sabit', 
            'tam_sayı', 'tam_sayi', 'ondalık', 'ondalik', 
            'metin', 'liste', 'sözlük', 'sozluk'
        )
        if curr.type == 'KEYWORD' and curr.value in type_modifiers:
            mod_tok = self.eat('KEYWORD')
            target_tok = self.eat('ID')
            target = Degisken(target_tok.value, target_tok.lineno)
            self.eat('OP', '=')
            value = self.parse_expression()
            self.expect_statement_end()
            return Atama(target, value, curr.lineno, modifier=mod_tok.value)
            
        expr = self.parse_expression()
        if self.current().type == 'OP' and self.current().value == '=':
            self.eat('OP')
            value = self.parse_expression()
            self.expect_statement_end()
            return Atama(expr, value, curr.lineno)
            
        self.expect_statement_end()
        return Ifade(expr, curr.lineno)

    def parse_expression(self):
        return self.parse_logical_or()
        
    def parse_logical_or(self):
        node = self.parse_logical_and()
        while self.current().type == 'KEYWORD' and self.current().value in ('veya', 'or'):
            op_tok = self.eat('KEYWORD')
            right = self.parse_logical_and()
            node = IkiliIslem('veya', node, right, op_tok.lineno)
        return node
        
    def parse_logical_and(self):
        node = self.parse_logical_not()
        while self.current().type == 'KEYWORD' and self.current().value in ('ve', 'and'):
            op_tok = self.eat('KEYWORD')
            right = self.parse_logical_not()
            node = IkiliIslem('ve', node, right, op_tok.lineno)
        return node
        
    def parse_logical_not(self):
        if self.current().type == 'KEYWORD' and self.current().value in ('değil', 'degil', 'not'):
            op_tok = self.eat('KEYWORD')
            operand = self.parse_logical_not()
            return TekliIslem('değil', operand, op_tok.lineno)
        return self.parse_comparison()
        
    def parse_comparison(self):
        node = self.parse_additive()
        ops = ('==', '!=', '<', '>', '<=', '>=')
        while self.current().type == 'OP' and self.current().value in ops:
            op_tok = self.eat('OP')
            right = self.parse_additive()
            node = IkiliIslem(op_tok.value, node, right, op_tok.lineno)
        return node
        
    def parse_additive(self):
        node = self.parse_multiplicative()
        while self.current().type == 'OP' and self.current().value in ('+', '-'):
            op_tok = self.eat('OP')
            right = self.parse_multiplicative()
            node = IkiliIslem(op_tok.value, node, right, op_tok.lineno)
        return node
        
    def parse_multiplicative(self):
        node = self.parse_power()
        while self.current().type == 'OP' and self.current().value in ('*', '/', '%'):
            op_tok = self.eat('OP')
            right = self.parse_power()
            node = IkiliIslem(op_tok.value, node, right, op_tok.lineno)
        return node
        
    def parse_power(self):
        node = self.parse_unary()
        if self.current().type == 'OP' and self.current().value == '**':
            op_tok = self.eat('OP')
            right = self.parse_power()
            return IkiliIslem('**', node, right, op_tok.lineno)
        return node
        
    def parse_unary(self):
        if self.current().type == 'OP' and self.current().value in ('+', '-'):
            op_tok = self.eat('OP')
            operand = self.parse_unary()
            return TekliIslem(op_tok.value, operand, op_tok.lineno)
        return self.parse_primary()

    def parse_primary(self):
        node = self.parse_atom()
        while True:
            curr = self.current()
            if curr.type == 'OP' and curr.value == '(':
                self.eat('OP')
                args = []
                if self.current().type != 'OP' or self.current().value != ')':
                    args.append(self.parse_expression())
                    while self.current().type == 'OP' and self.current().value == ',':
                        self.eat('OP')
                        args.append(self.parse_expression())
                self.eat('OP')
                node = Cagir(node, args, curr.lineno)
            elif curr.type == 'OP' and curr.value == '[':
                self.eat('OP')
                index_expr = self.parse_expression()
                self.eat('OP')
                node = Endeks(node, index_expr, curr.lineno)
            elif curr.type == 'OP' and curr.value == '.':
                self.eat('OP')
                attr_tok = self.eat('ID')
                node = Nitelik(node, attr_tok.value, curr.lineno)
            else:
                break
        return node

    def parse_atom(self):
        tok = self.current()
        if tok.type == 'NUM_INT':
            self.eat('NUM_INT')
            return Deger(int(tok.value), tok.lineno)
        elif tok.type == 'NUM_FLOAT':
            self.eat('NUM_FLOAT')
            return Deger(float(tok.value), tok.lineno)
        elif tok.type == 'STRING':
            self.eat('STRING')
            val = tok.value[1:-1]
            # Handle minor escape sequences
            val = val.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"').replace("\\'", "'")
            return Deger(val, tok.lineno)
        elif tok.type == 'KEYWORD' and tok.value in ('doğru', 'dogru'):
            self.eat('KEYWORD')
            return Deger(True, tok.lineno)
        elif tok.type == 'KEYWORD' and tok.value in ('yanlış', 'yanlis'):
            self.eat('KEYWORD')
            return Deger(False, tok.lineno)
        elif tok.type == 'KEYWORD' and tok.value in ('yok', 'boş', 'bos'):
            self.eat('KEYWORD')
            return Deger(None, tok.lineno)
        elif tok.type == 'ID':
            self.eat('ID')
            return Degisken(tok.value, tok.lineno)
        elif tok.type == 'OP' and tok.value == '(':
            self.eat('OP')
            expr = self.parse_expression()
            self.eat('OP')
            return expr
        elif tok.type == 'OP' and tok.value == '[':
            self.eat('OP')
            elts = []
            if self.current().type != 'OP' or self.current().value != ']':
                elts.append(self.parse_expression())
                while self.current().type == 'OP' and self.current().value == ',':
                    self.eat('OP')
                    elts.append(self.parse_expression())
            self.eat('OP')
            return Liste(elts, tok.lineno)
        elif tok.type == 'OP' and tok.value == '{':
            self.eat('OP')
            keys = []
            values = []
            if self.current().type != 'OP' or self.current().value != '}':
                keys.append(self.parse_expression())
                self.eat('OP', ':')
                values.append(self.parse_expression())
                while self.current().type == 'OP' and self.current().value == ',':
                    self.eat('OP')
                    keys.append(self.parse_expression())
                    self.eat('OP', ':')
                    values.append(self.parse_expression())
            self.eat('OP')
            return Sozluk(keys, values, tok.lineno)
        else:
            raise SyntaxError(f"Geçersiz sözdizimi: '{tok.value}'")

# --- ENVIRONMENT & INTERPRETER ---

class Environment:
    def __init__(self, parent=None):
        self.values = {}
        self.types = {}
        self.constants = set()
        self.parent = parent
        
    def define(self, name, value, modifier=None):
        self.values[name] = value
        if modifier:
            if modifier in ('sabit',):
                self.constants.add(name)
            elif modifier in ('tam_sayı', 'tam_sayi', 'ondalık', 'ondalik', 'metin', 'liste', 'sözlük', 'sozluk'):
                self.types[name] = modifier
        
    def lookup(self, name, lineno):
        if name in self.values:
            return self.values[name]
        if self.parent:
            return self.parent.lookup(name, lineno)
            
        raise OzdilError(
            "Tanımlama Hatası (NameError)",
            f"'{name}' adında bir değişken, fonksiyon veya kütüphane bulunamadı. Lütfen adını doğru yazdığınızdan emin olun.",
            lineno
        )
        
    def assign(self, name, value, lineno, modifier=None):
        if self.is_constant(name):
            raise OzdilError(
                "Değer Hatası (ValueError)",
                f"'{name}' bir sabittir (constant) ve değeri değiştirilemez.",
                lineno
            )
            
        if modifier:
            self.validate_type(modifier, value, lineno)
            
        target_env = self.find_env_for_var(name)
        if target_env:
            if name in target_env.types:
                target_env.validate_type(target_env.types[name], value, lineno)
            target_env.values[name] = value
            if modifier == 'sabit':
                target_env.constants.add(name)
            elif modifier:
                target_env.types[name] = modifier
        else:
            self.values[name] = value
            if modifier == 'sabit':
                self.constants.add(name)
            elif modifier:
                self.types[name] = modifier
                
    def is_constant(self, name):
        if name in self.constants:
            return True
        if self.parent:
            return self.parent.is_constant(name)
        return False
        
    def find_env_for_var(self, name):
        if name in self.values:
            return self
        if self.parent:
            return self.parent.find_env_for_var(name)
        return None
        
    def validate_type(self, modifier, value, lineno):
        if modifier in ('tam_sayı', 'tam_sayi'):
            if not isinstance(value, int) or isinstance(value, bool):
                raise OzdilError(
                    "Tür Hatası (TypeError)",
                    f"Beklenen tür 'tam_sayı', ancak '{type(value).__name__}' türünde değer verildi.",
                    lineno
                )
        elif modifier in ('ondalık', 'ondalik'):
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                raise OzdilError(
                    "Tür Hatası (TypeError)",
                    f"Beklenen tür 'ondalık', ancak '{type(value).__name__}' türünde değer verildi.",
                    lineno
                )
        elif modifier == 'metin':
            if not isinstance(value, str):
                raise OzdilError(
                    "Tür Hatası (TypeError)",
                    f"Beklenen tür 'metin', ancak '{type(value).__name__}' türünde değer verildi.",
                    lineno
                )
        elif modifier == 'liste':
            if not isinstance(value, list):
                raise OzdilError(
                    "Tür Hatası (TypeError)",
                    f"Beklenen tür 'liste', ancak '{type(value).__name__}' türünde değer verildi.",
                    lineno
                )
        elif modifier in ('sözlük', 'sozluk'):
            if not isinstance(value, dict):
                raise OzdilError(
                    "Tür Hatası (TypeError)",
                    f"Beklenen tür 'sözlük', ancak '{type(value).__name__}' türünde değer verildi.",
                    lineno
                )

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class BreakException(Exception):
    pass

class ContinueException(Exception):
    pass

def get_attribute(obj, attr, lineno):
    if isinstance(obj, list):
        if attr in ('ekle', 'append'):
            return obj.append
        if attr in ('çıkar', 'cikar', 'remove'):
            return obj.remove
        if attr in ('temizle', 'clear'):
            return obj.clear
        if attr in ('uzunluk', 'len'):
            return lambda: len(obj)
        if attr in ('sırala', 'sirala', 'sort'):
            return obj.sort
        if attr in ('ters_çevir', 'ters_cevir', 'reverse'):
            return obj.reverse
        if attr in ('bul', 'index'):
            return obj.index
        if attr in ('say', 'count'):
            return obj.count
        if attr in ('sil', 'pop'):
            return obj.pop
    elif isinstance(obj, dict):
        if attr in ('anahtarlar', 'keys'):
            return lambda: list(obj.keys())
        if attr in ('değerler', 'degerler', 'values'):
            return lambda: list(obj.values())
        if attr in ('temizle', 'clear'):
            return obj.clear
    elif isinstance(obj, str):
        if attr in ('büyük_harf', 'buyuk_harf', 'upper'):
            return obj.upper
        if attr in ('küçük_harf', 'kucuk_harf', 'lower'):
            return obj.lower
            
    if isinstance(obj, dict) and attr in obj:
        return obj[attr]
        
    if hasattr(obj, attr):
        return getattr(obj, attr)
        
    raise OzdilError(
        "Öznitelik Hatası (AttributeError)",
        f"'{type(obj).__name__}' nesnesinin '{attr}' adında bir özelliği veya fonksiyonu yok.",
        lineno
    )

def load_external_package(name, lineno, stdout_ref):
    import os
    import json
    import re
    import math
    import random
    import time
    
    from ozdil.package_manager import verify_package_signature
    from ozdil.sandbox import verify_python_code
    import ozdil.plugin_api
    
    package_dirs = [
        os.path.abspath(os.path.expanduser("~/.ozdil/packages")),
        os.path.abspath("./oz_packages"),
    ]
    
    found_pkg_dir = None
    for pdir in package_dirs:
        potential_dir = os.path.join(pdir, name)
        if os.path.isdir(potential_dir):
            found_pkg_dir = potential_dir
            break
            
    if not found_pkg_dir:
        raise OzdilError(
            "Kütüphane Hatası (ImportError)",
            f"'{name}' kütüphanesi bulunamadı. Lütfen 'ozpip' ile yüklendiğinden veya yerel olarak mevcut olduğundan emin olun.",
            lineno
        )
        
    config_file = os.path.join(found_pkg_dir, "ozpaket.json")
    if not os.path.isfile(config_file):
        raise OzdilError(
            "Kütüphane Hatası (ImportError)",
            f"'{name}' kütüphanesinde 'ozpaket.json' yapılandırma dosyası eksik.",
            lineno
        )
        
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            meta = json.load(f)
    except Exception as e:
        raise OzdilError(
            "Kütüphane Hatası (ImportError)",
            f"'{name}' kütüphanesinin 'ozpaket.json' dosyası okunamadı veya geçersiz JSON: {str(e)}",
            lineno
        )
        
    # 1. Sürüm imza doğrulaması (SHA256)
    sig_ok, sig_msg = verify_package_signature(name)
    if not sig_ok:
        raise OzdilError(
            "Güvenlik Hatası (SignatureError)",
            f"'{name}' kütüphanesi güvenlik/imza testini geçemedi: {sig_msg}",
            lineno
        )
        
    pkg_type = meta.get("tur", "ozdil")
    permissions = meta.get("izinler", [])
    
    # Tetikle: paket_yuklendi
    ozdil.plugin_api.plugin.trigger_event("paket_yuklendi", name)
    
    if pkg_type == "ozdil":
        entry_file = os.path.join(found_pkg_dir, f"{name}.oz")
        if not os.path.isfile(entry_file):
            entry_file = os.path.join(found_pkg_dir, "main.oz")
            
        if not os.path.isfile(entry_file):
            raise OzdilError(
                "Kütüphane Hatası (ImportError)",
                f"'{name}' kütüphanesinde bir giriş dosyası ('{name}.oz' veya 'main.oz') bulunamadı.",
                lineno
            )
            
        try:
            with open(entry_file, "r", encoding="utf-8") as f:
                code_content = f.read()
        except Exception as e:
            raise OzdilError(
                "Kütüphane Hatası (ImportError)",
                f"'{name}' kütüphanesinin giriş dosyası okunamadı: {str(e)}",
                lineno
            )
            
        try:
            pkg_tokens = lex_ozdil(code_content)
            pkg_parser = Parser(pkg_tokens)
            pkg_ast = pkg_parser.parse_program()
            
            pkg_interpreter = Interpreter()
            pkg_interpreter.stdout = stdout_ref
            
            pkg_interpreter.eval(pkg_ast, pkg_interpreter.global_env)
            return pkg_interpreter.global_env.values
        except Exception as e:
            if isinstance(e, OzdilError):
                raise OzdilError(
                    f"Kütüphane Hatası ({e.friendly_type})",
                    f"'{name}' kütüphanesi yüklenirken hata oluştu (Satır {e.lineno}): {e.message}",
                    lineno
                )
            raise OzdilError(
                "Kütüphane Hatası (ImportError)",
                f"'{name}' kütüphanesi yürütülürken hata: {str(e)}",
                lineno
            )
            
    elif pkg_type == "python":
        entry_file = os.path.join(found_pkg_dir, f"{name}.py")
        if not os.path.isfile(entry_file):
            entry_file = os.path.join(found_pkg_dir, "main.py")
            
        if not os.path.isfile(entry_file):
            raise OzdilError(
                "Kütüphane Hatası (ImportError)",
                f"'{name}' kütüphanesinde Python giriş dosyası ('{name}.py' veya 'main.py') bulunamadı.",
                lineno
            )
            
        try:
            with open(entry_file, "r", encoding="utf-8") as f:
                code_content = f.read()
        except Exception as e:
            raise OzdilError(
                "Kütüphane Hatası (ImportError)",
                f"'{name}' kütüphanesinin Python dosyası okunamadı: {str(e)}",
                lineno
            )
            
        # 2. Gelişmiş AST-tabanlı Python Sandbox Güvenlik Kontrolü
        sandbox_ok, sandbox_errors = verify_python_code(code_content, name, permissions)
        if not sandbox_ok:
            raise OzdilError(
                "Güvenlik Hatası (SecurityError)",
                f"'{name}' Python eklentisi güvenlik süzgecini geçemedi:\n" + "\n".join(sandbox_errors),
                lineno
            )
            
        try:
            local_scope = {}
            exec_globals = {
                "__builtins__": __builtins__,
                "print": lambda *args: stdout_ref.append(" ".join(str(x) for x in args) + "\n"),
                "math": math,
                "random": random,
                "time": time,
                "plugin_api": ozdil.plugin_api
            }
            exec(code_content, exec_globals, local_scope)
            
            if "plugin" not in local_scope:
                raise OzdilError(
                    "Güvenlik Hatası (PluginError)",
                    f"'{name}' kütüphanesinde 'plugin()' fonksiyonu tanımlanmamış.",
                    lineno
                )
                
            plugin_func = local_scope["plugin"]
            if not callable(plugin_func):
                raise OzdilError(
                    "Güvenlik Hatası (PluginError)",
                    f"'{name}' kütüphanesindeki 'plugin' bir fonksiyon değil.",
                    lineno
                )
                
            plugin_apis = plugin_func()
            if not isinstance(plugin_apis, dict):
                raise OzdilError(
                    "Güvenlik Hatası (PluginError)",
                    f"'{name}' kütüphanesinin 'plugin()' fonksiyonu bir sözlük döndürmeli.",
                    lineno
                )
                
            return plugin_apis
        except Exception as e:
            if isinstance(e, OzdilError):
                raise e
            raise OzdilError(
                "Kütüphane Hatası (ImportError)",
                f"'{name}' Python eklentisi yüklenirken hata oluştu: {str(e)}",
                lineno
            )
    else:
        raise OzdilError(
            "Kütüphane Hatası (ImportError)",
            f"'{name}' kütüphanesinin türü ('{pkg_type}') desteklenmiyor. Geçerli türler: 'ozdil', 'python'",
            lineno
        )

class Interpreter:
    def __init__(self):
        self.stdout = []
        self.global_env = Environment()
        self.init_builtins()
        
    def init_builtins(self):
        def oz_yazdir(*args):
            def tr_val(val):
                if val is True: return "doğru"
                if val is False: return "yanlış"
                if val is None: return "boş"
                if isinstance(val, list):
                    return "[" + ", ".join(tr_val(x) for x in val) + "]"
                if isinstance(val, dict):
                    return "{" + ", ".join(f"{tr_val(k)}: {tr_val(v)}" for k, v in val.items()) + "}"
                return str(val)
            text = " ".join(tr_val(x) for x in args)
            self.stdout.append(text + "\n")
            
        self.global_env.define('yazdır', oz_yazdir)
        self.global_env.define('yazdir', oz_yazdir)
        self.global_env.define('uzunluk', len)
        
        self.global_env.define('tam_sayı', int)
        self.global_env.define('tam_sayi', int)
        self.global_env.define('ondalık', float)
        self.global_env.define('ondalik', float)
        self.global_env.define('metin', str)
        self.global_env.define('aralık', range)
        self.global_env.define('aralik', range)
        
        # Register math direct calls for convenience/backwards compatibility
        self.global_env.define('karekök', math.sqrt)
        self.global_env.define('karekok', math.sqrt)
        self.global_env.define('faktöriyel', math.factorial)
        self.global_env.define('faktoriyel', math.factorial)
        self.global_env.define('sinüs', math.sin)
        self.global_env.define('sinus', math.sin)
        self.global_env.define('kosinüs', math.cos)
        self.global_env.define('kosinus', math.cos)
        self.global_env.define('tanjant', math.tan)
        self.global_env.define('radyan', math.radians)
        self.global_env.define('derece', math.degrees)
        self.global_env.define('üs', math.pow)
        self.global_env.define('us', math.pow)
        self.global_env.define('mutlak', math.fabs)
        self.global_env.define('aşağı_yuvarla', math.floor)
        self.global_env.define('asagi_yuvarla', math.floor)
        self.global_env.define('yukarı_yuvarla', math.ceil)
        self.global_env.define('yukari_yuvarla', math.ceil)
        self.global_env.define('ebob', math.gcd)
        self.global_env.define('en_buyuk_ortak_bolen', math.gcd)
        self.global_env.define('pi_sayısı', math.pi)
        self.global_env.define('pi_sayisi', math.pi)
        
        # Register random direct calls
        self.global_env.define('ondalık_seç', random.random)
        self.global_env.define('ondalik_sec', random.random)
        self.global_env.define('tamsayı_seç', random.randint)
        self.global_env.define('tamsayi_sec', random.randint)
        self.global_env.define('aralıkta_seç', random.randrange)
        self.global_env.define('aralikta_sec', random.randrange)
        self.global_env.define('seç', random.choice)
        self.global_env.define('sec', random.choice)
        self.global_env.define('karıştır', random.shuffle)
        self.global_env.define('karistir', random.shuffle)
        self.global_env.define('örnek_seç', random.sample)
        self.global_env.define('ornek_sec', random.sample)
        
        # Register time direct calls
        self.global_env.define('bekle', time.sleep)
        self.global_env.define('yerel_zaman', time.localtime)
        self.global_env.define('tarih_saat', time.ctime)

    def eval(self, node, env):
        if isinstance(node, Program):
            for stmt in node.body:
                self.eval(stmt, env)
            return None
            
        elif isinstance(node, Ifade):
            return self.eval(node.expr, env)
            
        elif isinstance(node, Deger):
            return node.value
            
        elif isinstance(node, Degisken):
            return env.lookup(node.name, node.lineno)
            
        elif isinstance(node, Atama):
            val = self.eval(node.value, env)
            if isinstance(node.target, Degisken):
                env.assign(node.target.name, val, node.lineno, modifier=node.modifier)
            elif isinstance(node.target, Endeks):
                obj = self.eval(node.target.value, env)
                idx = self.eval(node.target.index, env)
                try:
                    obj[idx] = val
                except Exception as e:
                    raise OzdilError("Tür Hatası (TypeError)", f"Endeks ataması başarısız: {str(e)}", node.lineno)
            else:
                raise OzdilError("Yazım Hatası (SyntaxError)", "Geçersiz atama hedefi.", node.lineno)
            return val
            
        elif isinstance(node, Liste):
            return [self.eval(elt, env) for elt in node.elts]
            
        elif isinstance(node, Sozluk):
            keys = [self.eval(k, env) for k in node.keys]
            vals = [self.eval(v, env) for v in node.values]
            return dict(zip(keys, vals))
            
        elif isinstance(node, Endeks):
            obj = self.eval(node.value, env)
            idx = self.eval(node.index, env)
            try:
                return obj[idx]
            except Exception as e:
                raise OzdilError("Dizin Hatası (IndexError)", f"Sınır dışı erişim veya geçersiz anahtar: {str(e)}", node.lineno)
                
        elif isinstance(node, Nitelik):
            obj = self.eval(node.value, env)
            return get_attribute(obj, node.attr, node.lineno)
            
        elif isinstance(node, IkiliIslem):
            left_val = self.eval(node.left, env)
            
            if node.op == 'veya':
                return left_val or self.eval(node.right, env)
            if node.op == 've':
                return left_val and self.eval(node.right, env)
                
            right_val = self.eval(node.right, env)
            
            try:
                if node.op == '+': return left_val + right_val
                if node.op == '-': return left_val - right_val
                if node.op == '*': return left_val * right_val
                if node.op == '/': 
                    if right_val == 0:
                        raise OzdilError("Sıfıra Bölme Hatası (ZeroDivisionError)", "Bir sayı sıfıra bölünemez.", node.lineno)
                    return left_val / right_val
                if node.op == '%': return left_val % right_val
                if node.op == '**': return left_val ** right_val
                if node.op == '==': return left_val == right_val
                if node.op == '!=': return left_val != right_val
                if node.op == '<': return left_val < right_val
                if node.op == '>': return left_val > right_val
                if node.op == '<=': return left_val <= right_val
                if node.op == '>=': return left_val >= right_val
            except Exception as e:
                if isinstance(e, OzdilError):
                    raise e
                raise OzdilError("Tür Hatası (TypeError)", f"'{node.op}' işlemi için uyumsuz veri türleri ({type(left_val).__name__} ve {type(right_val).__name__})", node.lineno)
                
        elif isinstance(node, TekliIslem):
            operand_val = self.eval(node.operand, env)
            try:
                if node.op == '+': return +operand_val
                if node.op == '-': return -operand_val
                if node.op == 'değil': return not operand_val
            except Exception as e:
                raise OzdilError("Tür Hatası (TypeError)", f"'{node.op}' işlemi için uyumsuz veri türü ({type(operand_val).__name__})", node.lineno)
                
        elif isinstance(node, Cagir):
            func = self.eval(node.func, env)
            args = [self.eval(arg, env) for arg in node.args]
            if not callable(func):
                raise OzdilError("Tür Hatası (TypeError)", f"Nesne çağrılabilir bir işlem veya fonksiyon değil.", node.lineno)
            try:
                return func(*args)
            except ReturnException as r:
                return r.value
            except Exception as e:
                if isinstance(e, OzdilError):
                    raise e
                raise OzdilError("Yürütme Hatası (RuntimeError)", f"İşlem yürütülürken hata: {str(e)}", node.lineno)
                
        elif isinstance(node, Eger):
            test_val = self.eval(node.test, env)
            if test_val:
                for stmt in node.body:
                    self.eval(stmt, env)
            elif node.orelse:
                for stmt in node.orelse:
                    self.eval(stmt, env)
            return None
            
        elif isinstance(node, Iken):
            while self.eval(node.test, env):
                try:
                    for stmt in node.body:
                        self.eval(stmt, env)
                except BreakException:
                    break
                except ContinueException:
                    continue
            return None
            
        elif isinstance(node, Dongu):
            iter_val = self.eval(node.iter_expr, env)
            try:
                iterator = iter(iter_val)
            except TypeError:
                raise OzdilError("Tür Hatası (TypeError)", f"'{type(iter_val).__name__}' nesnesi üzerinde döngü kurulamaz.", node.lineno)
                
            for val in iterator:
                env.define(node.target.name, val)
                try:
                    for stmt in node.body:
                        self.eval(stmt, env)
                except BreakException:
                    break
                except ContinueException:
                    continue
            return None
            
        elif isinstance(node, Islem):
            def make_oz_func(fn_node, fn_env):
                def oz_func(*args):
                    if len(args) != len(fn_node.args):
                        raise OzdilError("Tür Hatası (TypeError)", f"'{fn_node.name}' işlemi {len(fn_node.args)} parametre bekliyor, fakat {len(args)} tane verildi.", fn_node.lineno)
                    local_env = Environment(fn_env)
                    for name, val in zip(fn_node.args, args):
                        local_env.define(name, val)
                    
                    try:
                        for stmt in fn_node.body:
                            self.eval(stmt, local_env)
                    except ReturnException as r:
                        return r.value
                    return None
                return oz_func
                
            env.define(node.name, make_oz_func(node, env))
            return None
            
        elif isinstance(node, Dondur):
            val = self.eval(node.value, env) if node.value else None
            raise ReturnException(val)
            
        elif isinstance(node, Getir):
            if node.name in ('matematik', 'math'):
                math_ns = {
                    'karekök': math.sqrt, 'karekok': math.sqrt,
                    'faktöriyel': math.factorial, 'faktoriyel': math.factorial,
                    'sinüs': math.sin, 'sinus': math.sin,
                    'kosinüs': math.cos, 'kosinus': math.cos,
                    'tanjant': math.tan, 'radyan': math.radians,
                    'derece': math.degrees, 'üs': math.pow, 'us': math.pow,
                    'mutlak': math.fabs, 'aşağı_yuvarla': math.floor, 'asagi_yuvarla': math.floor,
                    'yukarı_yuvarla': math.ceil, 'yukari_yuvarla': math.ceil,
                    'ebob': math.gcd, 'en_buyuk_ortak_bolen': math.gcd,
                    'pi_sayısı': math.pi, 'pi_sayisi': math.pi
                }
                env.define('matematik', math_ns)
            elif node.name in ('rastgele', 'random'):
                random_ns = {
                    'ondalık_seç': random.random, 'ondalik_sec': random.random,
                    'tamsayı_seç': random.randint, 'tamsayi_sec': random.randint,
                    'aralıkta_seç': random.randrange, 'aralikta_sec': random.randrange,
                    'seç': random.choice, 'sec': random.choice,
                    'karıştır': random.shuffle, 'karistir': random.shuffle,
                    'örnek_seç': random.sample, 'ornek_sec': random.sample
                }
                env.define('rastgele', random_ns)
            elif node.name in ('zaman', 'time'):
                time_ns = {
                    'bekle': time.sleep, 'yerel_zaman': time.localtime, 'tarih_saat': time.ctime
                }
                env.define('zaman', time_ns)
            else:
                try:
                    pkg_ns = load_external_package(node.name, node.lineno, self.stdout)
                    env.define(node.name, pkg_ns)
                    
                    # Kopya al: plugin_api tarafından kayıt edilmiş tüm fonksiyonları ve komutları global env alanına aktar
                    import ozdil.plugin_api
                    for func_name, func_obj in ozdil.plugin_api.plugin.functions.items():
                        env.define(func_name, func_obj)
                    for cmd_name, cmd_obj in ozdil.plugin_api.plugin.commands.items():
                        env.define(cmd_name, cmd_obj)
                        
                except OzdilError as oz_err:
                    raise oz_err
                except Exception as e:
                    raise OzdilError("Kütüphane Hatası (ImportError)", f"'{node.name}' kütüphanesi yüklenirken hata oluştu: {str(e)}", node.lineno)
            return None
            
        elif isinstance(node, DurNode):
            raise BreakException()
            
        elif isinstance(node, DevamEtNode):
            raise ContinueException()
            
        return None

# --- RUNNER ---

def run_code(custom_code):
    output = ""
    error = None
    ast_dict = None
    translated_tokens_str = ""
    
    import ozdil.plugin_api
    # Temizle ve sıfırla
    ozdil.plugin_api.plugin.clear()
    
    try:
        # Lexer
        tokens = lex_ozdil(custom_code)
        
        # Build friendly Lexer output for the "Sözcükler (Lexer)" tab
        token_lines = []
        for tok in tokens:
            token_lines.append(f"Satır {tok.lineno:2d}, Sütun {tok.col:2d} | Tür: {tok.type:<12} | Değer: {repr(tok.value)}")
        translated_tokens_str = "\n".join(token_lines)
        
        # Parser
        parser = Parser(tokens)
        ast_root = parser.parse_program()
        ast_dict = ast_root.to_dict()
        
        # Olay tetikle: program_basladi
        ozdil.plugin_api.plugin.trigger_event("program_basladi")
        
        # Interpreter VM
        interpreter = Interpreter()
        interpreter.eval(ast_root, interpreter.global_env)
        
        # Olay tetikle: program_bitti
        ozdil.plugin_api.plugin.trigger_event("program_bitti")
        
        output = "".join(interpreter.stdout)
        
    except IndentationError as ind_err:
        lines = custom_code.splitlines()
        tb = traceback.extract_tb(sys.exc_info()[2])
        lineno = tb[-1].lineno if tb else 1
        # Try to find the line number of indentation error
        for frame in tb:
            if frame.filename == "<string>" or frame.filename == "<kendi_dil>":
                lineno = frame.lineno
        err_line = lines[lineno - 1].strip() if 1 <= lineno <= len(lines) else "Bilinmiyor"
        error = (
            f"ÖzDil Çalışma Hatası (Girinti Hatası - IndentationError) 🚨\n"
            f"--------------------------------------------------\n"
            f"Açıklama  : Kod bloklarının hizalaması (girintisi) uyuşmuyor.\n"
            f"Satır     : {lineno}\n"
            f"--------------------------------------------------\n"
            f"Hatalı Kod: {err_line}"
        )
        ozdil.plugin_api.plugin.trigger_event("hata_olustu", error)
    except SyntaxError as syn_err:
        lines = custom_code.splitlines()
        # Retrieve actual or estimated lineno and col
        lineno = 1
        col = 1
        msg = str(syn_err)
        
        # Extract from syn_err tuple if present
        if len(syn_err.args) > 1 and isinstance(syn_err.args[1], tuple):
            lineno = syn_err.args[1][1] or 1
            col = syn_err.args[1][2] or 1
        else:
            # Fallback to scanning tokens
            if 'parser' in locals() and parser.tokens:
                curr_tok = parser.current()
                lineno = curr_tok.lineno
                col = curr_tok.col
                
        err_line = lines[lineno - 1].strip() if 1 <= lineno <= len(lines) else "Bilinmiyor"
        error = (
            f"ÖzDil Çalışma Hatası (Yazım Hatası - SyntaxError) 🚨\n"
            f"--------------------------------------------------\n"
            f"Açıklama  : {msg}\n"
            f"Satır     : {lineno}\n"
            f"Kolon     : {col}\n"
            f"--------------------------------------------------\n"
            f"Hatalı Kod: {err_line}"
        )
        ozdil.plugin_api.plugin.trigger_event("hata_olustu", error)
    except OzdilError as oz_err:
        lines = custom_code.splitlines()
        err_line = lines[oz_err.lineno - 1].strip() if 1 <= oz_err.lineno <= len(lines) else "Bilinmiyor"
        error = (
            f"ÖzDil Çalışma Hatası ({oz_err.friendly_type}) 🚨\n"
            f"--------------------------------------------------\n"
            f"Açıklama  : {oz_err.message}\n"
            f"Satır     : {oz_err.lineno}\n"
            f"--------------------------------------------------\n"
            f"Teknik Hata Detayı:\n"
            f"{oz_err.friendly_type}: {oz_err.message}\n"
            f"Hatalı Kod: {err_line}"
        )
        ozdil.plugin_api.plugin.trigger_event("hata_olustu", error)
    except Exception as e:
        tb = traceback.extract_tb(sys.exc_info()[2])
        lineno = tb[-1].lineno if tb else 1
        lines = custom_code.splitlines()
        err_line = lines[lineno - 1].strip() if 1 <= lineno <= len(lines) else "Bilinmiyor"
        error = (
            f"ÖzDil Çalışma Hatası (Beklenmeyen Hata) 🚨\n"
            f"--------------------------------------------------\n"
            f"Açıklama  : {str(e)}\n"
            f"Satır     : {lineno}\n"
            f"--------------------------------------------------\n"
            f"Hatalı Kod: {err_line}"
        )
        ozdil.plugin_api.plugin.trigger_event("hata_olustu", error)
        
    return {
        "translated": translated_tokens_str,
        "ast": ast_dict,
        "output": output,
        "error": error
    }

if __name__ == '__main__':
    input_data = sys.stdin.read()
    try:
        req = json.loads(input_data)
        code = req.get("code", "")
        result = run_code(code)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({
            "translated": "",
            "ast": None,
            "output": "",
            "error": f"Sistem Hatası: {str(e)}"
        }))
