# Coğrafi Konum ve Mesafe Hesaplama Kütüphanesi
import math

_SEHIR_KOORDINATLARI = {
    "ANKARA": (39.9334, 32.8597),
    "ISTANBUL": (41.0082, 28.9784),
    "IZMIR": (38.4237, 27.1428),
    "BURSA": (40.1885, 29.0610),
    "ANTALYA": (36.8969, 30.7133),
    "ADANA": (37.0000, 35.3213),
    "TRABZON": (41.0027, 39.7168),
    "ERZURUM": (39.9043, 41.2679),
    "SIVAS": (39.7477, 37.0179),
    "GAZIANTEP": (37.0662, 37.3833)
}

def haversine_mesafe(lat1, lon1, lat2, lon2):
    R = 6371.0 # Dünya yarıçapı km
    dlat = math.radians(float(lat2) - float(lat1))
    dlon = math.radians(float(lon2) - float(lon1))
    a = (math.sin(dlat / 2) ** 2) + math.cos(math.radians(float(lat1))) * math.cos(math.radians(float(lat2))) * (math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)

def sehir_koordinati(sehir_adi):
    return _SEHIR_KOORDINATLARI.get(str(sehir_adi).upper(), (0.0, 0.0))

def sehirler_arasi_mesafe(sehir1, sehir2):
    k1 = sehir_koordinati(sehir1)
    k2 = sehir_koordinati(sehir2)
    if k1 == (0.0, 0.0) or k2 == (0.0, 0.0):
        return None
    return haversine_mesafe(k1[0], k1[1], k2[0], k2[1])

def plugin():
    return {
        "haversine_mesafe": haversine_mesafe,
        "sehir_koordinati": sehir_koordinati,
        "sehirler_arasi_mesafe": sehirler_arasi_mesafe
    }
