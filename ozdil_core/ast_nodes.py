# -*- coding: utf-8 -*-

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
            "işlenen": self.operand.to_dict()
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
            "parametreler": [arg.to_dict() for arg in self.args]
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
            "type": "Endeks",
            "lineno": self.lineno,
            "değer": self.value.to_dict(),
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
            "elemanlar": [elt.to_dict() for elt in self.elts]
        }

class Sozluk(ASTNode):
    def __init__(self, keys, values, lineno):
        self.keys = keys
        self.values = values
        self.lineno = lineno
    def to_dict(self):
        return {
            "type": "Sözlük",
            "lineno": self.lineno,
            "anahtarlar": [k.to_dict() for k in self.keys],
            "değerler": [v.to_dict() for v in self.values]
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
        return {
            "type": "Dur (Break)",
            "lineno": self.lineno
        }

class DevamEtNode(ASTNode):
    def __init__(self, lineno):
        self.lineno = lineno
    def to_dict(self):
        return {
            "type": "DevamEt (Continue)",
            "lineno": self.lineno
        }

class Sinif(ASTNode):
    def __init__(self, name, body, lineno):
        self.name = name
        self.body = body
        self.lineno = lineno
    def to_dict(self):
        return {
            "type": "Sinif (Sınıf)",
            "lineno": self.lineno,
            "ad": self.name,
            "gövde": [node.to_dict() for node in self.body]
        }

class Dene(ASTNode):
    def __init__(self, body, handlers, lineno):
        self.body = body
        self.handlers = handlers  # list of (err_type_name, err_var_name, body_nodes)
        self.lineno = lineno
    def to_dict(self):
        return {
            "type": "Dene (Hata Yakalama)",
            "lineno": self.lineno,
            "gövde": [node.to_dict() for node in self.body],
            "hata_yakalayıcılar": [
                {
                    "hata_türü": h[0],
                    "takma_ad": h[1],
                    "gövde": [node.to_dict() for node in h[2]]
                } for h in self.handlers
            ]
        }
