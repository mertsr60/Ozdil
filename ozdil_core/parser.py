# -*- coding: utf-8 -*-
from .tokens import Token
from .ast_nodes import (
    Program, Atama, Eger, Iken, Dongu, Islem, Dondur, Getir,
    IkiliIslem, TekliIslem, Degisken, Deger, Cagir, Nitelik,
    Endeks, Liste, Sozluk, Ifade, DurNode, DevamEtNode, Sinif, Dene
)

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
        
    def skip_newlines_and_indents(self):
        while self.current().type in ('NEWLINE', 'INDENT', 'DEDENT'):
            self.pos += 1
            
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
            elif curr.value in ('sinif', 'sınıf', 'class'):
                return self.parse_sinif()
            elif curr.value in ('dene', 'try'):
                return self.parse_dene()
                
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
                self.eat('OP', ',')
                if self.current().type == 'OP' and self.current().value == ')':
                    break
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

    def parse_sinif(self):
        tok = self.eat('KEYWORD')
        name_tok = self.eat('ID')
        name = name_tok.value
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
        return Sinif(name, body, tok.lineno)

    def parse_dene(self):
        tok = self.eat('KEYWORD')
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
        
        handlers = []
        while self.current().type == 'KEYWORD' and self.current().value in ('hata_yakala', 'except'):
            handler_tok = self.eat('KEYWORD')
            err_type = None
            err_var = None
            
            if self.current().type == 'ID':
                err_type_tok = self.eat('ID')
                err_type = err_type_tok.value
                
                if self.current().type == 'KEYWORD' and self.current().value in ('olarak', 'as'):
                    self.eat('KEYWORD')
                    err_var_tok = self.eat('ID')
                    err_var = err_var_tok.value
                    
            self.eat('OP', ':')
            self.eat('NEWLINE')
            self.eat('INDENT')
            handler_body = []
            while self.current().type != 'DEDENT' and self.current().type != 'EOF':
                while self.current().type == 'NEWLINE':
                    self.eat('NEWLINE')
                if self.current().type in ('DEDENT', 'EOF'):
                    break
                handler_body.append(self.parse_statement())
            self.eat('DEDENT')
            handlers.append((err_type, err_var, handler_body))
            
        return Dene(body, handlers, tok.lineno)

    def parse_atama_or_expr(self):
        curr = self.current()
        type_modifiers = (
            'değişken', 'degisken', 'sabit', 
            'tam_sayı', 'tam_sayi', 'ondalık', 'ondalik', 
            'metin', 'liste', 'sözlük', 'sozluk'
        )
        if curr.type == 'KEYWORD' and curr.value in type_modifiers:
            allowed_keyword_ids = ('tam_sayı', 'tam_sayi', 'ondalık', 'ondalik', 'metin', 'liste', 'sözlük', 'sozluk')
            next_tok = self.peek()
            if next_tok.type == 'ID' or (next_tok.type == 'KEYWORD' and next_tok.value in allowed_keyword_ids):
                mod_tok = self.eat('KEYWORD')
                target_tok = self.current()
                if target_tok.type == 'ID':
                    self.eat('ID')
                else:
                    self.eat('KEYWORD')
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
                self.eat('OP', '(')
                self.skip_newlines_and_indents()
                args = []
                if self.current().type != 'OP' or self.current().value != ')':
                    args.append(self.parse_expression())
                    self.skip_newlines_and_indents()
                    while self.current().type == 'OP' and self.current().value == ',':
                        self.eat('OP', ',')
                        self.skip_newlines_and_indents()
                        if self.current().type == 'OP' and self.current().value == ')':
                            break
                        args.append(self.parse_expression())
                        self.skip_newlines_and_indents()
                self.eat('OP', ')')
                node = Cagir(node, args, curr.lineno)
            elif curr.type == 'OP' and curr.value == '[':
                self.eat('OP', '[')
                self.skip_newlines_and_indents()
                index_expr = self.parse_expression()
                self.skip_newlines_and_indents()
                self.eat('OP', ']')
                node = Endeks(node, index_expr, curr.lineno)
            elif curr.type == 'OP' and curr.value == '.':
                self.eat('OP', '.')
                tok = self.current()
                if tok.type in ('ID', 'KEYWORD'):
                    self.pos += 1
                    attr_tok = tok
                else:
                    raise SyntaxError(f"Yazım hatası: Beklenen ID, fakat '{tok.value}' bulundu.")
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
            import ast
            try:
                val = ast.literal_eval(tok.value)
            except Exception:
                # Robust fallback
                val = tok.value[1:-1].replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"').replace("\\'", "'").replace('\\\\', '\\')
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
        elif tok.type == 'KEYWORD' and tok.value in ('tam_sayı', 'tam_sayi', 'ondalık', 'ondalik', 'metin', 'liste', 'sözlük', 'sozluk'):
            self.eat('KEYWORD')
            return Degisken(tok.value, tok.lineno)
        elif tok.type == 'ID':
            self.eat('ID')
            return Degisken(tok.value, tok.lineno)
        elif tok.type == 'OP' and tok.value == '(':
            self.eat('OP', '(')
            self.skip_newlines_and_indents()
            expr = self.parse_expression()
            self.skip_newlines_and_indents()
            self.eat('OP', ')')
            return expr
        elif tok.type == 'OP' and tok.value == '[':
            self.eat('OP', '[')
            self.skip_newlines_and_indents()
            elts = []
            if self.current().type != 'OP' or self.current().value != ']':
                elts.append(self.parse_expression())
                self.skip_newlines_and_indents()
                while self.current().type == 'OP' and self.current().value == ',':
                    self.eat('OP', ',')
                    self.skip_newlines_and_indents()
                    if self.current().type == 'OP' and self.current().value == ']':
                        break
                    elts.append(self.parse_expression())
                    self.skip_newlines_and_indents()
            self.eat('OP', ']')
            return Liste(elts, tok.lineno)
        elif tok.type == 'OP' and tok.value == '{':
            self.eat('OP', '{')
            self.skip_newlines_and_indents()
            keys = []
            values = []
            if self.current().type != 'OP' or self.current().value != '}':
                keys.append(self.parse_expression())
                self.skip_newlines_and_indents()
                self.eat('OP', ':')
                self.skip_newlines_and_indents()
                values.append(self.parse_expression())
                self.skip_newlines_and_indents()
                while self.current().type == 'OP' and self.current().value == ',':
                    self.eat('OP', ',')
                    self.skip_newlines_and_indents()
                    if self.current().type == 'OP' and self.current().value == '}':
                        break
                    keys.append(self.parse_expression())
                    self.skip_newlines_and_indents()
                    self.eat('OP', ':')
                    self.skip_newlines_and_indents()
                    values.append(self.parse_expression())
                    self.skip_newlines_and_indents()
            self.eat('OP', '}')
            return Sozluk(keys, values, tok.lineno)
        else:
            raise SyntaxError(f"Geçersiz sözdizimi: '{tok.value}'")
