# -*- coding: utf-8 -*-
import sys
import os
import json
import zipfile

# The code for ozdil.py runner
OZDIL_RUNNER_CONTENT = """# -*- coding: utf-8 -*-
\"\"\"
ÖzDil - Türkçe Programlama Dili Yerel ve Çevrimdışı Çalıştırıcısı
Kullanım: python3 ozdil.py <dosya_adi.oz>
\"\"\"
import sys
import os
import math
import random
import time

class OzdilError(Exception):
    def __init__(self, friendly_type, message, lineno):
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
            break
            
        # Numbers
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
            
        # Identifiers & Keywords
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
                'metin', 'liste', 'sözlük', 'sozluk'
            )
            if val in keywords_list:
                tokens.append(Token('KEYWORD', val, lineno, start_col))
            else:
                tokens.append(Token('ID', val, lineno, start_col))
            continue
            
        # Operators
        if i + 1 < n and line_str[i:i+2] in ('==', '!=', '<=', '>=', '**'):
            tokens.append(Token('OP', line_str[i:i+2], lineno, i + 1))
            i += 2
            continue
            
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
        stripped = line.rstrip()
        
        if not stripped.strip() or stripped.strip().startswith('#'):
            continue
            
        indent_level = 0
        for char in line:
            if char == ' ':
                indent_level += 1
            elif char == '\t':
                indent_level += 4
            else:
                break
                
        line_tokens = tokenize_line(stripped[indent_level:], lineno)
        if not line_tokens:
            continue
            
        if indent_level > indent_stack[-1]:
            indent_stack.append(indent_level)
            all_tokens.append(Token('INDENT', '    ', lineno, 1))
        elif indent_level < indent_stack[-1]:
            while indent_level < indent_stack[-1]:
                indent_stack.pop()
                all_tokens.append(Token('DEDENT', '', lineno, 1))
            if indent_level != indent_stack[-1]:
                raise IndentationError("Girinti düzeyleri eşleşmiyor.")
                
        all_tokens.extend(line_tokens)
        all_tokens.append(Token('NEWLINE', '\\n', lineno, len(line) + 1))
        
    while len(indent_stack) > 1:
        indent_stack.pop()
        all_tokens.append(Token('DEDENT', '', len(lines), 1))
        
    return all_tokens

# --- AST CLASSES ---

class ASTNode:
    pass

class Program(ASTNode):
    def __init__(self, body):
        self.body = body

class Atama(ASTNode):
    def __init__(self, target, value, lineno):
        self.target = target
        self.value = value
        self.lineno = lineno

class Eger(ASTNode):
    def __init__(self, test, body, orelse, lineno):
        self.test = test
        self.body = body
        self.orelse = orelse
        self.lineno = lineno

class Iken(ASTNode):
    def __init__(self, test, body, lineno):
        self.test = test
        self.body = body
        self.lineno = lineno

class Dongu(ASTNode):
    def __init__(self, target, iter_expr, body, lineno):
        self.target = target
        self.iter_expr = iter_expr
        self.body = body
        self.lineno = lineno

class Islem(ASTNode):
    def __init__(self, name, args, body, lineno):
        self.name = name
        self.args = args
        self.body = body
        self.lineno = lineno

class Dondur(ASTNode):
    def __init__(self, value, lineno):
        self.value = value
        self.lineno = lineno

class Getir(ASTNode):
    def __init__(self, name, lineno):
        self.name = name
        self.lineno = lineno

class IkiliIslem(ASTNode):
    def __init__(self, op, left, right, lineno):
        self.op = op
        self.left = left
        self.right = right
        self.lineno = lineno

class TekliIslem(ASTNode):
    def __init__(self, op, operand, lineno):
        self.op = op
        self.operand = operand
        self.lineno = lineno

class Degisken(ASTNode):
    def __init__(self, name, lineno):
        self.name = name
        self.lineno = lineno

class Deger(ASTNode):
    def __init__(self, value, lineno):
        self.value = value
        self.lineno = lineno

class Cagir(ASTNode):
    def __init__(self, func, args, lineno):
        self.func = func
        self.args = args
        self.lineno = lineno

class Nitelik(ASTNode):
    def __init__(self, value, attr, lineno):
        self.value = value
        self.attr = attr
        self.lineno = lineno

class Endeks(ASTNode):
    def __init__(self, value, index, lineno):
        self.value = value
        self.index = index
        self.lineno = lineno

class Liste(ASTNode):
    def __init__(self, elts, lineno):
        self.elts = elts
        self.lineno = lineno

class Sozluk(ASTNode):
    def __init__(self, keys, values, lineno):
        self.keys = keys
        self.values = values
        self.lineno = lineno

class Ifade(ASTNode):
    def __init__(self, expr, lineno):
        self.expr = expr
        self.lineno = lineno

class DurNode(ASTNode):
    def __init__(self, lineno):
        self.lineno = lineno

class DevamEtNode(ASTNode):
    def __init__(self, lineno):
        self.lineno = lineno

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
        
        orelse = []
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
            orelse = [Eger(elif_test, elif_body, [], elif_tok.lineno)]
            
        if self.current().type == 'KEYWORD' and self.current().value in ('değilse', 'degilse'):
            self.eat('KEYWORD')
            self.eat('OP', ':')
            self.eat('NEWLINE')
            self.eat('INDENT')
            else_body = []
            while self.current().type != 'DEDENT' and self.current().type != 'EOF':
                while self.current().type == 'NEWLINE':
                    self.eat('NEWLINE')
                if self.current().type in ('DEDENT', 'EOF'):
                    break
                else_body.append(self.parse_statement())
            self.eat('DEDENT')
            if orelse:
                orelse[0].orelse = else_body
            else:
                orelse = else_body
                
        return Eger(test, body, orelse, tok.lineno)
        
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
        
        self.eat('KEYWORD')
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
            self.eat('KEYWORD')
            target_tok = self.eat('ID')
            target = Degisken(target_tok.value, target_tok.lineno)
            self.eat('OP', '=')
            value = self.parse_expression()
            self.expect_statement_end()
            return Atama(target, value, curr.lineno)
            
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
        while self.current().type == 'OP' and self.current().value == '**':
            op_tok = self.eat('OP')
            right = self.parse_unary()
            node = IkiliIslem('**', node, right, op_tok.lineno)
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
            val = val.replace('\\\\n', '\\n').replace('\\\\t', '\\t').replace('\\\\"', '"').replace("\\\\'", "'")
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
        self.parent = parent
        
    def define(self, name, value):
        self.values[name] = value
        
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
        
    def assign(self, name, value, lineno):
        if name in self.values:
            self.values[name] = value
            return
        if self.parent:
            self.parent.assign(name, value, lineno)
            return
        self.values[name] = value

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class BreakException(Exception):
    pass

class ContinueException(Exception):
    pass

def get_attribute(obj, attr, lineno):
    if isinstance(obj, list):
        if attr in ('ekle', 'append'): return obj.append
        if attr in ('çıkar', 'cikar', 'remove'): return obj.remove
        if attr in ('temizle', 'clear'): return obj.clear
        if attr in ('uzunluk', 'len'): return lambda: len(obj)
    elif isinstance(obj, dict):
        if attr in ('anahtarlar', 'keys'): return lambda: list(obj.keys())
        if attr in ('değerler', 'degerler', 'values'): return lambda: list(obj.values())
        if attr in ('temizle', 'clear'): return obj.clear
    elif isinstance(obj, str):
        if attr in ('büyük_harf', 'buyuk_harf', 'upper'): return obj.upper
        if attr in ('küçük_harf', 'kucuk_harf', 'lower'): return obj.lower
            
    if isinstance(obj, dict) and attr in obj:
        return obj[attr]
        
    if hasattr(obj, attr):
        return getattr(obj, attr)
        
    raise OzdilError(
        "Öznitelik Hatası (AttributeError)",
        f"'{type(obj).__name__}' nesnesinin '{attr}' adında bir özelliği veya fonksiyonu yok.",
        lineno
    )

class Interpreter:
    def __init__(self):
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
            print(text)
            
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
                env.assign(node.target.name, val, node.lineno)
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
            def oz_func(*args):
                if len(args) != len(node.args):
                    raise OzdilError("Tür Hatası (TypeError)", f"'{node.name}' işlemi {len(node.args)} parametre bekliyor, fakat {len(args)} tane verildi.", node.lineno)
                local_env = Environment(env)
                for name, val in zip(node.args, args):
                    local_env.define(name, val)
                
                for stmt in node.body:
                    self.eval(stmt, local_env)
                return None
                
            env.define(node.name, oz_func)
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
                raise OzdilError("Kütüphane Hatası (ImportError)", f"'{node.name}' kütüphanesi bulunamadı.", node.lineno)
            return None
            
        elif isinstance(node, DurNode):
            raise BreakException()
            
        elif isinstance(node, DevamEtNode):
            raise ContinueException()
            
        return None

def main():
    if len(sys.argv) < 2:
        print("Kullanım: python3 ozdil.py <dosya_adi.oz>")
        print("Örnek: python3 ozdil.py kodumuz.oz")
        sys.exit(1)
    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"Hata: '{filepath}' dosyası bulunamadı!")
        sys.exit(1)
    with open(filepath, 'r', encoding='utf-8') as f:
        custom_code = f.read()
        
    try:
        tokens = lex_ozdil(custom_code)
        parser = Parser(tokens)
        ast_root = parser.parse_program()
        
        interpreter = Interpreter()
        interpreter.eval(ast_root, interpreter.global_env)
        
    except IndentationError as ind_err:
        lines = custom_code.splitlines()
        tb = traceback.extract_tb(sys.exc_info()[2])
        lineno = tb[-1].lineno if tb else 1
        for frame in tb:
            if frame.filename == filepath:
                lineno = frame.lineno
        err_line = lines[lineno - 1].strip() if 1 <= lineno <= len(lines) else "Bilinmiyor"
        print(f"\\nÖzDil Çalışma Hatası (Girinti Hatası - IndentationError) \\u26a1")
        print("--------------------------------------------------")
        print("Açıklama  : Kod bloklarının hizalaması (girintisi) uyuşmuyor.")
        print(f"Satır     : {lineno}")
        print("--------------------------------------------------")
        print(f"Hatalı Kod: {err_line}")
    except SyntaxError as syn_err:
        lines = custom_code.splitlines()
        lineno = 1
        col = 1
        msg = str(syn_err)
        if len(syn_err.args) > 1 and isinstance(syn_err.args[1], tuple):
            lineno = syn_err.args[1][1] or 1
            col = syn_err.args[1][2] or 1
        else:
            if 'parser' in locals() and parser.tokens:
                curr_tok = parser.current()
                lineno = curr_tok.lineno
                col = curr_tok.col
        err_line = lines[lineno - 1].strip() if 1 <= lineno <= len(lines) else "Bilinmiyor"
        print(f"\\nÖzDil Çalışma Hatası (Yazım Hatası - SyntaxError) \\u26a1")
        print("--------------------------------------------------")
        print(f"Açıklama  : {msg}")
        print(f"Satır     : {lineno}")
        print(f"Kolon     : {col}")
        print("--------------------------------------------------")
        print(f"Hatalı Kod: {err_line}")
    except OzdilError as oz_err:
        lines = custom_code.splitlines()
        err_line = lines[oz_err.lineno - 1].strip() if 1 <= oz_err.lineno <= len(lines) else "Bilinmiyor"
        print(f"\\nÖzDil Çalışma Hatası ({oz_err.friendly_type}) \\u26a1")
        print("--------------------------------------------------")
        print(f"Açıklama  : {oz_err.message}")
        print(f"Satır     : {oz_err.lineno}")
        print("--------------------------------------------------")
        print("Teknik Hata Detayı:")
        print(f"{oz_err.friendly_type}: {oz_err.message}")
        print(f"Hatalı Kod: {err_line}")
    except Exception as e:
        tb = traceback.extract_tb(sys.exc_info()[2])
        lineno = tb[-1].lineno if tb else 1
        lines = custom_code.splitlines()
        err_line = lines[lineno - 1].strip() if 1 <= lineno <= len(lines) else "Bilinmiyor"
        print(f"\\nÖzDil Çalışma Hatası (Beklenmeyen Hata) \\u26a1")
        print("--------------------------------------------------")
        print(f"Açıklama  : {str(e)}")
        print(f"Satır     : {lineno}")
        print("--------------------------------------------------")
        print(f"Hatalı Kod: {err_line}")

if __name__ == '__main__':
    main()
"""

README_CONTENT = """# ÖzDil - Türkçe Programlama Dili (Yerel / Çevrimdışı Çalıştırıcı)

Tebrikler! ÖzDil projenizi başarıyla yerel cihazınıza dışa aktardınız.
Artık ÖzDil kodlarınızı bilgisayarınızda, sunucunuzda veya Android cihazınızda (Termux) çalıştırabilirsiniz!

## Dosya Yapısı

- `ozdil.py`: ÖzDil kodlarını doğrudan sözcük çözücü ve AST yorumlayıcı ile koşturan yerel ÖzDil VM motoru.
- `kodumuz.oz`: Siteden indirdiğiniz kendi özel kodunuz.
- `README.md`: Bu bilgilendirme dosyası.

## Kurulum ve Çalıştırma

ÖzDil'i çalıştırmak için bilgisayarınızda veya telefonunuzda **Python 3** kurulu olmalıdır.

### 1. Bilgisayarda Çalıştırma (Windows / MacOS / Linux)

Terminali veya Komut İstemi'ni (CMD) açın, bu dosyaların olduğu klasöre gidin ve şu komutu yazın:

```bash
python3 ozdil.py kodumuz.oz
```

*(Windows kullanıyorsanız `python` veya `py` yazmanız gerekebilir):*
```cmd
python ozdil.py kodumuz.oz
```

---

### 2. Mobilde / Android'de Çalıştırma (Termux)

Android telefonunuzda kodlarınızı çalıştırmak için **Termux** uygulamasını kullanabilirsiniz:

1. Termux uygulamasını açın.
2. Gerekli paketleri ve Python'u kurun:
   ```bash
   pkg update && pkg upgrade
   pkg install python
   ```
3. Dosyaların bulunduğu dizine gidin (örneğin telefon hafızasındaki Download klasörü):
   ```bash
   termux-setup-storage
   cd /sdcard/Download
   ```
4. Kodunuzu çalıştırın:
   ```bash
   python3 ozdil.py kodumuz.oz
   ```

## Kendi Dosyalarınızı Yazın

Yeni bir dosya oluşturup (örn: `hesapla.oz`) içine Türkçe ÖzDil kodlarınızı yazıp çalıştırabilirsiniz:
```bash
python3 ozdil.py hesapla.oz
```

İyi kodlamalar!
"""

def main():
    try:
        input_data = sys.stdin.read()
        req = json.loads(input_data)
        user_code = req.get("code", "")
        
        # We will create a zip file on disk
        zip_filename = "ozdil_projesi.zip"
        
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.writestr("ozdil.py", OZDIL_RUNNER_CONTENT)
            zipf.writestr("kodumuz.oz", user_code)
            zipf.writestr("README.md", README_CONTENT)
            
        print(json.dumps({"success": True, "filename": zip_filename}))
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))

if __name__ == '__main__':
    main()
