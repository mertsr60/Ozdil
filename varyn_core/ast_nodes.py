# -*- coding: utf-8 -*-

class ASTNode:
    def __init__(self, lineno=1):
        self.lineno = lineno

    def to_dict(self):
        res = {"type": self.__class__.__name__, "lineno": self.lineno}
        for k, v in self.__dict__.items():
            if k == 'lineno':
                continue
            if isinstance(v, ASTNode):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if isinstance(x, ASTNode) else x for x in v]
            elif isinstance(v, tuple):
                res[k] = tuple(x.to_dict() if isinstance(x, ASTNode) else x for x in v)
            else:
                res[k] = v
        return res

class Program(ASTNode):
    def __init__(self, body, lineno=1):
        super().__init__(lineno)
        self.body = body

class Atama(ASTNode):
    def __init__(self, target, value, modifier=None, lineno=1):
        super().__init__(lineno)
        self.target = target
        self.value = value
        self.modifier = modifier

class Eger(ASTNode):
    def __init__(self, test, body, orelse=None, lineno=1):
        super().__init__(lineno)
        self.test = test
        self.body = body
        self.orelse = orelse if orelse is not None else []

class Iken(ASTNode):
    def __init__(self, test, body, lineno=1):
        super().__init__(lineno)
        self.test = test
        self.body = body

class Dongu(ASTNode):
    def __init__(self, target, iter_expr, body, lineno=1):
        super().__init__(lineno)
        self.target = target
        self.iter_expr = iter_expr
        self.body = body

class Islem(ASTNode):
    def __init__(self, name, args, body, lineno=1):
        super().__init__(lineno)
        self.name = name
        self.args = args
        self.body = body

class Dondur(ASTNode):
    def __init__(self, value=None, lineno=1):
        super().__init__(lineno)
        self.value = value

class Getir(ASTNode):
    def __init__(self, name, lineno=1):
        super().__init__(lineno)
        self.name = name

class IkiliIslem(ASTNode):
    def __init__(self, op, left, right, lineno=1):
        super().__init__(lineno)
        self.op = op
        self.left = left
        self.right = right

class TekliIslem(ASTNode):
    def __init__(self, op, operand, lineno=1):
        super().__init__(lineno)
        self.op = op
        self.operand = operand

class Degisken(ASTNode):
    def __init__(self, name, lineno=1):
        super().__init__(lineno)
        self.name = name

class Deger(ASTNode):
    def __init__(self, value, lineno=1):
        super().__init__(lineno)
        self.value = value

class Cagir(ASTNode):
    def __init__(self, func, args, lineno=1):
        super().__init__(lineno)
        self.func = func
        self.args = args

class Nitelik(ASTNode):
    def __init__(self, value, attr, lineno=1):
        super().__init__(lineno)
        self.value = value
        self.attr = attr

class Endeks(ASTNode):
    def __init__(self, value, index, lineno=1):
        super().__init__(lineno)
        self.value = value
        self.index = index

class Liste(ASTNode):
    def __init__(self, elts, lineno=1):
        super().__init__(lineno)
        self.elts = elts

class Sozluk(ASTNode):
    def __init__(self, keys, values, lineno=1):
        super().__init__(lineno)
        self.keys = keys
        self.values = values

class Ifade(ASTNode):
    def __init__(self, expr, lineno=1):
        super().__init__(lineno)
        self.expr = expr

class DurNode(ASTNode):
    def __init__(self, lineno=1):
        super().__init__(lineno)

class DevamEtNode(ASTNode):
    def __init__(self, lineno=1):
        super().__init__(lineno)

class Sinif(ASTNode):
    def __init__(self, name, body, lineno=1):
        super().__init__(lineno)
        self.name = name
        self.body = body

class Dene(ASTNode):
    def __init__(self, body, handlers, lineno=1):
        super().__init__(lineno)
        self.body = body
        self.handlers = handlers
