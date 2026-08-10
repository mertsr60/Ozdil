# -*- coding: utf-8 -*-
from .errors import OzdilError, ReturnException

class OzValue:
    def to_native(self):
        raise NotImplementedError()
    def get_type_name(self):
        raise NotImplementedError()
    def __repr__(self):
        raise NotImplementedError()

class OzNull(OzValue):
    def to_native(self):
        return None
    def get_type_name(self):
        return "Boş"
    def __repr__(self):
        return "boş"

class OzBool(OzValue):
    def __init__(self, val):
        self.val = bool(val)
    def to_native(self):
        return self.val
    def get_type_name(self):
        return "Mantıksal"
    def __repr__(self):
        return "doğru" if self.val else "yanlış"

class OzInt(OzValue):
    def __init__(self, val):
        self.val = int(val)
    def to_native(self):
        return self.val
    def get_type_name(self):
        return "Sayı"
    def __repr__(self):
        return str(self.val)

class OzFloat(OzValue):
    def __init__(self, val):
        self.val = float(val)
    def to_native(self):
        return self.val
    def get_type_name(self):
        return "Ondalık"
    def __repr__(self):
        return str(self.val)

class OzString(OzValue):
    def __init__(self, val):
        self.val = str(val)
    def to_native(self):
        return self.val
    def get_type_name(self):
        return "Metin"
    def __repr__(self):
        return self.val

class OzList(OzValue):
    def __init__(self, val=None):
        if val is None:
            self.val = []
        elif isinstance(val, list):
            self.val = [wrap_value(v) for v in val]
        else:
            self.val = list(val)
    def to_native(self):
        return [v.to_native() if isinstance(v, OzValue) else v for v in self.val]
    def get_type_name(self):
        return "Liste"
    def __repr__(self):
        return "[" + ", ".join(repr(v) for v in self.val) + "]"

class OzMap(OzValue):
    def __init__(self, val=None):
        if val is None:
            self.val = {}
        elif isinstance(val, dict):
            self.val = {wrap_value(k): wrap_value(v) for k, v in val.items()}
        else:
            self.val = val
    def to_native(self):
        return {
            (k.to_native() if isinstance(k, OzValue) else k):
            (v.to_native() if isinstance(v, OzValue) else v)
            for k, v in self.val.items()
        }
    def get_type_name(self):
        return "Sözlük"
    def __repr__(self):
        parts = []
        for k, v in self.val.items():
            parts.append(f"{repr(k)}: {repr(v)}")
        return "{" + ", ".join(parts) + "}"

class OzFunction(OzValue):
    def __init__(self, name, args, body, env, interpreter):
        self.name = name
        self.args = args
        self.body = body
        self.env = env
        self.interpreter = interpreter
    def to_native(self):
        def native_wrapper(*args):
            wrapped_args = [wrap_value(arg) for arg in args]
            res = self.call(wrapped_args)
            return res.to_native() if isinstance(res, OzValue) else res
        return native_wrapper
    def get_type_name(self):
        return "İşlem"
    def __repr__(self):
        return f"<işlem {self.name}>"
    def call(self, passed_args):
        if len(passed_args) != len(self.args):
            raise OzdilError(
                "Tür Hatası (TypeError)",
                f"'{self.name}' işlemi {len(self.args)} parametre bekliyor, fakat {len(passed_args)} tane verildi.",
                1
            )
        from .environment import Environment
        local_env = Environment(self.env)
        # Parameter bindings are stored as OzValue objects in the local environment
        for arg_name, arg_val in zip(self.args, passed_args):
            local_env.define(arg_name, wrap_value(arg_val))
        
        try:
            for stmt in self.body:
                self.interpreter.eval(stmt, local_env)
        except ReturnException as r:
            return wrap_value(r.value)
        return OzNull()

class OzClass(OzValue):
    def __init__(self, name, methods, interpreter):
        self.name = name
        self.methods = methods  # dict of name -> OzFunction
        self.interpreter = interpreter
    def to_native(self):
        return self
    def get_type_name(self):
        return "Sınıf"
    def __repr__(self):
        return f"<sınıf {self.name}>"
    def call(self, passed_args):
        instance = OzInstance(self)
        init_method = self.methods.get('__init__')
        if init_method:
            bound_init = OzBoundMethod(init_method, instance)
            bound_init.call(passed_args)
        elif len(passed_args) > 0:
            raise OzdilError("Tür Hatası (TypeError)", f"'{self.name}' sınıfı parametre almıyor.", 1)
        return instance

class OzBoundMethod(OzValue):
    def __init__(self, method, instance):
        self.method = method  # OzFunction
        self.instance = instance  # OzInstance
    def to_native(self):
        def native_wrapper(*args):
            wrapped_args = [wrap_value(arg) for arg in args]
            res = self.call(wrapped_args)
            return res.to_native() if isinstance(res, OzValue) else res
        return native_wrapper
    def get_type_name(self):
        return "Metot"
    def __repr__(self):
        return f"<bağlı metot {self.method.name}>"
    def call(self, passed_args):
        return self.method.call([self.instance] + passed_args)

class OzInstance(OzValue):
    def __init__(self, klass):
        self.klass = klass
        self.fields = {}
    def to_native(self):
        return self
    def get_type_name(self):
        return "Nesne"
    def __repr__(self):
        return f"<{self.klass.name} nesnesi>"
    def get_attr(self, name):
        if name in self.fields:
            return self.fields[name]
        if name in self.klass.methods:
            return OzBoundMethod(self.klass.methods[name], self)
        raise AttributeError(f"'{self.klass.name}' nesnesinin '{name}' adında bir özelliği yok.")
    def set_attr(self, name, value):
        self.fields[name] = wrap_value(value)

class OzNativeCallable(OzValue):
    def __init__(self, name, func):
        self.name = name
        self.func = func
    def to_native(self):
        return self.func
    def get_type_name(self):
        return "Yerleşik İşlem"
    def __repr__(self):
        return f"<yerleşik işlem {self.name}>"
    def call(self, passed_args):
        native_args = [v.to_native() if isinstance(v, OzValue) else v for v in passed_args]
        res = self.func(*native_args)
        return wrap_value(res)

def wrap_value(val):
    if isinstance(val, OzValue):
        return val
    if val is None:
        return OzNull()
    if isinstance(val, bool):
        return OzBool(val)
    if isinstance(val, int):
        return OzInt(val)
    if isinstance(val, float):
        return OzFloat(val)
    if isinstance(val, str):
        return OzString(val)
    if isinstance(val, list):
        return OzList(val)
    if isinstance(val, tuple):
        return OzList(list(val))
    if isinstance(val, dict):
        return OzMap(val)
    if callable(val):
        return OzNativeCallable(getattr(val, '__name__', 'anonim'), val)
    return val
