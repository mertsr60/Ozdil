# -*- coding: utf-8 -*-
from .errors import OzdilError

# Move mapping to module level to prevent recreating it on every validate_type call
_TYPE_MAPPING = {
    'tam_sayı': int, 'tam_sayi': int,
    'ondalık': float, 'ondalik': float,
    'metin': str,
    'liste': list,
    'sözlük': dict, 'sozluk': dict
}

class Environment:
    def __init__(self, parent=None):
        self.values = {}
        self.modifiers = {}
        self.parent = parent
        
    def define(self, name, value, modifier=None):
        self.values[name] = value
        if modifier:
            self.modifiers[name] = modifier
            self.validate_type(modifier, value, -1) # Default to -1 if we define directly at start
            
    def lookup(self, name, lineno):
        env = self
        while env is not None:
            if name in env.values:
                return env.values[name]
            env = env.parent
        raise OzdilError("Tanımlanmamış Değişken (NameError)", f"'{name}' tanımlanmamış bir değişken.", lineno)
        
    def assign(self, name, value, lineno, modifier=None):
        env = self.find_env_for_var(name)
        if env:
            # Check constant assignment
            if env.is_constant(name):
                raise OzdilError("Sabit Hatası (ConstantError)", f"'{name}' bir sabittir ve değeri değiştirilemez.", lineno)
            
            # Type constraint check
            target_mod = env.modifiers.get(name) or modifier
            if target_mod:
                self.validate_type(target_mod, value, lineno)
                if modifier and modifier != target_mod:
                    raise OzdilError("Tip Hatası (TypeError)", f"'{name}' değişkeninin veri türü değiştirilemez (Mevcut: '{target_mod}', Verilen: '{modifier}').", lineno)
            
            env.values[name] = value
            if modifier:
                env.modifiers[name] = modifier
        else:
            # Define as new variable in local scope
            if modifier:
                self.validate_type(modifier, value, lineno)
                self.modifiers[name] = modifier
            self.values[name] = value
            
    def is_constant(self, name):
        env = self
        while env is not None:
            if name in env.modifiers and env.modifiers[name] == 'sabit':
                return True
            env = env.parent
        return False
        
    def find_env_for_var(self, name):
        env = self
        while env is not None:
            if name in env.values:
                return env
            env = env.parent
        return None
        
    def validate_type(self, modifier, value, lineno):
        if modifier == 'sabit':
            return # Sabit can contain any type initially
        
        expected_type = _TYPE_MAPPING.get(modifier)
        if expected_type:
            # Special case for ints and floats
            if expected_type is float and isinstance(value, int):
                return # Implicitly allow int to float assignment
            if not isinstance(value, expected_type):
                raise OzdilError(
                    "Tip Hatası (TypeError)",
                    f"Beklenen veri türü '{modifier}', fakat '{type(value).__name__}' türünde değer verildi.",
                    lineno
                )

