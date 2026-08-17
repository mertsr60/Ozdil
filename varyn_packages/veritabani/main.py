# Veritabanı ve Anahtar-Değer Deposu Kütüphanesi
import json

_DB_STORE = {}

def baglan(db_adi="varsayilan"):
    if db_adi not in _DB_STORE:
        _DB_STORE[db_adi] = {}
    return db_adi

def koy(anahtar, deger, db_adi="varsayilan"):
    if db_adi not in _DB_STORE:
        _DB_STORE[db_adi] = {}
    _DB_STORE[db_adi][str(anahtar)] = deger
    return True

def al(anahtar, varsayilan=None, db_adi="varsayilan"):
    if db_adi in _DB_STORE:
        return _DB_STORE[db_adi].get(str(anahtar), varsayilan)
    return varsayilan

def sil(anahtar, db_adi="varsayilan"):
    if db_adi in _DB_STORE and str(anahtar) in _DB_STORE[db_adi]:
        del _DB_STORE[db_adi][str(anahtar)]
        return True
    return False

def tumunu_getir(db_adi="varsayilan"):
    if db_adi in _DB_STORE:
        return dict(_DB_STORE[db_adi])
    return {}

def temizle(db_adi="varsayilan"):
    if db_adi in _DB_STORE:
        _DB_STORE[db_adi].clear()
        return True
    return False

def plugin():
    return {
        "veritabani_baglan": baglan,
        "veritabani_koy": koy,
        "veritabani_al": al,
        "veritabani_sil": sil,
        "veritabani_tumunu_getir": tumunu_getir,
        "veritabani_temizle": temizle
    }
