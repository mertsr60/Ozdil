# -*- coding: utf-8 -*-
from .errors import VarynError
from .runtime_types import OzValue, OzInstance, tr_upper, tr_lower

# Forbidden attribute names and substrings to prevent Python sandbox escapes
DANGEROUS_ATTRIBUTES = {
    'class', 'base', 'bases', 'subclasses', 'mro',
    'globals', 'builtins', 'code', 'closure', 'defaults', 'kwdefaults',
    'dict', 'doc', 'module', 'qualname', 'name', 'self', 'func',
    'init', 'new', 'del', 'call', 'reduce', 'reduce_ex',
    'getstate', 'setstate', 'annotations', 'frame', 'traceback',
    'loader', 'spec', 'path', 'package', 'objclass',
    'f_globals', 'f_locals', 'f_builtins', 'f_code',
    'gi_frame', 'cr_frame', 'ag_frame', 'tb_frame', 'tb_next',
    'co_code', 'co_consts', 'co_names', 'co_varnames',
    'import', 'eval', 'exec', 'compile', 'system', 'popen', 'spawn'
}

def is_dangerous_attribute(attr):
    if not isinstance(attr, str):
        return True
    if attr.startswith('_') or '__' in attr:
        return True
    attr_lower = attr.lower()
    cleaned = attr_lower.replace('_', '')
    if attr_lower in DANGEROUS_ATTRIBUTES or cleaned in DANGEROUS_ATTRIBUTES:
        return True
    for item in DANGEROUS_ATTRIBUTES:
        if item == attr_lower or item == cleaned or item.replace('_', '') == cleaned:
            return True
    return False

_LIST_METHODS = {
    'ekle': 'append', 'append': 'append',
    'çıkar': 'remove', 'cikar': 'remove', 'remove': 'remove',
    'temizle': 'clear', 'clear': 'clear',
    'sırala': 'sort', 'sirala': 'sort', 'sort': 'sort',
    'ters_çevir': 'reverse', 'ters_cevir': 'reverse', 'reverse': 'reverse',
    'bul': 'index', 'index': 'index',
    'say': 'count', 'count': 'count',
    'sil': 'pop', 'pop': 'pop'
}

_DICT_METHODS = {
    'temizle': 'clear', 'clear': 'clear',
    'sil': 'pop', 'pop': 'pop'
}

def get_attribute(obj, attr, lineno):
    # Strictly block dangerous introspection and internal attributes
    if is_dangerous_attribute(attr):
        raise VarynError(
            "Öznitelik Hatası (AttributeError)",
            f"Güvenlik İhlali: '{attr}' özniteliğine veya sistem nesnesine erişim engellendi.",
            lineno
        )

    if isinstance(obj, OzValue):
        if hasattr(obj, 'get_attr'):
            try:
                return obj.get_attr(attr)
            except AttributeError:
                pass
        native_obj = obj.to_native()
        if native_obj is not obj:
            try:
                return get_attribute(native_obj, attr, lineno)
            except VarynError:
                pass

    if isinstance(obj, list):
        if attr in _LIST_METHODS:
            return getattr(obj, _LIST_METHODS[attr])
        if attr in ('uzunluk', 'len'):
            return lambda: len(obj)
    elif isinstance(obj, dict):
        if attr in _DICT_METHODS:
            return getattr(obj, _DICT_METHODS[attr])
        if attr in ('anahtarlar', 'keys'):
            return lambda: list(obj.keys())
        if attr in ('değerler', 'degerler', 'values'):
            return lambda: list(obj.values())
        if attr in ('çıkar', 'cikar', 'remove'):
            return lambda key: obj.pop(key, None)
        if attr in ('uzunluk', 'len'):
            return lambda: len(obj)
    elif isinstance(obj, str):
        if attr in ('büyük_harf', 'buyuk_harf', 'upper'):
            return lambda: tr_upper(obj)
        if attr in ('küçük_harf', 'kucuk_harf', 'lower'):
            return lambda: tr_lower(obj)
        if attr in ('uzunluk', 'len'):
            return lambda: len(obj)
        if attr in ('parçala', 'parcala', 'split'):
            return lambda sep=None: obj.split(sep)
        if attr in ('değiştir', 'degistir', 'replace'):
            return lambda old, new: obj.replace(old, new)
        if attr in ('kırp', 'kirp', 'strip'):
            return lambda: obj.strip()
        if attr in ('başlar_mı', 'baslar_mi', 'startswith'):
            return lambda prefix: obj.startswith(prefix)
        if attr in ('biter_mi', 'endswith'):
            return lambda suffix: obj.endswith(suffix)
        if attr in ('bul', 'find'):
            return lambda sub: obj.find(sub)
            
    if isinstance(obj, dict) and attr in obj:
        return obj[attr]
        
    # Safe user class instances
    if isinstance(obj, OzInstance):
        try:
            return obj.get_attr(attr)
        except AttributeError:
            pass

    obj_type_name = obj._OzInstance__klass.name if isinstance(obj, OzInstance) else type(obj).__name__
    raise VarynError(
        "Öznitelik Hatası (AttributeError)",
        f"'{obj_type_name}' nesnesinin '{attr}' adında bir özelliği veya fonksiyonu yok.",
        lineno
    )

