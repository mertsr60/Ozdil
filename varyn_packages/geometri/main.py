# Geometri ve Alan/Hacim Hesaplama Kütüphanesi
import math

def ucgen_alani(taban, yukseklik):
    return round(0.5 * float(taban) * float(yukseklik), 2)

def daire_alani(yaricap):
    r = float(yaricap)
    return round(math.pi * (r ** 2), 2)

def daire_cevresi(yaricap):
    r = float(yaricap)
    return round(2 * math.pi * r, 2)

def hipotenus(a, b):
    return round(math.sqrt((float(a) ** 2) + (float(b) ** 2)), 2)

def kure_hacmi(yaricap):
    r = float(yaricap)
    return round((4.0 / 3.0) * math.pi * (r ** 3), 2)

def silindir_hacmi(yaricap, yukseklik):
    r = float(yaricap)
    h = float(yukseklik)
    return round(math.pi * (r ** 2) * h, 2)

def plugin():
    return {
        "ucgen_alani": ucgen_alani,
        "daire_alani": daire_alani,
        "daire_cevresi": daire_cevresi,
        "hipotenus": hipotenus,
        "kure_hacmi": kure_hacmi,
        "silindir_hacmi": silindir_hacmi
    }
