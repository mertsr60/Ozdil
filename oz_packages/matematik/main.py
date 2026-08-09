# Matematik Eklentisi
import math
import plugin_api

def karekok(x):
    try:
        val = float(x)
        if val < 0:
            return "Hata: Negatif sayının karekökü alınamaz."
        return math.sqrt(val)
    except Exception as e:
        return f"Hata: {str(e)}"

def us(x, y):
    try:
        return math.pow(float(x), float(y))
    except Exception as e:
        return f"Hata: {str(e)}"

def mutlak_deger(x):
    try:
        return abs(float(x))
    except Exception as e:
        return f"Hata: {str(e)}"

def faktoriyel(x):
    try:
        val = int(float(x))
        if val < 0:
            return "Hata: Negatif sayının faktöriyeli yoktur."
        return math.factorial(val)
    except Exception as e:
        return f"Hata: {str(e)}"

def plugin():
    # Yeni eklenti API'sini kullanarak fonksiyonları doğrudan ÖzDil global alanına ekliyoruz
    plugin_api.plugin.fonksiyon_ekle("karekok", karekok)
    plugin_api.plugin.fonksiyon_ekle("us", us)
    plugin_api.plugin.fonksiyon_ekle("mutlak_deger", mutlak_deger)
    plugin_api.plugin.fonksiyon_ekle("faktoriyel", faktoriyel)
    return {
        "karekok": karekok,
        "us": us,
        "mutlak_deger": mutlak_deger,
        "faktoriyel": faktoriyel
    }
