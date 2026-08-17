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
        return Token('EOF', '', len(self.tokens) + 1, 1)

    def peek(self, offset=1):
        if self.pos + offset < len(self.tokens):
            return self.tokens[self.pos + offset]
        return Token('EOF', '', len(self.tokens) + 1, 1)

    def consume(self, expected_type, expected_value=None):
        tok = self.current()
        if tok.type != expected_type:
            raise SyntaxError(f"Beklenen token türü: {expected_type}, fakat {tok.type} ({repr(tok.value)}) alındı. Satır: {tok.lineno}")
        if expected_value is not None:
            if isinstance(expected_value, (list, tuple, set)):
                if tok.value not in expected_value:
                    raise SyntaxError(f"Beklenen değerler: {expected_value}, fakat {repr(tok.value)} alındı. Satır: {tok.lineno}")
            elif tok.value != expected_value:
                raise SyntaxError(f"Beklenen değer: {expected_value}, fakat {repr(tok.value)} alındı. Satır: {tok.lineno}")
        self.pos += 1
        return tok

    def consume_id(self):
        tok = self.current()
        if tok.type in ('ID', 'KEYWORD'):
            self.pos += 1
            return Token('ID', tok.value, tok.lineno, tok.col)
        else:
            raise SyntaxError(f"Beklenen tanımlayıcı (ID), fakat {tok.type} ({repr(tok.value)}) alındı. Satır: {tok.lineno}")

    def consume_attr(self):
        tok = self.current()
        if tok.type in ('ID', 'KEYWORD'):
            self.pos += 1
            return Token('ID', tok.value, tok.lineno, tok.col)
        else:
            raise SyntaxError(f"Beklenen öznitelik adı, fakat {tok.type} ({repr(tok.value)}) alındı. Satır: {tok.lineno}")

    def match(self, expected_type, expected_value=None):
        tok = self.current()
        if tok.type != expected_type:
            return False
        if expected_value is not None:
            if isinstance(expected_value, (list, tuple, set)):
                if tok.value not in expected_value:
                    return False
            elif tok.value != expected_value:
                return False
        self.pos += 1
        return True

    def parse_program(self):
        body = []
        while self.pos < len(self.tokens) and self.current().type != 'EOF':
            if self.match('NEWLINE'):
                continue
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
        return Program(body, lineno=1)

    def parse_statement(self):
        tok = self.current()
        
        if self.match('KEYWORD', 'getir'):
            name_tok = self.consume_id()
            self.match('NEWLINE')
            return Getir(name_tok.value, lineno=tok.lineno)
            
        if self.match('KEYWORD', ('döndür', 'dondur')):
            val = None
            if self.current().type != 'NEWLINE':
                val = self.parse_expression()
            self.match('NEWLINE')
            return Dondur(val, lineno=tok.lineno)

        if self.match('KEYWORD', ('dur', 'break')):
            self.match('NEWLINE')
            return DurNode(lineno=tok.lineno)

        if self.match('KEYWORD', ('devam_et', 'continue')):
            self.match('NEWLINE')
            return DevamEtNode(lineno=tok.lineno)

        if self.match('KEYWORD', ('eğer', 'eger')):
            return self.parse_eger_statement(tok)

        if self.match('KEYWORD', 'iken'):
            test = self.parse_expression()
            self.consume('OP', ':')
            self.match('NEWLINE')
            body = self.parse_block()
            return Iken(test, body, lineno=tok.lineno)

        if self.match('KEYWORD', ('döngü', 'dongu', 'her')):
            target_var = Degisken(self.consume_id().value, lineno=self.current().lineno)
            self.consume('KEYWORD', ('içinde', 'icinde', 'in'))
            iter_expr = self.parse_expression()
            self.consume('OP', ':')
            self.match('NEWLINE')
            body = self.parse_block()
            return Dongu(target_var, iter_expr, body, lineno=tok.lineno)

        if self.match('KEYWORD', ('işlem', 'islem', 'fonksiyon')):
            name = self.consume_id().value
            self.consume('OP', '(')
            args = []
            if not self.match('OP', ')'):
                args.append(self.consume_id().value)
                while self.match('OP', ','):
                    args.append(self.consume_id().value)
                self.consume('OP', ')')
            self.consume('OP', ':')
            self.match('NEWLINE')
            body = self.parse_block()
            return Islem(name, args, body, lineno=tok.lineno)

        if self.match('KEYWORD', ('sınıf', 'sinif', 'class')):
            name = self.consume_id().value
            self.consume('OP', ':')
            self.match('NEWLINE')
            body = self.parse_block()
            return Sinif(name, body, lineno=tok.lineno)

        if self.match('KEYWORD', ('dene', 'try')):
            self.consume('OP', ':')
            self.match('NEWLINE')
            body = self.parse_block()
            handlers = []
            while self.current().type != 'EOF' and self.current().value in ('except', 'hata_yakala', 'yakala'):
                self.pos += 1
                err_type = None
                err_var = None
                if self.current().type in ('ID', 'KEYWORD'):
                    err_type = self.consume_id().value
                    if self.match('KEYWORD', ('olarak', 'as')):
                        err_var = self.consume_id().value
                self.consume('OP', ':')
                self.match('NEWLINE')
                handler_body = self.parse_block()
                handlers.append((err_type, err_var, handler_body))
            return Dene(body, handlers, lineno=tok.lineno)

        if self.match('KEYWORD', ('değişken', 'degisken', 'sabit', 'tam_sayı', 'tam_sayi', 'ondalık', 'ondalik', 'metin', 'liste', 'sözlük', 'sozluk')):
            modifier = tok.value
            target = Degisken(self.consume_id().value, lineno=self.current().lineno)
            self.consume('OP', '=')
            val = self.parse_expression()
            self.match('NEWLINE')
            return Atama(target, val, modifier, lineno=tok.lineno)

        expr = self.parse_expression()
        if isinstance(expr, (Degisken, Endeks, Nitelik)) and self.match('OP', '='):
            val = self.parse_expression()
            self.match('NEWLINE')
            return Atama(expr, val, None, lineno=tok.lineno)
            
        self.match('NEWLINE')
        return Ifade(expr, lineno=tok.lineno)

    def parse_eger_statement(self, first_tok):
        test = self.parse_expression()
        self.consume('OP', ':')
        self.match('NEWLINE')
        body = self.parse_block()
        
        orelse = []
        if self.current().type != 'EOF' and self.current().value in ('değişken_eğer', 'degilse_eger', 'değilse_eğer', 'degilse_eğer', 'değilse_eger'):
            elif_tok = self.current()
            self.pos += 1
            elif_node = self.parse_eger_statement(elif_tok)
            orelse = [elif_node]
        elif self.match('KEYWORD', ('değilse', 'degilse')):
            self.consume('OP', ':')
            self.match('NEWLINE')
            orelse = self.parse_block()
            
        return Eger(test, body, orelse, lineno=first_tok.lineno)

    def parse_block(self):
        self.consume('INDENT')
        body = []
        while self.current().type != 'EOF' and self.current().type != 'DEDENT':
            if self.match('NEWLINE'):
                continue
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
        self.consume('DEDENT')
        return body

    def parse_expression(self):
        return self.parse_logical_or()

    def parse_logical_or(self):
        node = self.parse_logical_and()
        while self.current().type != 'EOF' and self.current().value in ('veya', 'or'):
            op = self.current().value
            self.pos += 1
            right = self.parse_logical_and()
            node = IkiliIslem(op, node, right, lineno=node.lineno)
        return node

    def parse_logical_and(self):
        node = self.parse_equality()
        while self.current().type != 'EOF' and self.current().value in ('ve', 'and'):
            op = self.current().value
            self.pos += 1
            right = self.parse_equality()
            node = IkiliIslem(op, node, right, lineno=node.lineno)
        return node

    def parse_equality(self):
        node = self.parse_comparison()
        while self.current().type == 'OP' and self.current().value in ('==', '!='):
            op = self.current().value
            self.pos += 1
            right = self.parse_comparison()
            node = IkiliIslem(op, node, right, lineno=node.lineno)
        return node

    def parse_comparison(self):
        node = self.parse_term()
        while (self.current().type == 'OP' and self.current().value in ('<', '>', '<=', '>=')) or (self.current().type == 'KEYWORD' and self.current().value in ('içinde', 'icinde', 'in')):
            op = self.current().value
            self.pos += 1
            right = self.parse_term()
            node = IkiliIslem(op, node, right, lineno=node.lineno)
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.current().type == 'OP' and self.current().value in ('+', '-'):
            op = self.current().value
            self.pos += 1
            right = self.parse_factor()
            node = IkiliIslem(op, node, right, lineno=node.lineno)
        return node

    def parse_factor(self):
        node = self.parse_exponent()
        while self.current().type == 'OP' and self.current().value in ('*', '/', '%'):
            op = self.current().value
            self.pos += 1
            right = self.parse_exponent()
            node = IkiliIslem(op, node, right, lineno=node.lineno)
        return node

    def parse_exponent(self):
        node = self.parse_unary()
        while self.current().type == 'OP' and self.current().value == '**':
            op = self.current().value
            self.pos += 1
            right = self.parse_unary()
            node = IkiliIslem(op, node, right, lineno=node.lineno)
        return node

    def parse_unary(self):
        if self.current().type == 'OP' and self.current().value in ('+', '-'):
            op = self.current().value
            self.pos += 1
            operand = self.parse_unary()
            return TekliIslem(op, operand, lineno=operand.lineno)
        if self.current().type == 'KEYWORD' and self.current().value in ('değil', 'degil', 'not'):
            op = self.current().value
            self.pos += 1
            operand = self.parse_unary()
            return TekliIslem(op, operand, lineno=operand.lineno)
        return self.parse_call_or_member()

    def parse_call_or_member(self):
        node = self.parse_primary()
        while True:
            if self.match('OP', '('):
                args = []
                if not self.match('OP', ')'):
                    args.append(self.parse_expression())
                    while self.match('OP', ','):
                        args.append(self.parse_expression())
                    self.consume('OP', ')')
                node = Cagir(node, args, lineno=node.lineno)
            elif self.match('OP', '.'):
                attr_name = self.consume_attr().value
                node = Nitelik(node, attr_name, lineno=node.lineno)
            elif self.match('OP', '['):
                index_expr = self.parse_expression()
                self.consume('OP', ']')
                node = Endeks(node, index_expr, lineno=node.lineno)
            else:
                break
        return node

    def parse_primary(self):
        tok = self.current()
        
        if self.match('NUM_INT'):
            return Deger(int(tok.value), lineno=tok.lineno)
        if self.match('NUM_FLOAT'):
            return Deger(float(tok.value), lineno=tok.lineno)
            
        if self.match('STRING'):
            from .lexer import decode_string_literal
            val = decode_string_literal(tok.value)
            return Deger(val, lineno=tok.lineno)
            
        if self.match('KEYWORD', ('doğru', 'dogru')):
            return Deger(True, lineno=tok.lineno)
        if self.match('KEYWORD', ('yanlış', 'yanlis')):
            return Deger(False, lineno=tok.lineno)
        if self.match('KEYWORD', ('yok', 'boş', 'bos')):
            return Deger(None, lineno=tok.lineno)
            
        if self.current().type == 'ID' or (self.current().type == 'KEYWORD' and self.current().value in ('değişken', 'degisken', 'sabit', 'tam_sayı', 'tam_sayi', 'ondalık', 'ondalik', 'metin', 'liste', 'sözlük', 'sozluk')):
            tok = self.consume_id()
            return Degisken(tok.value, lineno=tok.lineno)
            
        if self.match('OP', '('):
            expr = self.parse_expression()
            self.consume('OP', ')')
            return expr
            
        if self.match('OP', '['):
            elts = []
            if not self.match('OP', ']'):
                elts.append(self.parse_expression())
                while self.match('OP', ','):
                    elts.append(self.parse_expression())
                self.consume('OP', ']')
            return Liste(elts, lineno=tok.lineno)
            
        if self.match('OP', '{'):
            keys = []
            values = []
            if not self.match('OP', '}'):
                keys.append(self.parse_expression())
                self.consume('OP', ':')
                values.append(self.parse_expression())
                while self.match('OP', ','):
                    keys.append(self.parse_expression())
                    self.consume('OP', ':')
                    values.append(self.parse_expression())
                self.consume('OP', '}')
            return Sozluk(keys, values, lineno=tok.lineno)
            
        raise SyntaxError(f"Beklenmedik ifade başlangıcı: '{tok.value}' (tür: {tok.type}) Satır: {tok.lineno}")
