# Matematik Eklentisi
import math
import plugin_api

def karekok(x):
    return math.sqrt(x)

def us(x, y):
    return math.pow(x, y)

def plugin():
    # Yeni eklenti API'sini kullanarak fonksiyonları doğrudan Varyn global alanına ekliyoruz
    plugin_api.plugin.fonksiyon_ekle("karekok", karekok)
    plugin_api.plugin.fonksiyon_ekle("us", us)
    return {
        "karekok": karekok,
        "us": us
    }
