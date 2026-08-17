# Şifreleme ve Kriptografi Yardımcı Araçları
import hashlib
import base64

def sha256_hesapla(metin):
    return hashlib.sha256(str(metin).encode("utf-8")).hexdigest()

def md5_hesapla(metin):
    return hashlib.md5(str(metin).encode("utf-8")).hexdigest()

def base64_kodla(metin):
    return base64.b64encode(str(metin).encode("utf-8")).decode("utf-8")

def base64_coz(kodlanmis_metin):
    try:
        return base64.b64decode(str(kodlanmis_metin).encode("utf-8")).decode("utf-8")
    except Exception:
        return None

def sezar_sifrele(metin, anahtar=3):
    sonuc = []
    for char in str(metin):
        if char.isalpha():
            base = ord("A") if char.isupper() else ord("a")
            sonuc.append(chr((ord(char) - base + int(anahtar)) % 26 + base))
        else:
            sonuc.append(char)
    return "".join(sonuc)

def sezar_coz(metin, anahtar=3):
    return sezar_sifrele(metin, -int(anahtar))

def plugin():
    return {
        "sha256_hesapla": sha256_hesapla,
        "md5_hesapla": md5_hesapla,
        "base64_kodla": base64_kodla,
        "base64_coz": base64_coz,
        "sezar_sifrele": sezar_sifrele,
        "sezar_coz": sezar_coz
    }
