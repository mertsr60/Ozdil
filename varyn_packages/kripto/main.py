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
    res = []
    for char in str(metin):
        if char.isalpha():
            start = ord('a') if char.islower() else ord('A')
            res.append(chr((ord(char) - start + int(anahtar)) % 26 + start))
        else:
            res.append(char)
    return "".join(res)

def plugin():
    plugin_api.plugin.fonksiyon_ekle("md5_uret", md5_uret)
    plugin_api.plugin.fonksiyon_ekle("sha256_uret", sha256_uret)
    plugin_api.plugin.fonksiyon_ekle("base64_kodla", base64_kodla)
    plugin_api.plugin.fonksiyon_ekle("base64_coz", base64_coz)
    plugin_api.plugin.fonksiyon_ekle("sezar_sifrele", sezar_sifrele)
    return {
        "md5_uret": md5_uret,
        "sha256_uret": sha256_uret,
        "base64_kodla": base64_kodla,
        "base64_coz": base64_coz,
        "sezar_sifrele": sezar_sifrele
    }
