# İş Otomasyonu ve Günlük Tutma Kütüphanesi
import time

_GUNLUK_LISTESI = []

def gunluk_ekle(mesaj, seviye="BILGI"):
    zaman_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    kayit = f"[{zaman_str}] [{str(seviye).upper()}]: {str(mesaj)}"
    _GUNLUK_LISTESI.append(kayit)
    return kayit

def gunluk_dokum():
    return list(_GUNLUK_LISTESI)

def gunluk_temizle():
    _GUNLUK_LISTESI.clear()
    return True

def zamanlayici_suresi(saniye_sayisi):
    s = int(saniye_sayisi)
    dakika = s // 60
    kalan_saniye = s % 60
    saat = dakika // 60
    kalan_dakika = dakika % 60
    return f"{saat:02d}:{kalan_dakika:02d}:{kalan_saniye:02d}"

def plugin():
    return {
        "gunluk_ekle": gunluk_ekle,
        "gunluk_dokum": gunluk_dokum,
        "gunluk_temizle": gunluk_temizle,
        "zamanlayici_suresi": zamanlayici_suresi
    }
