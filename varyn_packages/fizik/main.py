# Temel Fizik ve Hareket Denklemleri Kütüphanesi
import math

G = 9.80665

def serbest_dusme(sure_saniye):
    t = float(sure_saniye)
    h = 0.5 * G * (t ** 2)
    v = G * t
    return {"yukseklik": round(h, 2), "hiz": round(v, 2)}

def egik_atis(ilk_hiz, aci_derece):
    v0 = float(ilk_hiz)
    rad = math.radians(float(aci_derece))
    v0x = v0 * math.cos(rad)
    v0y = v0 * math.sin(rad)
    ucus_suresi = (2 * v0y) / G
    max_yukseklik = (v0y ** 2) / (2 * G)
    menzil = v0x * ucus_suresi
    return {
        "ucus_suresi": round(ucus_suresi, 2),
        "max_yukseklik": round(max_yukseklik, 2),
        "menzil": round(menzil, 2)
    }

def kinetik_enerji(kutle_kg, hiz_m_s):
    m = float(kutle_kg)
    v = float(hiz_m_s)
    return round(0.5 * m * (v ** 2), 2)

def potansiyel_enerji(kutle_kg, yukseklik_m):
    m = float(kutle_kg)
    h = float(yukseklik_m)
    return round(m * G * h, 2)

def plugin():
    return {
        "serbest_dusme": serbest_dusme,
        "egik_atis": egik_atis,
        "kinetik_enerji": kinetik_enerji,
        "potansiyel_enerji": potansiyel_enerji
    }
