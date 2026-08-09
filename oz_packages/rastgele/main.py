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

def rastgele_renk():
    return "#" + "".join(random.choice("0123456789ABCDEF") for _ in range(6))

def bozuk_para_at():
    return random.choice(["Yazı", "Tura"])

def plugin():
    plugin_api.plugin.fonksiyon_ekle("rastgele_sayi", rastgele_sayi)
    plugin_api.plugin.fonksiyon_ekle("rastgele_sec", rastgele_sec)
    plugin_api.plugin.fonksiyon_ekle("rastgele_karistir", rastgele_karistir)
    plugin_api.plugin.fonksiyon_ekle("sifre_olustur", sifre_olustur)
    plugin_api.plugin.fonksiyon_ekle("rastgele_renk", rastgele_renk)
    plugin_api.plugin.fonksiyon_ekle("bozuk_para_at", bozuk_para_at)
    return {
        "rastgele_sayi": rastgele_sayi,
        "rastgele_sec": rastgele_sec,
        "rastgele_karistir": rastgele_karistir,
        "sifre_olustur": sifre_olustur,
        "rastgele_renk": rastgele_renk,
        "bozuk_para_at": bozuk_para_at
    }
