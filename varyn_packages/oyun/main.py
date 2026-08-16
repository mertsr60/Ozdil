# Eğlenceli Konsol Oyun Eklentisi
import random
import plugin_api

def tas_kagit_makas(oyuncu_secimi):
    oyuncu = str(oyuncu_secimi).strip().lower()
    if oyuncu in ("taş", "tas"): oyuncu_norm = "tas"
    elif oyuncu in ("kağıt", "kagit"): oyuncu_norm = "kagit"
    elif oyuncu == "makas": oyuncu_norm = "makas"
    else:
        return "Geçersiz seçim! Lütfen taş, kağıt veya makas seçin."
    bilgisayar = random.choice(["tas", "kagit", "makas"])
    tr_map = {"tas": "Taş", "kagit": "Kağıt", "makas": "Makas"}
    if oyuncu_norm == bilgisayar:
        durum = "Berabere!"
    elif (oyuncu_norm == "tas" and bilgisayar == "makas") or          (oyuncu_norm == "kagit" and bilgisayar == "tas") or          (oyuncu_norm == "makas" and bilgisayar == "kagit"):
        durum = "Oyuncu kazandı! 🎉"
    else:
        durum = "Bilgisayar kazandı! 🤖"
    return f"Sizin Seçiminiz: {tr_map[oyuncu_norm]} | Bilgisayar: {tr_map[bilgisayar]} | Sonuç: {durum}"

def sayi_tahmin_et(hedef, tahmin):
    hedef = int(hedef)
    tahmin = int(tahmin)
    if tahmin < hedef:
        return "yukarı"
    elif tahmin > hedef:
        return "aşağı"
    else:
        return "doğru"

def zar_at():
    return random.randint(1, 6)

def skor_tablosu(isimler, skorlar):
    if not isinstance(isimler, list) or not isinstance(skorlar, list):
        return "Hata: İsimler ve skorlar liste olmalıdır."
    eslesmeler = []
    for i in range(min(len(isimler), len(skorlar))):
        eslesmeler.append((str(isimler[i]), int(skorlar[i])))
    eslesmeler.sort(key=lambda x: x[1], reverse=True)
    tablo = ["=== LİDERLİK TABLOSU ==="]
    for sira, (isim, skor) in enumerate(eslesmeler, 1):
        tablo.append(f"{sira}. {isim:<15} : {skor} Puan")
    tablo.append("=======================")
    return "\n".join(tablo)

def plugin():
    plugin_api.plugin.fonksiyon_ekle("tas_kagit_makas", tas_kagit_makas)
    plugin_api.plugin.fonksiyon_ekle("sayi_tahmin_et", sayi_tahmin_et)
    plugin_api.plugin.fonksiyon_ekle("zar_at", zar_at)
    plugin_api.plugin.fonksiyon_ekle("skor_tablosu", skor_tablosu)
    return {
        "tas_kagit_makas": tas_kagit_makas,
        "sayi_tahmin_et": sayi_tahmin_et,
        "zar_at": zar_at,
        "skor_tablosu": skor_tablosu
    }
