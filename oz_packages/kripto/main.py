# Kripto ve Özetleme Eklentisi
import hashlib
import plugin_api
import base64

def md5_uret(metin):
    return hashlib.md5(str(metin).encode("utf-8")).hexdigest()

def sha256_uret(metin):
    return hashlib.sha256(str(metin).encode("utf-8")).hexdigest()

def base64_kodla(metin):
    encoded = base64.b64encode(str(metin).encode("utf-8"))
    return encoded.decode("utf-8")

def base64_coz(metin):
    try:
        decoded = base64.b64decode(str(metin).encode("utf-8"))
        return decoded.decode("utf-8")
    except Exception as e:
        return f"Çözme Hatası: {str(e)}"

def sezar_sifrele(metin, anahtar):
    tr_lower = "abcçdefgğhıijklmnoöprsştuüvyz"
    tr_upper = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"
    en_lower = "abcdefghijklmnopqrstuvwxyz"
    en_upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    res = []
    shift = int(anahtar)
    for char in str(metin):
        if char in tr_lower:
            idx = tr_lower.index(char)
            new_idx = (idx + shift) % 29
            res.append(tr_lower[new_idx])
        elif char in tr_upper:
            idx = tr_upper.index(char)
            new_idx = (idx + shift) % 29
            res.append(tr_upper[new_idx])
        elif char in en_lower:
            idx = en_lower.index(char)
            new_idx = (idx + shift) % 26
            res.append(en_lower[new_idx])
        elif char in en_upper:
            idx = en_upper.index(char)
            new_idx = (idx + shift) % 26
            res.append(en_upper[new_idx])
        else:
            res.append(char)
    return "".join(res)

def sezar_coz(metin, anahtar):
    return sezar_sifrele(metin, -int(anahtar))

def sha1_uret(metin):
    return hashlib.sha1(str(metin).encode("utf-8")).hexdigest()

def plugin():
    plugin_api.plugin.fonksiyon_ekle("md5_uret", md5_uret)
    plugin_api.plugin.fonksiyon_ekle("sha256_uret", sha256_uret)
    plugin_api.plugin.fonksiyon_ekle("sha1_uret", sha1_uret)
    plugin_api.plugin.fonksiyon_ekle("base64_kodla", base64_kodla)
    plugin_api.plugin.fonksiyon_ekle("base64_coz", base64_coz)
    plugin_api.plugin.fonksiyon_ekle("sezar_sifrele", sezar_sifrele)
    plugin_api.plugin.fonksiyon_ekle("sezar_coz", sezar_coz)
    return {
        "md5_uret": md5_uret,
        "sha256_uret": sha256_uret,
        "sha1_uret": sha1_uret,
        "base64_kodla": base64_kodla,
        "base64_coz": base64_coz,
        "sezar_sifrele": sezar_sifrele,
        "sezar_coz": sezar_coz
    }
