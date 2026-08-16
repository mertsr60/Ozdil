# Rastgele Veri Üretim Eklentisi
import random
import plugin_api

def rastgele_sayi(min_val, max_val):
    return random.randint(int(min_val), int(max_val))

def rastgele_sec(liste):
    if not liste:
        return None
    return random.choice(liste)

def rastgele_karistir(liste):
    copied = list(liste)
    random.shuffle(copied)
    return copied

def sifre_olustur(uzunluk):
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
    res = [random.choice(characters) for _ in range(int(uzunluk))]
    return "".join(res)

def plugin():
    plugin_api.plugin.fonksiyon_ekle("rastgele_sayi", rastgele_sayi)
    plugin_api.plugin.fonksiyon_ekle("rastgele_sec", rastgele_sec)
    plugin_api.plugin.fonksiyon_ekle("rastgele_karistir", rastgele_karistir)
    plugin_api.plugin.fonksiyon_ekle("sifre_olustur", sifre_olustur)
    return {
        "rastgele_sayi": rastgele_sayi,
        "rastgele_sec": rastgele_sec,
        "rastgele_karistir": rastgele_karistir,
        "sifre_olustur": sifre_olustur
    }
