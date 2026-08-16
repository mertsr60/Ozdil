# Türkçe Metin İşleme Eklentisi
import plugin_api

def turkce_kucult(metin):
    res = []
    for char in str(metin):
        if char == 'İ': res.append('i')
        elif char == 'I': res.append('ı')
        else: res.append(char.lower())
    return "".join(res)

def turkce_buyut(metin):
    res = []
    for char in str(metin):
        if char == 'i': res.append('İ')
        elif char == 'ı': res.append('I')
        else: res.append(char.upper())
    return "".join(res)

def slug_yap(metin):
    metin = str(metin)
    lower_str = turkce_kucult(metin)
    replacements = {
        'ş': 's', 'ğ': 'g', 'ç': 'c', 'ö': 'o', 'ü': 'u'
    }
    ascii_chars = []
    for char in lower_str:
        if char in replacements:
            ascii_chars.append(replacements[char])
        elif char.isalnum() or char == ' ':
            ascii_chars.append(char)
        else:
            ascii_chars.append('-')
    
    joined = "".join(ascii_chars)
    import re
    cleaned = re.sub(r'\s+', '-', joined.strip())
    cleaned = re.sub(r'-+', '-', cleaned)
    return cleaned.strip('-')

def sesli_say(metin):
    sesliler = "aeıioöuüAEIİOÖUÜ"
    return sum(1 for char in str(metin) if char in sesliler)

def plugin():
    plugin_api.plugin.fonksiyon_ekle("turkce_kucult", turkce_kucult)
    plugin_api.plugin.fonksiyon_ekle("turkce_buyut", turkce_buyut)
    plugin_api.plugin.fonksiyon_ekle("slug_yap", slug_yap)
    plugin_api.plugin.fonksiyon_ekle("sesli_say", sesli_say)
    return {
        "turkce_kucult": turkce_kucult,
        "turkce_buyut": turkce_buyut,
        "slug_yap": slug_yap,
        "sesli_say": sesli_say
    }
