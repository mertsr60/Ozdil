# Veri Analizi Eklentisi
import plugin_api

def ortalama(sayilar):
    if not sayilar:
        return 0
    return sum(sayilar) / len(sayilar)

def medyan(sayilar):
    if not sayilar:
        return 0
    s = sorted(sayilar)
    n = len(s)
    if n % 2 == 1:
        return s[n // 2]
    return (s[n // 2 - 1] + s[n // 2]) / 2.0

def plugin():
    plugin_api.plugin.fonksiyon_ekle("ortalama", ortalama)
    plugin_api.plugin.fonksiyon_ekle("medyan", medyan)
    return {
        "ortalama": ortalama,
        "medyan": medyan
    }
