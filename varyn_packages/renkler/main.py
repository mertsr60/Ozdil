# Renklendirme Eklentisi
import plugin_api

def kirmizi(metin):
    return f"\033[91m{metin}\033[0m"

def yesil(metin):
    return f"\033[92m{metin}\033[0m"

def mavi(metin):
    return f"\033[94m{metin}\033[0m"

def plugin():
    plugin_api.plugin.fonksiyon_ekle("kirmizi", kirmizi)
    plugin_api.plugin.fonksiyon_ekle("yesil", yesil)
    plugin_api.plugin.fonksiyon_ekle("mavi", mavi)
    return {
        "kirmizi": kirmizi,
        "yesil": yesil,
        "mavi": mavi
    }
