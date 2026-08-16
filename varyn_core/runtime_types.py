# -*- coding: utf-8 -*-
from .errors import VarynError, ReturnException

def tr_upper(s):
    res = []
    for char in s:
        if char == 'i': res.append('İ')
        elif char == 'ı': res.append('I')
        else: res.append(char.upper())
    return "".join(res)

def tr_lower(s):
    res = []
    for char in s:
        if char == 'İ': res.append('i')
        elif char == 'I': res.append('ı')
        else: res.append(char.lower())
    return "".join(res)

class OzValue:
    def to_native(self):
        raise NotImplementedError()
    def get_type_name(self):
        raise NotImplementedError()
    def __repr__(self):
        raise NotImplementedError()
    def __eq__(self, other):
        if isinstance(other, OzValue):
            return type(self) is type(other) and getattr(self, 'val', None) == getattr(other, 'val', None)
        native_self = self.to_native()
        native_other = other.to_native() if isinstance(other, OzValue) else other
        return native_self == native_other
    def __hash__(self):
        val = getattr(self, 'val', None)
        try:
            return hash((type(self), val))
        except TypeError:
            return id(self)

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
        
    def __add__(self, other):
        o_val = other.val if isinstance(other, (OzInt, OzFloat)) else (other.to_native() if isinstance(other, OzValue) else other)
        res = self.val + o_val
        return OzFloat(res) if isinstance(res, float) or isinstance(other, OzFloat) else OzInt(res)
    def __sub__(self, other):
        o_val = other.val if isinstance(other, (OzInt, OzFloat)) else (other.to_native() if isinstance(other, OzValue) else other)
        res = self.val - o_val
        return OzFloat(res) if isinstance(res, float) or isinstance(other, OzFloat) else OzInt(res)
    def __mul__(self, other):
        o_val = other.val if isinstance(other, (OzInt, OzFloat)) else (other.to_native() if isinstance(other, OzValue) else other)
        res = self.val * o_val
        return OzFloat(res) if isinstance(res, float) or isinstance(other, OzFloat) else OzInt(res)
    def __truediv__(self, other):
        o_val = other.val if isinstance(other, (OzInt, OzFloat)) else (other.to_native() if isinstance(other, OzValue) else other)
        if o_val == 0:
            raise VarynError("Sıfıra Bölme Hatası (ZeroDivisionError)", "Bir sayı sıfıra bölünemez.", 1)
        return OzFloat(self.val / o_val)
    def __mod__(self, other):
        o_val = other.val if isinstance(other, (OzInt, OzFloat)) else (other.to_native() if isinstance(other, OzValue) else other)
        if o_val == 0:
            raise VarynError("Sıfıra Bölme Hatası (ZeroDivisionError)", "Bir sayı sıfıra bölünemez veya mod alınamaz.", 1)
        return OzInt(self.val % int(o_val))
    def __pow__(self, other):
        o_val = other.val if isinstance(other, (OzInt, OzFloat)) else (other.to_native() if isinstance(other, OzValue) else other)
        res = self.val ** o_val
        return OzFloat(res) if isinstance(res, float) or isinstance(other, OzFloat) else OzInt(res)
        
    def __lt__(self, other):
        o_val = other.val if isinstance(other, (OzInt, OzFloat)) else (other.to_native() if isinstance(other, OzValue) else other)
        return OzBool(self.val < o_val)
    def __gt__(self, other):
        o_val = other.val if isinstance(other, (OzInt, OzFloat)) else (other.to_native() if isinstance(other, OzValue) else other)
        return OzBool(self.val > o_val)
    def __le__(self, other):
        o_val = other.val if isinstance(other, (OzInt, OzFloat)) else (other.to_native() if isinstance(other, OzValue) else other)
        return OzBool(self.val <= o_val)
    def __ge__(self, other):
        o_val = other.val if isinstance(other, (OzInt, OzFloat)) else (other.to_native() if isinstance(other, OzValue) else other)
        return OzBool(self.val >= o_val)

class OzFloat(OzValue):
    def __init__(self, val):
        self.val = float(val)
    def to_native(self):
        return self.val
    def get_type_name(self):
        return "Ondalık"
    def __repr__(self):
        return str(self.val)
        
    def __add__(self, other):
        o_val = other.val if isinstance(other, (OzInt, OzFloat)) else (other.to_native() if isinstance(other, OzValue) else other)
        return OzFloat(self.val + o_val)
    def __sub__(self, other):
        o_val = other.val if isinstance(other, (OzInt, OzFloat)) else (other.to_native() if isinstance(other, OzValue) else other)
        return OzFloat(self.val - o_val)
    def __mul__(self, other):
        o_val = other.val if isinstance(other, (OzInt, OzFloat)) else (other.to_native() if isinstance(other, OzValue) else other)
        return OzFloat(self.val * o_val)
    def __truediv__(self, other):
        o_val = other.val if isinstance(other, (OzInt, OzFloat)) else (other.to_native() if isinstance(other, OzValue) else other)
        if o_val == 0:
            raise VarynError("Sıfıra Bölme Hatası (ZeroDivisionError)", "Bir sayı sıfıra bölünemez.", 1)
        return OzFloat(self.val / o_val)
    def __mod__(self, other):
        o_val = other.val if isinstance(other, (OzInt, OzFloat)) else (other.to_native() if isinstance(other, OzValue) else other)
        if o_val == 0:
            raise VarynError("Sıfıra Bölme Hatası (ZeroDivisionError)", "Bir sayı sıfıra bölünemez veya mod alınamaz.", 1)
        return OzFloat(self.val % o_val)
    def __pow__(self, other):
        o_val = other.val if isinstance(other, (OzInt, OzFloat)) else (other.to_native() if isinstance(other, OzValue) else other)
        return OzFloat(self.val ** o_val)
        
    def __lt__(self, other):
        o_val = other.val if isinstance(other, (OzInt, OzFloat)) else (other.to_native() if isinstance(other, OzValue) else other)
        return OzBool(self.val < o_val)
    def __gt__(self, other):
        o_val = other.val if isinstance(other, (OzInt, OzFloat)) else (other.to_native() if isinstance(other, OzValue) else other)
        return OzBool(self.val > o_val)
    def __le__(self, other):
        o_val = other.val if isinstance(other, (OzInt, OzFloat)) else (other.to_native() if isinstance(other, OzValue) else other)
        return OzBool(self.val <= o_val)
    def __ge__(self, other):
        o_val = other.val if isinstance(other, (OzInt, OzFloat)) else (other.to_native() if isinstance(other, OzValue) else other)
        return OzBool(self.val >= o_val)

class OzString(OzValue):
    def __init__(self, val):
        self.val = str(val)
    def to_native(self):
        return self.val
    def get_type_name(self):
        return "Metin"
    def __repr__(self):
        return self.val
        
    def __add__(self, other):
        o_val = other.val if isinstance(other, OzString) else (other.to_native() if isinstance(other, OzValue) else other)
        return OzString(self.val + str(o_val))
    def __mul__(self, other):
        n_val = other.val if isinstance(other, OzInt) else other
        return OzString(self.val * int(n_val))
        
    def __getitem__(self, idx):
        n_idx = idx.to_native() if isinstance(idx, OzValue) else idx
        return OzString(self.val[n_idx])
    def __len__(self):
        return len(self.val)
        
    def get_attr(self, name):
        if name in ('büyük_harf', 'buyuk_harf', 'upper'):
            return OzNativeCallable(name, lambda: tr_upper(self.val))
        if name in ('küçük_harf', 'kucuk_harf', 'lower'):
            return OzNativeCallable(name, lambda: tr_lower(self.val))
        raise AttributeError(f"'Metin' nesnesinin '{name}' adında bir özelliği yok.")

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
        
    def __add__(self, other):
        if isinstance(other, OzList):
            return OzList(self.val + other.val)
        raise TypeError(f"Liste ile {type(other).__name__} toplanamaz.")
        
    def __getitem__(self, idx):
        n_idx = idx.to_native() if isinstance(idx, OzValue) else idx
        return self.val[n_idx]
    def __setitem__(self, idx, value):
        n_idx = idx.to_native() if isinstance(idx, OzValue) else idx
        self.val[n_idx] = wrap_value(value)
    def __len__(self):
        return len(self.val)
    def __iter__(self):
        return iter(self.val)
        
    def get_attr(self, name):
        if name in ('ekle', 'append'):
            return OzNativeCallable(name, lambda item: self.val.append(wrap_value(item)))
        if name in ('çıkar', 'cikar', 'remove'):
            return OzNativeCallable(name, lambda item: self.val.remove(wrap_value(item)))
        if name in ('temizle', 'clear'):
            return OzNativeCallable(name, lambda: self.val.clear())
        if name in ('sırala', 'sirala', 'sort'):
            return OzNativeCallable(name, lambda: self.val.sort(key=lambda x: x.to_native() if isinstance(x, OzValue) else x))
        if name in ('ters_çevir', 'ters_cevir', 'reverse'):
            return OzNativeCallable(name, lambda: self.val.reverse())
        if name in ('bul', 'index'):
            return OzNativeCallable(name, lambda item: self.val.index(wrap_value(item)))
        if name in ('say', 'count'):
            return OzNativeCallable(name, lambda item: self.val.count(wrap_value(item)))
        if name in ('sil', 'pop'):
            return OzNativeCallable(name, lambda *args: self.val.pop(*args) if args else self.val.pop())
        if name in ('uzunluk', 'len'):
            return OzNativeCallable(name, lambda: len(self.val))
        raise AttributeError(f"'Liste' nesnesinin '{name}' adında bir özelliği yok.")

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
        
    def __getitem__(self, key):
        wrapped_key = wrap_value(key)
        if wrapped_key in self.val:
            return self.val[wrapped_key]
        for k, v in self.val.items():
            if k == wrapped_key or (isinstance(k, OzValue) and k.to_native() == wrapped_key.to_native()):
                return v
        raise KeyError(repr(key))
    def __setitem__(self, key, value):
        wrapped_key = wrap_value(key)
        wrapped_val = wrap_value(value)
        self.val[wrapped_key] = wrapped_val
    def __contains__(self, key):
        wrapped_key = wrap_value(key)
        if wrapped_key in self.val:
            return True
        for k in self.val.keys():
            if k == wrapped_key or (isinstance(k, OzValue) and k.to_native() == wrapped_key.to_native()):
                return True
        return False
    def __len__(self):
        return len(self.val)
    def __iter__(self):
        return iter(self.val)
        
    def get_attr(self, name):
        if name in ('temizle', 'clear'):
            return OzNativeCallable(name, lambda: self.val.clear())
        if name in ('sil', 'pop'):
            return OzNativeCallable(name, lambda key, *default: self.val.pop(wrap_value(key), *[wrap_value(d) for d in default]))
        if name in ('anahtarlar', 'keys'):
            return OzNativeCallable(name, lambda: list(k.to_native() if isinstance(k, OzValue) else k for k in self.val.keys()))
        if name in ('değerler', 'degerler', 'values'):
            return OzNativeCallable(name, lambda: list(v.to_native() if isinstance(v, OzValue) else v for v in self.val.values()))
        if name in ('çıkar', 'cikar', 'remove'):
            return OzNativeCallable(name, lambda key: self.val.pop(wrap_value(key), None))
        raise AttributeError(f"'Sözlük' nesnesinin '{name}' adında bir özelliği yok.")

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
            raise VarynError(
                "Tür Hatası (TypeError)",
                f"'{self.name}' işlemi {len(self.args)} parametre bekliyor, fakat {len(passed_args)} tane verildi.",
                1
            )
        from .environment import Environment
        local_env = Environment(self.env)
        # Parameter bindings are stored as OzValue objects in the local environment
        for arg_name, arg_val in zip(self.args, passed_args):
            local_env.define(arg_name, wrap_value(arg_val))
        
        # Check if we have bytecode
        if getattr(self, 'bytecode', None) is not None:
            if hasattr(self.interpreter, 'run'):
                return self.interpreter.run(self.bytecode, local_env)
        
        if self.body is not None:
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
            raise VarynError("Tür Hatası (TypeError)", f"'{self.name}' sınıfı parametre almıyor.", 1)
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
