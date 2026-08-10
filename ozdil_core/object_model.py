# -*- coding: utf-8 -*-
from .errors import OzdilError
from .runtime_types import OzValue, OzInstance, tr_upper, tr_lower

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
            except OzdilError:
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
    elif isinstance(obj, str):
        if attr in ('büyük_harf', 'buyuk_harf', 'upper'):
            return lambda: tr_upper(obj)
        if attr in ('küçük_harf', 'kucuk_harf', 'lower'):
            return lambda: tr_lower(obj)
            
    if isinstance(obj, dict) and attr in obj:
        return obj[attr]
        
    if hasattr(obj, attr):
        return getattr(obj, attr)
        
    obj_type_name = obj._OzInstance__klass.name if isinstance(obj, OzInstance) else type(obj).__name__
    raise OzdilError(
        "Öznitelik Hatası (AttributeError)",
        f"'{obj_type_name}' nesnesinin '{attr}' adında bir özelliği veya fonksiyonu yok.",
        lineno
    )
