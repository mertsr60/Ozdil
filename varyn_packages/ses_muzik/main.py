# Ses ve Müzik Frekans/Ritim Kütüphanesi
import math

_NOTALAR = {
    "DO": 261.63, "C": 261.63,
    "RE": 293.66, "D": 293.66,
    "MI": 329.63, "E": 329.63,
    "FA": 349.23, "F": 349.23,
    "SOL": 392.00, "G": 392.00,
    "LA": 440.00, "A": 440.00,
    "SI": 493.88, "B": 493.88
}

def nota_frekansi(nota_adi):
    return _NOTALAR.get(str(nota_adi).upper(), 440.0)

def oktav_hesapla(frekans, oktav_farki):
    return float(frekans) * (2 ** int(oktav_farki))

def bpm_vurus_suresi(bpm):
    if bpm <= 0:
        return 0.0
    return 60.0 / float(bpm)

def sinus_dalgasi_ornekle(frekans, sure_saniye=1, ornekleme_hizi=8000):
    ornekler = []
    toplam_ornek = int(sure_saniye * ornekleme_hizi)
    for i in range(min(toplam_ornek, 1000)):
        t = i / float(ornekleme_hizi)
        val = math.sin(2 * math.pi * float(frekans) * t)
        ornekler.append(round(val, 4))
    return ornekler

def plugin():
    return {
        "nota_frekansi": nota_frekansi,
        "oktav_hesapla": oktav_hesapla,
        "bpm_vurus_suresi": bpm_vurus_suresi,
        "sinus_dalgasi_ornekle": sinus_dalgasi_ornekle
    }
