# Tarih ve Saat Eklentisi
import datetime
import plugin_api

def simdi():
    now = datetime.datetime.now()
    return {
        "yil": now.year,
        "ay": now.month,
        "gun": now.day,
        "saat": now.hour,
        "dakika": now.minute,
        "saniye": now.second
    }

def turkce_tarih(yil=None, ay=None, gun=None):
    aylar = ["", "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
    if yil is None or ay is None or gun is None:
        now = datetime.datetime.now()
        yil, ay, gun = now.year, now.month, now.day
    try:
        dt = datetime.datetime(int(yil), int(ay), int(gun))
        gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
        gun_adi = gunler[dt.weekday()]
        ay_adi = aylar[dt.month]
        return f"{dt.day} {ay_adi} {dt.year} {gun_adi}"
    except Exception as e:
        return f"Hata: {str(e)}"

def gun_farki(tarih1_str, tarih2_str):
    try:
        t1 = datetime.datetime.strptime(tarih1_str.strip(), "%Y-%m-%d")
        t2 = datetime.datetime.strptime(tarih2_str.strip(), "%Y-%m-%d")
        return abs((t2 - t1).days)
    except Exception as e:
        return f"Format Hatası (beklenen YYYY-MM-DD): {str(e)}"

def plugin():
    plugin_api.plugin.fonksiyon_ekle("simdi", simdi)
    plugin_api.plugin.fonksiyon_ekle("turkce_tarih", turkce_tarih)
    plugin_api.plugin.fonksiyon_ekle("gun_farki", gun_farki)
    return {
        "simdi": simdi,
        "turkce_tarih": turkce_tarih,
        "gun_farki": gun_farki
    }
