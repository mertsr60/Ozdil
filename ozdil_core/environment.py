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
        # If a modifier is explicitly provided (except if it is None), it represents a variable declaration.
        # It must be defined in the local environment directly to shadow outer variables.
        if modifier is not None:
            # Check constant assignment in local scope first
            if name in self.values and self.is_constant(name):
                raise OzdilError("Sabit Hatası (ConstantError)", f"'{name}' bir sabittir ve değeri değiştirilemez.", lineno)
            
            # If there's an existing type constraint in local scope:
            target_mod = self.modifiers.get(name) or modifier
            if target_mod:
                self.validate_type(target_mod, value, lineno)
                # If we redeclare with a different modifier
                if modifier != target_mod and target_mod != 'değişken' and modifier != 'değişken':
                    raise OzdilError("Tip Hatası (TypeError)", f"'{name}' değişkeninin veri türü değiştirilemez (Mevcut: '{target_mod}', Verilen: '{modifier}').", lineno)
            
            self.values[name] = value
            self.modifiers[name] = modifier
        else:
            # If modifier is None, we look up if the variable is already defined in the hierarchy.
            env = self.find_env_for_var(name)
            if env:
                if env.is_constant(name):
                    raise OzdilError("Sabit Hatası (ConstantError)", f"'{name}' bir sabittir ve değeri değiştirilemez.", lineno)
                
                target_mod = env.modifiers.get(name)
                if target_mod:
                    self.validate_type(target_mod, value, lineno)
                
                env.values[name] = value
            else:
                # If not found anywhere, define in the local scope
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
        
        from .runtime_types import OzValue
        native_value = value.to_native() if isinstance(value, OzValue) else value
        
        expected_type = _TYPE_MAPPING.get(modifier)
        if expected_type:
            # Special case for ints and floats
            if expected_type is float and isinstance(native_value, int):
                return # Implicitly allow int to float assignment
            if not isinstance(native_value, expected_type):
                type_name = getattr(value, 'get_type_name', lambda: type(native_value).__name__)()
                raise OzdilError(
                    "Tip Hatası (TypeError)",
                    f"Beklenen veri türü '{modifier}', fakat '{type_name}' türünde değer verildi.",
                    lineno
                )

