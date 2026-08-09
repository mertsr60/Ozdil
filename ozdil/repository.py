# -*- coding: utf-8 -*-
"""
ÖzDil Paket Deposu (repository.py)
Bu dosya, ÖzDil paket ekosistemindeki merkezi paket deposunu ve arama/bilgi alma servislerini simüle eder.
"""

import json
import hashlib

# Merkezi Paket Deposu Veritabanı (Simüle edilmiş online depo)
REPOSITORY_PACKAGES = {
    "matematik": {
        "meta": {
            "isim": "matematik",
            "surum": "1.0.0",
            "yazar": "ozdil_toplulugu",
            "tur": "python",
            "aciklama": "Gelişmiş matematiksel işlemler ve sabitler kütüphanesi.",
            "izinler": [],
            "bagimliliklar": []
        },
        "files": {
            "main.py": """# Matematik Eklentisi
import math
import plugin_api

def karekok(x):
    return math.sqrt(x)

def us(x, y):
    return math.pow(x, y)

def plugin():
    # Yeni eklenti API'sini kullanarak fonksiyonları doğrudan ÖzDil global alanına ekliyoruz
    plugin_api.plugin.fonksiyon_ekle("karekok", karekok)
    plugin_api.plugin.fonksiyon_ekle("us", us)
    return {
        "karekok": karekok,
        "us": us
    }
"""
        }
    },
    "renkler": {
        "meta": {
            "isim": "renkler",
            "surum": "1.2.0",
            "yazar": "tasarim_merkezi",
            "tur": "python",
            "aciklama": "Konsol çıktılarını renklendirmek için kullanılan ANSI renk kütüphanesi.",
            "izinler": [],
            "bagimliliklar": []
        },
        "files": {
            "main.py": """# Renklendirme Eklentisi
import plugin_api

def kirmizi(metin):
    return f"\\033[91m{metin}\\033[0m"

def yesil(metin):
    return f"\\033[92m{metin}\\033[0m"

def mavi(metin):
    return f"\\033[94m{metin}\\033[0m"

def plugin():
    plugin_api.plugin.fonksiyon_ekle("kirmizi", kirmizi)
    plugin_api.plugin.fonksiyon_ekle("yesil", yesil)
    plugin_api.plugin.fonksiyon_ekle("mavi", mavi)
    return {
        "kirmizi": kirmizi,
        "yesil": yesil,
        "mavi": mavi
    }
"""
        }
    },
    "hesap": {
        "meta": {
            "isim": "hesap",
            "surum": "2.0.0",
            "yazar": "hesap_uzmani",
            "tur": "python",
            "aciklama": "İstatistiksel hesaplamalar yapan ve renkler paketini kullanan kütüphane.",
            "izinler": [],
            "bagimliliklar": ["renkler>=1.2.0"]
        },
        "files": {
            "main.py": """# Hesaplama ve Sunum Eklentisi
import plugin_api
# renkler bağımlılığını getiriyoruz
import renkler

def renkli_topla(a, b):
    toplam = a + b
    # Bağımlılık olarak yüklenen renkler modülünü kullanıyoruz
    renkli_str = f"Toplam: {toplam}"
    try:
        import renkler
        # plugin_api ya da doğrudan import üzerinden erişilebilir
        renkli_str = renkler.plugin()["yesil"](str(toplam))
    except Exception:
        pass
    return f"Toplama Sonucu: {renkli_str}"

def plugin():
    plugin_api.plugin.fonksiyon_ekle("renkli_topla", renkli_topla)
    return {
        "renkli_topla": renkli_topla
    }
"""
        }
    },
    "grafik": {
        "meta": {
            "isim": "grafik",
            "surum": "1.2.0",
            "yazar": "ozdil_toplulugu",
            "tur": "ozdil",
            "aciklama": "ÖzDil için konsol tabanlı grafik çizim ve görselleştirme araçları.",
            "izinler": [],
            "bagimliliklar": []
        },
        "files": {
            "grafik.oz": """# Grafik ve Konsol Çizim Kütüphanesi

işlem çizgi(karakter, uzunluk):
    değişken s = ""
    döngü i içinde aralık(uzunluk):
        s = s + karakter
    yazdır(s)

işlem kutu(en, boy):
    çizgi("*", en)
    döngü i içinde aralık(boy - 2):
        değişken s = "*"
        döngü j içinde aralık(en - 2):
            s = s + " "
        s = s + "*"
        yazdır(s)
    çizgi("*", en)

işlem grafik_ciz(veriler):
    yazdır("--- Sütun Grafiği ---")
    döngü x içinde veriler:
        değişken bar = ""
        döngü i içinde aralık(x):
            bar = bar + "█"
        yazdır(bar + " (" + metin(x) + ")")
"""
        }
    },
    "kamera": {
        "meta": {
            "isim": "kamera",
            "surum": "1.0.4",
            "yazar": "sistem_gelistirici",
            "tur": "python",
            "aciklama": "Kamera kontrolleri ve fotoğraf çekme işlevleri sağlayan Python eklentisi.",
            "izinler": ["kamera", "dosya_sistemi"],
            "bagimliliklar": []
        },
        "files": {
            "main.py": """# Kamera Donanım Kontrolcü Modülü
import plugin_api

def foto_cek():
    print("[Kamera] Fotoğraf başarıyla çekildi! Görüntü 'foto_cekimi.jpg' olarak kaydedildi.")
    return "foto_cekimi.jpg"

def kamera_ac():
    print("[Kamera] Kamera cihazı donanımı başlatılıyor...")
    print("[Kamera] Video yakalama akışı aktif (30 FPS).")
    return True

def plugin():
    plugin_api.plugin.fonksiyon_ekle("foto_cek", foto_cek)
    plugin_api.plugin.fonksiyon_ekle("kamera_ac", kamera_ac)
    return {
        "foto_cek": foto_cek,
        "kamera_ac": kamera_ac
    }
"""
        }
    },
    "veri_analizi": {
        "meta": {
            "isim": "veri_analizi",
            "surum": "2.1.0",
            "yazar": "veri_bilimci",
            "tur": "python",
            "aciklama": "Veri listeleri üzerinde istatistiksel işlemler yapan kütüphane.",
            "izinler": [],
            "bagimliliklar": []
        },
        "files": {
            "main.py": """# Veri Analizi Eklentisi
import plugin_api

def ortalama(sayilar):
    if not sayilar:
        return 0
    return sum(sayilar) / len(sayilar)

def medyan(sayilar):
    if not sayilar:
        return 0
    s = sorted(sayilar)
    n = len(s)
    if n % 2 == 1:
        return s[n // 2]
    return (s[n // 2 - 1] + s[n // 2]) / 2.0

def plugin():
    plugin_api.plugin.fonksiyon_ekle("ortalama", ortalama)
    plugin_api.plugin.fonksiyon_ekle("medyan", medyan)
    return {
        "ortalama": ortalama,
        "medyan": medyan
    }
"""
        }
    },
    "yapay_zeka": {
        "meta": {
            "isim": "yapay_zeka",
            "surum": "1.1.2",
            "yazar": "ai_uzmani",
            "tur": "ozdil",
            "aciklama": "Temel yapay zeka ve doğrusal regresyon tahmin modeli.",
            "izinler": [],
            "bagimliliklar": []
        },
        "files": {
            "yapay_zeka.oz": """# Temel Yapay Zeka Regresyon Modülü

işlem tahmin_et(girdi):
    değişken sonuc = girdi * 2.5 + 4
    yazdır("[Yapay Zeka] Tahmin Modeli Çalıştırıldı.")
    yazdır("[Yapay Zeka] Girdi Değeri: " + metin(girdi))
    yazdır("[Yapay Zeka] Üretilen Tahmin: " + metin(sonuc))
    döndür sonuc
"""
        }
    },
    "tarih_saat": {
        "meta": {
            "isim": "tarih_saat",
            "surum": "1.0.0",
            "yazar": "ozdil_toplulugu",
            "tur": "python",
            "aciklama": "Tarih, saat ve Türkçe tarih biçimlendirme kütüphanesi.",
            "izinler": [],
            "bagimliliklar": []
        },
        "files": {
            "main.py": """# Tarih ve Saat Eklentisi
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
"""
        }
    },
    "metin_isleme": {
        "meta": {
            "isim": "metin_isleme",
            "surum": "1.0.0",
            "yazar": "ozdil_toplulugu",
            "tur": "python",
            "aciklama": "Gelişmiş Türkçe karakter duyarlı büyük/küçük harf dönüşümü, slug yapımı ve sesli harf analizi.",
            "izinler": [],
            "bagimliliklar": []
        },
        "files": {
            "main.py": """# Türkçe Metin İşleme Eklentisi
import plugin_api

def turkce_kucult(metin):
    res = []
    for char in str(metin):
        if char == 'İ': res.append('i')
        elif char == 'I': res.append('ı')
        else: res.append(char.lower())
    return "".join(res)

def turkce_buyut(metin):
    res = []
    for char in str(metin):
        if char == 'i': res.append('İ')
        elif char == 'ı': res.append('I')
        else: res.append(char.upper())
    return "".join(res)

def slug_yap(metin):
    metin = str(metin)
    lower_str = turkce_kucult(metin)
    replacements = {
        'ş': 's', 'ğ': 'g', 'ç': 'c', 'ö': 'o', 'ü': 'u'
    }
    ascii_chars = []
    for char in lower_str:
        if char in replacements:
            ascii_chars.append(replacements[char])
        elif char.isalnum() or char == ' ':
            ascii_chars.append(char)
        else:
            ascii_chars.append('-')
    
    joined = "".join(ascii_chars)
    import re
    cleaned = re.sub(r'\\s+', '-', joined.strip())
    cleaned = re.sub(r'-+', '-', cleaned)
    return cleaned.strip('-')

def sesli_say(metin):
    sesliler = "aeıioöuüAEIİOÖUÜ"
    return sum(1 for char in str(metin) if char in sesliler)

def plugin():
    plugin_api.plugin.fonksiyon_ekle("turkce_kucult", turkce_kucult)
    plugin_api.plugin.fonksiyon_ekle("turkce_buyut", turkce_buyut)
    plugin_api.plugin.fonksiyon_ekle("slug_yap", slug_yap)
    plugin_api.plugin.fonksiyon_ekle("sesli_say", sesli_say)
    return {
        "turkce_kucult": turkce_kucult,
        "turkce_buyut": turkce_buyut,
        "slug_yap": slug_yap,
        "sesli_say": sesli_say
    }
"""
        }
    },
    "kripto": {
        "meta": {
            "isim": "kripto",
            "surum": "1.0.0",
            "yazar": "güvenlik_timi",
            "tur": "python",
            "aciklama": "Veri özetleme (MD5, SHA256), Base64 kodlama/çözme ve Sezar şifreleme kütüphanesi.",
            "izinler": [],
            "bagimliliklar": []
        },
        "files": {
            "main.py": """# Kripto ve Özetleme Eklentisi
import hashlib
import plugin_api
import base64

def md5_uret(metin):
    return hashlib.md5(str(metin).encode("utf-8")).hexdigest()

def sha256_uret(metin):
    return hashlib.sha256(str(metin).encode("utf-8")).hexdigest()

def base64_kodla(metin):
    encoded = base64.b64encode(str(metin).encode("utf-8"))
    return encoded.decode("utf-8")

def base64_coz(metin):
    try:
        decoded = base64.b64decode(str(metin).encode("utf-8"))
        return decoded.decode("utf-8")
    except Exception as e:
        return f"Çözme Hatası: {str(e)}"

def sezar_sifrele(metin, anahtar):
    res = []
    for char in str(metin):
        if char.isalpha():
            start = ord('a') if char.islower() else ord('A')
            res.append(chr((ord(char) - start + int(anahtar)) % 26 + start))
        else:
            res.append(char)
    return "".join(res)

def plugin():
    plugin_api.plugin.fonksiyon_ekle("md5_uret", md5_uret)
    plugin_api.plugin.fonksiyon_ekle("sha256_uret", sha256_uret)
    plugin_api.plugin.fonksiyon_ekle("base64_kodla", base64_kodla)
    plugin_api.plugin.fonksiyon_ekle("base64_coz", base64_coz)
    plugin_api.plugin.fonksiyon_ekle("sezar_sifrele", sezar_sifrele)
    return {
        "md5_uret": md5_uret,
        "sha256_uret": sha256_uret,
        "base64_kodla": base64_kodla,
        "base64_coz": base64_coz,
        "sezar_sifrele": sezar_sifrele
    }
"""
        }
    },
    "rastgele": {
        "meta": {
            "isim": "rastgele",
            "surum": "1.0.0",
            "yazar": "ozdil_toplulugu",
            "tur": "python",
            "aciklama": "Rastgele sayı üretimi, liste elemanı seçimi ve güvenli şifre oluşturucu.",
            "izinler": [],
            "bagimliliklar": []
        },
        "files": {
            "main.py": """# Rastgele Veri Üretim Eklentisi
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
"""
        }
    },
    "finans": {
        "meta": {
            "isim": "finans",
            "surum": "1.0.0",
            "yazar": "finans_analisti",
            "tur": "python",
            "aciklama": "Bileşik faiz hesaplama, döviz çevirme, enflasyon etkisi ve kredi taksit tablosu çıkaran finansal analiz kütüphanesi.",
            "izinler": [],
            "bagimliliklar": []
        },
        "files": {
            "main.py": """# Gelişmiş Finans ve Yatırım Eklentisi
import plugin_api

def faiz_hesapla(ana_para, oran, sure):
    ana_para = float(ana_para)
    oran = float(oran)
    sure = float(sure)
    toplam = ana_para * ((1 + (oran / 100)) ** sure)
    return round(toplam, 2)

def doviz_cevir(tutar, kur):
    tutar = float(tutar)
    kur = float(kur)
    return round(tutar * kur, 2)

def enflasyon_etkisi(tutar, oran, yil):
    tutar = float(tutar)
    oran = float(oran)
    yil = float(yil)
    alim_gucu = tutar / ((1 + (oran / 100)) ** yil)
    return round(alim_gucu, 2)

def kredi_taksit(tutar, oran, vade):
    tutar = float(tutar)
    yillik_oran = float(oran)
    vade = int(vade)
    aylik_oran = (yillik_oran / 12) / 100
    if aylik_oran == 0:
        return round(tutar / vade, 2)
    faktor = (1 + aylik_oran) ** vade
    taksit = tutar * (aylik_oran * faktor) / (faktor - 1)
    return round(taksit, 2)

def plugin():
    plugin_api.plugin.fonksiyon_ekle("faiz_hesapla", faiz_hesapla)
    plugin_api.plugin.fonksiyon_ekle("doviz_cevir", doviz_cevir)
    plugin_api.plugin.fonksiyon_ekle("enflasyon_etkisi", enflasyon_etkisi)
    plugin_api.plugin.fonksiyon_ekle("kredi_taksit", kredi_taksit)
    return {
        "faiz_hesapla": faiz_hesapla,
        "doviz_cevir": doviz_cevir,
        "enflasyon_etkisi": enflasyon_etkisi,
        "kredi_taksit": kredi_taksit
    }
"""
        }
    },
    "oyun": {
        "meta": {
            "isim": "oyun",
            "surum": "1.0.0",
            "yazar": "retro_kodcu",
            "tur": "python",
            "aciklama": "Taş-kağıt-makas simülasyonu, sayı tahmin rehberliği, şans zarları ve skor tablosu oluşturucu içeren eğlenceli oyun araçları.",
            "izinler": [],
            "bagimliliklar": []
        },
        "files": {
            "main.py": """# Eğlenceli Konsol Oyun Eklentisi
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
    elif (oyuncu_norm == "tas" and bilgisayar == "makas") or \
         (oyuncu_norm == "kagit" and bilgisayar == "tas") or \
         (oyuncu_norm == "makas" and bilgisayar == "kagit"):
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
    return "\\n".join(tablo)

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
"""
        }
    },
    "telefon": {
        "meta": {
            "isim": "telefon",
            "surum": "1.0.0",
            "yazar": "mobil_tasarimci",
            "tur": "python",
            "aciklama": "Mobil telefonlar için etkileşimli, görsel ve zengin arayüz elemanları tasarlamayı sağlayan GUI kütüphanesi.",
            "izinler": [],
            "bagimliliklar": []
        },
        "files": {
            "main.py": """# Mobil GUI Telefon Eklentisi
import plugin_api

def _append_element(elem):
    if getattr(plugin_api.plugin, "current_page", None) is not None:
        plugin_api.plugin.current_page["elements"].append(elem)
    else:
        plugin_api.plugin.gui_elements.append(elem)

def temizle():
    plugin_api.plugin.gui_elements.clear()
    plugin_api.plugin.current_page = None
    return True

def sayfa(sayfa_adi):
    page_dict = {"type": "sayfa", "val": str(sayfa_adi), "elements": []}
    plugin_api.plugin.gui_elements.append(page_dict)
    plugin_api.plugin.current_page = page_dict
    return True

def sayfa_bitir():
    plugin_api.plugin.current_page = None
    return True

def baslik(metin):
    _append_element({"type": "baslik", "val": str(metin)})
    return True

def yazi(metin, stil="normal"):
    if isinstance(stil, dict):
        style_val = stil
    else:
        style_val = str(stil)
    _append_element({"type": "yazi", "val": str(metin), "style": style_val})
    return True

def buton(metin, mesaj=""):
    if callable(mesaj):
        func_name = getattr(mesaj, '__name__', 'buton_olay')
        event_name = f"click_{func_name}"
        plugin_api.plugin.event_ekle(event_name, mesaj)
        action_val = event_name
    else:
        action_val = str(mesaj)
    _append_element({"type": "buton", "val": str(metin), "action": action_val})
    return True

def girdi(etiket, degisken_adi=""):
    _append_element({"type": "girdi", "val": str(etiket), "var_name": str(degisken_adi)})
    return True

def kart(baslik_metni, icerik_metni):
    _append_element({"type": "kart", "title": str(baslik_metni), "content": str(icerik_metni)})
    return True

def resim(url):
    _append_element({"type": "resim", "val": str(url)})
    return True

def liste(elemanlar):
    elems = [str(x) for x in elemanlar] if isinstance(elemanlar, list) else [str(elemanlar)]
    _append_element({"type": "liste", "items": elems})
    return True

def ilerleme(yuzde):
    _append_element({"type": "ilerleme", "val": int(yuzde)})
    return True

def anahtar(etiket, aktif=False):
    _append_element({"type": "anahtar", "val": str(etiket), "checked": bool(aktif)})
    return True

def arka_plan(renk):
    plugin_api.plugin.gui_elements.append({"type": "arka_plan", "val": str(renk)})
    return True

# New elements requested by the user:
def video(url):
    _append_element({"type": "video", "val": str(url)})
    return True

def kamera():
    _append_element({"type": "kamera"})
    return True

def harita(konum, boylam=None):
    if boylam is not None:
        _append_element({"type": "harita", "lat": float(konum), "lng": float(boylam)})
    else:
        _append_element({"type": "harita", "val": str(konum)})
    return True

def ikon(isim):
    _append_element({"type": "ikon", "val": str(isim)})
    return True

def menu(elemanlar):
    elems = [str(x) for x in elemanlar] if isinstance(elemanlar, list) else [str(elemanlar)]
    _append_element({"type": "menu", "items": elems})
    return True

def sekme(elemanlar, aktif_sekme_indeksi=0):
    elems = [str(x) for x in elemanlar] if isinstance(elemanlar, list) else [str(elemanlar)]
    _append_element({"type": "sekme", "items": elems, "active_index": int(aktif_sekme_indeksi)})
    return True

def kaydirici(etiket, min_deger=0, max_deger=100, varsayilan=50):
    _append_element({
        "type": "kaydirici",
        "val": str(etiket),
        "min": int(min_deger),
        "max": int(max_deger),
        "value": int(varsayilan)
    })
    return True

def resim_yukle(etiket):
    _append_element({"type": "resim_yukle", "val": str(etiket)})
    return True

def ses(url):
    _append_element({"type": "ses", "val": str(url)})
    return True


def olay_ekle(olay_adi, fonksiyon):
    plugin_api.plugin.event_ekle(str(olay_adi), fonksiyon)
    return True

def tiklandiginda(olay_adi, fonksiyon):
    plugin_api.plugin.event_ekle(str(olay_adi), fonksiyon)
    return True

def olay_tetikle(olay_adi, *args):
    plugin_api.plugin.trigger_event(str(olay_adi), *args)
    return True


def ornekler(sayfa_adi):
    sayfa_key = str(sayfa_adi).lower().strip()
    if sayfa_key == "profil":
        temizle()
        arka_plan("gok_mavisi")
        baslik("Profil Bilgileri")
        resim("https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=150&h=150&q=80")
        yazi("Alper Öztürk", "baslik")
        yazi("Yazılım Geliştirici", "alt_baslik")
        kart("Hakkımda", "ÖzDil Türkçe programlama dili ile mobil uygulamalar geliştiren bir retro teknoloji tutkunu.")
        buton("E-Posta Gönder", "E-posta uygulaması açılıyor...")
    elif sayfa_key == "hava_durumu":
        temizle()
        arka_plan("gece_mavisi")
        baslik("Hava Durumu")
        yazi("İstanbul", "baslik")
        yazi("28°C", "derece")
        yazi("Hava Güneşli ve Açık", "alt_baslik")
        kart("Haftalık Tahmin", "Pazartesi: 29°C | Salı: 30°C | Çarşamba: 27°C")
        ilerleme(70)
        yazi("Nem Oranı: %70", "normal")
    elif sayfa_key == "magaza":
        temizle()
        arka_plan("kirli_beyaz")
        baslik("Mobil Mağaza")
        yazi("ÖzDil Özel Ürünleri", "baslik")
        kart("ÖzDil Kupa Bardağı", "Fiyat: 150 TL | Stokta Var")
        buton("Sepete Ekle", "Ürün sepete eklendi! 🛒")
        kart("Retro Klavye", "Fiyat: 1200 TL | Son 2 adet!")
        buton("Sepete Ekle", "Ürün sepete eklendi! 🛒")
    return True

def plugin():
    plugin_api.plugin.fonksiyon_ekle("temizle", temizle)
    plugin_api.plugin.fonksiyon_ekle("sayfa", sayfa)
    plugin_api.plugin.fonksiyon_ekle("sayfa_bitir", sayfa_bitir)
    plugin_api.plugin.fonksiyon_ekle("baslik", baslik)
    plugin_api.plugin.fonksiyon_ekle("yazi", yazi)
    plugin_api.plugin.fonksiyon_ekle("buton", buton)
    plugin_api.plugin.fonksiyon_ekle("girdi", girdi)
    plugin_api.plugin.fonksiyon_ekle("kart", kart)
    plugin_api.plugin.fonksiyon_ekle("resim", resim)
    plugin_api.plugin.fonksiyon_ekle("liste", liste)
    plugin_api.plugin.fonksiyon_ekle("ilerleme", ilerleme)
    plugin_api.plugin.fonksiyon_ekle("anahtar", anahtar)
    plugin_api.plugin.fonksiyon_ekle("arka_plan", arka_plan)
    
    # New ones
    plugin_api.plugin.fonksiyon_ekle("video", video)
    plugin_api.plugin.fonksiyon_ekle("kamera", kamera)
    plugin_api.plugin.fonksiyon_ekle("harita", harita)
    plugin_api.plugin.fonksiyon_ekle("ikon", ikon)
    plugin_api.plugin.fonksiyon_ekle("menu", menu)
    plugin_api.plugin.fonksiyon_ekle("sekme", sekme)
    plugin_api.plugin.fonksiyon_ekle("kaydirici", kaydirici)
    plugin_api.plugin.fonksiyon_ekle("resim_yukle", resim_yukle)
    plugin_api.plugin.fonksiyon_ekle("ses", ses)

    plugin_api.plugin.fonksiyon_ekle("olay_ekle", olay_ekle)
    plugin_api.plugin.fonksiyon_ekle("tiklandiginda", tiklandiginda)
    plugin_api.plugin.fonksiyon_ekle("olay_tetikle", olay_tetikle)
    plugin_api.plugin.fonksiyon_ekle("tetikle", olay_tetikle)
    plugin_api.plugin.fonksiyon_ekle("ornekler", ornekler)
    return {
        "temizle": temizle,
        "sayfa": sayfa,
        "sayfa_bitir": sayfa_bitir,
        "baslik": baslik,
        "yazi": yazi,
        "buton": buton,
        "girdi": girdi,
        "kart": kart,
        "resim": resim,
        "liste": liste,
        "ilerleme": ilerleme,
        "anahtar": anahtar,
        "arka_plan": arka_plan,
        "video": video,
        "kamera": kamera,
        "harita": harita,
        "ikon": ikon,
        "menu": menu,
        "sekme": sekme,
        "kaydirici": kaydirici,
        "resim_yukle": resim_yukle,
        "ses": ses,
        "olay_ekle": olay_ekle,
        "tiklandiginda": tiklandiginda,
        "olay_tetikle": olay_tetikle,
        "tetikle": olay_tetikle,
        "ornekler": ornekler
    }
"""
        }
    }
}

def generate_sha256(content_dict):
    """
    Paket içeriğindeki tüm dosyaları birleştirerek SHA256 imzası üretir.
    """
    sha = hashlib.sha256()
    for filename in sorted(content_dict.keys()):
        sha.update(filename.encode('utf-8'))
        sha.update(content_dict[filename].encode('utf-8'))
    return sha.hexdigest()

# İmza eklemesi yapılmış repository listesini dinamik olarak hazırla
for name, data in REPOSITORY_PACKAGES.items():
    data["meta"]["imza"] = generate_sha256(data["files"])

def get_repository_json():
    """
    Merkezi repository.json çıktısı üretir.
    """
    paketler = []
    for name, data in REPOSITORY_PACKAGES.items():
        paketler.append({
            "isim": data["meta"]["isim"],
            "surum": data["meta"]["surum"],
            "yazar": data["meta"]["yazar"],
            "tur": data["meta"]["tur"],
            "aciklama": data["meta"]["aciklama"],
            "izinler": data["meta"]["izinler"],
            "bagimliliklar": data["meta"]["bagimliliklar"],
            "imza": data["meta"]["imza"]
        })
    return {"paketler": paketler}

def fetch_package_data(package_name):
    """
    Repository'den paket içeriğini ve meta verilerini döner.
    """
    return REPOSITORY_PACKAGES.get(package_name.lower().strip())
