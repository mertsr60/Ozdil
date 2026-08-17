# -*- coding: utf-8 -*-
"""
Varyn Paket Deposu (repository.py)
Bu dosya, Varyn paket ekosistemindeki merkezi paket deposunu ve arama/bilgi alma servislerini simüle eder.
"""

import json
import hashlib

# Merkezi Paket Deposu Veritabanı (Simüle edilmiş online depo)
REPOSITORY_PACKAGES = {
    "algoritma": {
        "meta": {
            "isim": "algoritma",
            "surum": "1.1.0",
            "yazar": "varyn_toplulugu",
            "tur": "varyn",
            "aciklama": "Tamamen ÖzDil ile yazılmış ilk kütüphane. Sıralama, arama, istatistik, matematiksel ve sayı dizisi (Fibonacci) algoritmaları içerir.",
            "izinler": [],
            "bagimliliklar": []
        },
        "files": {
            "main.varyn": """# Algoritma Kütüphanesi - 100% ÖzDil ile yazılmış ilk paket!

işlem sirala(dizi):
    değişken n = uzunluk(dizi)
    döngü i içinde aralık(n):
        değişken sinir = n - i - 1
        döngü j içinde aralık(sinir):
            eğer dizi[j] > dizi[j + 1]:
                değişken gecici = dizi[j]
                dizi[j] = dizi[j + 1]
                dizi[j + 1] = gecici
    döndür dizi

işlem ikili_ara(dizi, hedef):
    değişken sol = 0
    değişken sag = uzunluk(dizi) - 1
    iken sol <= sag:
        değişken orta = tam_sayi((sol + sag) / 2)
        eğer dizi[orta] == hedef:
            döndür orta
        değilse:
            eğer dizi[orta] < hedef:
                sol = orta + 1
            değilse:
                sag = orta - 1
    döndür -1

işlem en_buyuk(dizi):
    eğer uzunluk(dizi) == 0:
        döndür boş
    değişken eb = dizi[0]
    döngü eleman içinde dizi:
        eğer eleman > eb:
            eb = eleman
    döndür eb

işlem en_kucuk(dizi):
    eğer uzunluk(dizi) == 0:
        döndür boş
    değişken ek = dizi[0]
    döngü eleman içinde dizi:
        eğer eleman < ek:
            ek = eleman
    döndür ek

işlem toplam(dizi):
    değişken t = 0
    döngü eleman içinde dizi:
        t = t + eleman
    döndür t

işlem ortalama(dizi):
    değişken n = uzunluk(dizi)
    eğer n == 0:
        döndür 0
    değişken t = toplam(dizi)
    döndür t / n

işlem tersine_cevir(dizi):
    değişken n = uzunluk(dizi)
    değişken yeni_dizi = []
    döngü i içinde aralık(n):
        yeni_dizi.ekle(dizi[n - i - 1])
    döndür yeni_dizi

işlem asal_mi(sayi):
    eğer sayi <= 1:
        döndür yanlış
    değişken bolen = 2
    iken bolen * bolen <= sayi:
        eğer sayi % bolen == 0:
            döndür yanlış
        bolen = bolen + 1
    döndür doğru

işlem ebob(a, b):
    iken b != 0:
        değişken gecici = b
        b = a % b
        a = gecici
    döndür a

işlem ekok(a, b):
    eğer a == 0 veya b == 0:
        döndür 0
    değişken carpim = a * b
    eğer carpim < 0:
        carpim = carpim * -1
    döndür carpim / ebob(a, b)

işlem benzersizler(dizi):
    değişken sonuc = []
    döngü eleman içinde dizi:
        değişken var_mi = yanlış
        döngü x içinde sonuc:
            eğer x == eleman:
                var_mi = doğru
        eğer değil var_mi:
            sonuc.ekle(eleman)
    döndür sonuc

işlem fibonacci(n):
    eğer n <= 0:
        döndür []
    eğer n == 1:
        döndür [0]
    değişken dizi = [0, 1]
    iken uzunluk(dizi) < n:
        değişken n2 = uzunluk(dizi)
        değişken yeni_eleman = dizi[n2 - 1] + dizi[n2 - 2]
        dizi.ekle(yeni_eleman)
    döndür dizi
"""
        }
    },
    "matematik": {
        "meta": {
            "isim": "matematik",
            "surum": "1.0.0",
            "yazar": "varyn_toplulugu",
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
    # Yeni eklenti API'sini kullanarak fonksiyonları doğrudan Varyn global alanına ekliyoruz
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
            "yazar": "varyn_toplulugu",
            "tur": "varyn",
            "aciklama": "Varyn için konsol tabanlı grafik çizim ve görselleştirme araçları.",
            "izinler": [],
            "bagimliliklar": []
        },
        "files": {
            "grafik.varyn": """# Grafik ve Konsol Çizim Kütüphanesi

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
            "tur": "varyn",
            "aciklama": "Temel yapay zeka ve doğrusal regresyon tahmin modeli, k-means kümeleme, k-NN sınıflandırma ve yapay sinir hücresi simülasyonu.",
            "izinler": [],
            "bagimliliklar": []
        },
        "files": {
            "yapay_zeka.varyn": """# Temel Yapay Zeka Regresyon Modülü

işlem tahmin_et(girdi):
    değişken sonuc = girdi * 2.5 + 4
    yazdır("[Yapay Zeka] Tahmin Modeli Çalıştırıldı.")
    yazdır("[Yapay Zeka] Girdi Değeri: " + metin(girdi))
    yazdır("[Yapay Zeka] Üretilen Tahmin: " + metin(sonuc))
    döndür sonuc

işlem dogrusal_regresyon_egit(x_listesi, y_listesi):
    değişken n = uzunluk(x_listesi)
    değişken sum_x = 0.0
    değişken sum_y = 0.0
    değişken sum_xy = 0.0
    değişken sum_xx = 0.0
    döngü i içinde aralık(n):
        değişken x = x_listesi[i]
        değişken y = y_listesi[i]
        sum_x = sum_x + x
        sum_y = sum_y + y
        sum_xy = sum_xy + (x * y)
        sum_xx = sum_xx + (x * x)
    değişken pay = n * sum_xy - sum_x * sum_y
    değişken payda = n * sum_xx - sum_x * sum_x
    değişken egim = pay / payda
    değişken kesim_noktasi = (sum_y - egim * sum_x) / n
    değişken model = {
        "egim": egim,
        "kesim_noktasi": kesim_noktasi
    }
    döndür model

işlem dogrusal_regresyon_tahmin_et(model, x):
    değişken w = model["egim"]
    değişken b = model["kesim_noktasi"]
    döndür w * x + b

işlem k_ortalama_kumele(veri_noktalari, k, iterasyonlar):
    değişken merkezler = []
    döngü i içinde aralık(k):
        merkezler.ekle(veri_noktalari[i])
        
    döngü iter içinde aralık(iterasyonlar):
        değişken kume_toplamlari = []
        değişken kume_sayilari = []
        döngü i içinde aralık(k):
            değişken boy = uzunluk(merkezler[0])
            değişken t = []
            döngü b içinde aralık(boy):
                t.ekle(0.0)
            kume_toplamlari.ekle(t)
            kume_sayilari.ekle(0)
            
        döngü p içinde veri_noktalari:
            değişken en_yakin_indis = 0
            değişken en_kucuk_uzaklik = -1.0
            
            döngü c_indis içinde aralık(k):
                değişken m = merkezler[c_indis]
                değişken d = 0.0
                döngü dim içinde aralık(uzunluk(p)):
                    değişken fark = p[dim] - m[dim]
                    d = d + (fark * fark)
                eğer en_kucuk_uzaklik == -1.0 veya d < en_kucuk_uzaklik:
                    en_kucuk_uzaklik = d
                    en_yakin_indis = c_indis
            
            kume_sayilari[en_yakin_indis] = kume_sayilari[en_yakin_indis] + 1
            döngü dim içinde aralık(uzunluk(p)):
                kume_toplamlari[en_yakin_indis][dim] = kume_toplamlari[en_yakin_indis][dim] + p[dim]
                
        döngü c_indis içinde aralık(k):
            değişken sayi = kume_sayilari[c_indis]
            eğer sayi > 0:
                döngü dim içinde aralık(uzunluk(merkezler[c_indis])):
                    merkezler[c_indis][dim] = kume_toplamlari[c_indis][dim] / sayi
                    
    değişken sonuc = {
        "merkezler": merkezler
    }
    döndür sonuc

işlem knn_siniflandir(egitim_seti, test_nesnesi, k):
    değişken n = uzunluk(egitim_seti)
    değişken uzakliklar = []
    döngü i içinde aralık(n):
        değişken eleman = egitim_seti[i]
        değişken ozellik = eleman[0]
        değişken etiket = eleman[1]
        
        değişken d = 0.0
        döngü dim içinde aralık(uzunluk(test_nesnesi)):
            değişken fark = test_nesnesi[dim] - ozellik[dim]
            d = d + (fark * fark)
            
        uzakliklar.ekle([d, etiket])
        
    döngü i içinde aralık(uzunluk(uzakliklar)):
        değişken n_u = uzunluk(uzakliklar)
        döngü j içinde aralık(n_u - i - 1):
            eğer uzakliklar[j][0] > uzakliklar[j + 1][0]:
                değişken gecici = uzakliklar[j]
                uzakliklar[j] = uzakliklar[j + 1]
                uzakliklar[j + 1] = gecici
                
    değişken sinir = k
    eğer uzunluk(uzakliklar) < k:
        sinir = uzunluk(uzakliklar)
        
    değişken en_yakin_etiketler = []
    döngü i içinde aralık(sinir):
        en_yakin_etiketler.ekle(uzakliklar[i][1])
        
    değişken en_sik_etiket = boş
    değişken en_yuksek_frekans = 0
    döngü etiket içinde en_yakin_etiketler:
        değişken frekans = 0
        döngü x içinde en_yakin_etiketler:
            eğer x == etiket:
                frekans = frekans + 1
        eğer frekans > en_yuksek_frekans:
            en_yuksek_frekans = frekans
            en_sik_etiket = etiket
            
    döndür en_sik_etiket

işlem yapay_sinir_hucresi(girdiler, agirliklar, sapma, aktivasyon):
    değişken toplam = 0.0
    döngü i içinde aralık(uzunluk(girdiler)):
        toplam = toplam + girdiler[i] * agirliklar[i]
    toplam = toplam + sapma
    
    eğer aktivasyon == "relu":
        eğer toplam < 0:
            döndür 0.0
        değilse:
            döndür toplam
    değilse:
        eğer aktivasyon == "adim" veya aktivasyon == "adım":
            eğer toplam >= 0:
                döndür 1
            değilse:
                döndür 0
                
    döndür toplam
"""
        }
    },
    "tarih_saat": {
        "meta": {
            "isim": "tarih_saat",
            "surum": "1.0.0",
            "yazar": "varyn_toplulugu",
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
            "yazar": "varyn_toplulugu",
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
            "yazar": "varyn_toplulugu",
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
    if plugin_api.plugin.current_page is not None:
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
        func_name = str(mesaj)
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
        kart("Hakkımda", "Varyn Türkçe programlama dili ile mobil uygulamalar geliştiren bir retro teknoloji tutkunu.")
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
        yazi("Varyn Özel Ürünleri", "baslik")
        kart("Varyn Kupa Bardağı", "Fiyat: 150 TL | Stokta Var")
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
    },
    "program": {
        "meta": {
            "isim": "program",
            "surum": "1.0.0",
            "yazar": "varyn_toplulugu",
            "tur": "python",
            "aciklama": "ÖzDil / Varyn ile tam donanımlı masaüstü ve pencere tabanlı grafik programları, form uygulamaları, veri panelleri ve etkileşimli yazılımlar geliştirme kütüphanesi.",
            "izinler": [],
            "bagimliliklar": []
        },
        "files": {
            "main.py": """# Masaüstü & Pencere Programı Geliştirme Kütüphanesi
import plugin_api

def _append_element(elem):
    if plugin_api.plugin.current_program is not None:
        plugin_api.plugin.current_program["elements"].append(elem)
    else:
        pencere_dict = {
            "type": "program_pencere",
            "title": "Varyn Programı",
            "width": 640,
            "height": 480,
            "theme": "koyu",
            "icon": "uygulama",
            "elements": [elem]
        }
        plugin_api.plugin.gui_elements.append(pencere_dict)
        plugin_api.plugin.current_program = pencere_dict

def temizle():
    plugin_api.plugin.gui_elements.clear()
    plugin_api.plugin.current_program = None
    return True

def olustur(baslik="Varyn Programı", genislik=640, yukseklik=480, tema="koyu", ikon="uygulama"):
    pencere_dict = {
        "type": "program_pencere",
        "title": str(baslik),
        "width": int(genislik) if genislik else 640,
        "height": int(yukseklik) if yukseklik else 480,
        "theme": str(tema),
        "icon": str(ikon),
        "elements": []
    }
    plugin_api.plugin.gui_elements.append(pencere_dict)
    plugin_api.plugin.current_program = pencere_dict
    return True

def menu_cubugu(menuler):
    if isinstance(menuler, str):
        menuler = [menuler]
    elem = {"type": "menu_cubugu", "items": [str(m) for m in menuler]}
    _append_element(elem)
    return True

def arac_cubugu(araclar):
    if isinstance(araclar, str):
        araclar = [araclar]
    elem = {"type": "arac_cubugu", "items": [str(a) for a in araclar]}
    _append_element(elem)
    return True

def sekme(sekmeler, aktif=0):
    if isinstance(sekmeler, str):
        sekmeler = [sekmeler]
    elem = {"type": "sekme_grubu", "items": [str(s) for s in sekmeler], "active": int(aktif)}
    _append_element(elem)
    return True

def baslik(metin, alt_yazi="", seviye=1):
    elem = {"type": "program_baslik", "title": str(metin), "subtitle": str(alt_yazi) if alt_yazi else "", "level": int(seviye)}
    _append_element(elem)
    return True

def yazi(metin, stil="normal", hizalama="sol"):
    elem = {"type": "program_yazi", "text": str(metin), "style": str(stil), "align": str(hizalama)}
    _append_element(elem)
    return True

def metin_kutusu(etiket, varsayilan="", ipucu=""):
    elem = {"type": "metin_kutusu", "label": str(etiket), "value": str(varsayilan), "placeholder": str(ipucu) if ipucu else f"{etiket} giriniz..."}
    _append_element(elem)
    return True

def sayi_kutusu(etiket, min_deger=0, max_deger=100, varsayilan=0):
    elem = {"type": "sayi_kutusu", "label": str(etiket), "min": float(min_deger), "max": float(max_deger), "value": float(varsayilan)}
    _append_element(elem)
    return True

def buton(yazi, eylem="", stil="birincil", ikon=""):
    elem = {"type": "program_buton", "label": str(yazi), "action": str(eylem) if eylem else str(yazi), "style": str(stil), "icon": str(ikon) if ikon else ""}
    _append_element(elem)
    return True

def onay_kutusu(etiket, secili_mi=False):
    elem = {"type": "onay_kutusu", "label": str(etiket), "checked": bool(secili_mi)}
    _append_element(elem)
    return True

def secim_kutusu(etiket, secenekler=None, varsayilan=None):
    if secenekler is None:
        secenekler = []
    elem = {"type": "secim_kutusu", "label": str(etiket), "options": [str(s) for s in secenekler], "selected": str(varsayilan) if varsayilan else (str(secenekler[0]) if secenekler else "")}
    _append_element(elem)
    return True

def kaydirici(etiket, min_deger=0, max_deger=100, deger=50):
    elem = {"type": "program_kaydirici", "label": str(etiket), "min": float(min_deger), "max": float(max_deger), "value": float(deger)}
    _append_element(elem)
    return True

def kart(baslik, icerik="", rozet="", ikon=""):
    elem = {"type": "program_kart", "title": str(baslik), "content": str(icerik), "badge": str(rozet) if rozet else "", "icon": str(ikon) if ikon else ""}
    _append_element(elem)
    return True

def tablo(kolonlar, satirlar):
    elem = {"type": "program_tablo", "headers": [str(k) for k in kolonlar], "rows": [[str(cell) for cell in row] for row in satirlar]}
    _append_element(elem)
    return True

def kod_kutusu(kod, dil="varyn"):
    elem = {"type": "kod_kutusu", "code": str(kod), "lang": str(dil)}
    _append_element(elem)
    return True

def terminal_kutusu(ciktilar=None):
    if ciktilar is None:
        ciktilar = ["[Sistem] Uygulama çekirdeği başlatıldı.", "[Sistem] Hazır ve dinlemede..."]
    elif isinstance(ciktilar, str):
        ciktilar = [ciktilar]
    elem = {"type": "terminal_kutusu", "logs": [str(log) for log in ciktilar]}
    _append_element(elem)
    return True

def ilerleme(yuzde, durum=""):
    elem = {"type": "program_ilerleme", "percent": max(0, min(100, float(yuzde))), "status": str(durum)}
    _append_element(elem)
    return True

def durum_cubugu(sol_mesaj="Hazır", sag_bilgi="v1.0.0 | UTF-8", durum="tamam"):
    elem = {"type": "durum_cubugu", "left": str(sol_mesaj), "right": str(sag_bilgi), "status": str(durum)}
    _append_element(elem)
    return True

def bildirim(baslik, mesaj, tip="bilgi"):
    elem = {"type": "program_bildirim", "title": str(baslik), "message": str(mesaj), "alert_type": str(tip)}
    _append_element(elem)
    return True

def mesaj_kutusu(baslik, mesaj):
    return bildirim(baslik, mesaj, "bilgi")

def ornek_program(program_turu):
    temizle()
    if program_turu == "hesap_makinesi":
        olustur("Varyn Hesap Makinesi v1.0", 420, 540, "karanlik", "hesap")
        menu_cubugu(["Görünüm", "Düzenle", "Yardım"])
        baslik("Hesap Makinesi Pro", "Varyn Sanal Makine Tabanlı Hesaplayıcı")
        metin_kutusu("Sonuç Ekranı", "0", "0")
        kart("İşlem Hafızası", "Son işlem: 125 x 8 = 1000", "Aktif", "hesap")
        arac_cubugu(["C", "(", ")", "/", "7", "8", "9", "*", "4", "5", "6", "-", "1", "2", "3", "+", "0", ".", "="])
        durum_cubugu("Hesaplayıcı Hazır", "Standart Mod", "tamam")
    elif program_turu == "not_defteri":
        olustur("Varyn Not Defteri", 680, 520, "aydinlik", "dosya")
        menu_cubugu(["Dosya", "Düzenle", "Biçim", "Görünüm", "Yardım"])
        arac_cubugu(["Yeni Not", "Kaydet", "Dışa Aktar", "Yazdır"])
        metin_kutusu("Başlık", "Proje Planı", "Not başlığı girin...")
        kod_kutusu("# Bugün Yapılacaklar Listesi:\n1. Varyn dilinde yeni kütüphane oluştur\n2. Masaüstü GUI testlerini tamamla\n3. varynpip deposunu güncelle", "markdown")
        durum_cubugu("Satır: 4 | Sütun: 1", "Karakter: 142 | UTF-8", "tamam")
    elif program_turu == "gorev_yoneticisi":
        olustur("Varyn Görev & Süreç Yöneticisi", 720, 520, "karanlik", "sistem")
        menu_cubugu(["İşlemler", "Performans", "Uygulama Geçmişi", "Hizmetler"])
        kart("CPU Kullanımı: %18", "4 Çekirdek Aktif | 3.4 GHz", "%18", "islemci")
        kart("Bellek (RAM): 2.4 GB / 8.0 GB", "Kullanılabilir: 5.6 GB", "%30", "bellek")
        ilerleme(30, "Sistem kaynakları optimum düzeyde")
        tablo(["İşlem Adı", "PID", "Durum", "CPU %", "Bellek"], [
            ["varyn_vm_worker", "4812", "Çalışıyor", "%12.4", "45 MB"],
            ["grafik_renderer", "4815", "Çalışıyor", "%4.2", "82 MB"],
            ["paket_denetleyici", "4820", "Beklemede", "%0.1", "12 MB"]
        ])
        buton("Seçili Görevi Sonlandır", "gorev_sonlandir", "tehlike", "cop")
        durum_cubugu("3 İşlem Çalışıyor", "Sistem Güvenli", "tamam")
    elif program_turu == "veri_tablosu":
        olustur("Envanter ve Satış Yönetim Programı", 740, 540, "karanlik", "tablo")
        menu_cubugu(["Dosya", "Kayıtlar", "Raporlar", "Veri Tabanı", "Yardım"])
        arac_cubugu(["Yeni Kayıt", "Dışa Aktar (CSV)", "Filtrele", "Yenile"])
        kart("Toplam Ciro", "148.500 ₺", "+%14 Bu Hafta", "para")
        kart("Toplam Stok", "1.240 Adet", "23 Kategori", "kutu")
        tablo(["Barkod", "Ürün Adı", "Kategori", "Birim Fiyat", "Stok Durumu"], [
            ["869001", "Varyn Ultra Laptop", "Bilgisayar", "32.500 ₺", "18 Adet"],
            ["869002", "Mekanik RGB Klavye", "Donanım", "1.450 ₺", "64 Adet"],
            ["869003", "Kablosuz Optik Mouse", "Aksesuar", "420 ₺", "120 Adet"],
            ["869004", "27 inç 144Hz Monitör", "Ekran", "7.800 ₺", "9 Adet"]
        ])
        durum_cubugu("4 Kayıt Gösteriliyor", "Bağlantı: Çevrimiçi", "tamam")
    else:
        olustur("Varyn Kontrol Paneli", 640, 480, "karanlik")
        baslik("Sistem ve Uygulama Paneli", "Tüm modüller aktif")
        yazi("Uygulama başarıyla yüklendi.", "basarili")
        durum_cubugu("Hazır", "v1.0.0", "tamam")
    return True

def olay_ekle(olay_adi, fonksiyon):
    plugin_api.plugin.event_ekle(str(olay_adi), fonksiyon)
    return True

def olay_tetikle(olay_adi, veri=None):
    plugin_api.plugin.trigger_event(str(olay_adi), veri)
    return True

def plugin():
    apis = {
        "olustur": olustur,
        "temizle": temizle,
        "menu_cubugu": menu_cubugu,
        "arac_cubugu": arac_cubugu,
        "sekme": sekme,
        "baslik": baslik,
        "yazi": yazi,
        "metin_kutusu": metin_kutusu,
        "sayi_kutusu": sayi_kutusu,
        "buton": buton,
        "onay_kutusu": onay_kutusu,
        "secim_kutusu": secim_kutusu,
        "kaydirici": kaydirici,
        "kart": kart,
        "tablo": tablo,
        "kod_kutusu": kod_kutusu,
        "terminal_kutusu": terminal_kutusu,
        "ilerleme": ilerleme,
        "durum_cubugu": durum_cubugu,
        "bildirim": bildirim,
        "mesaj_kutusu": mesaj_kutusu,
        "ornek_program": ornek_program,
        "olay_ekle": olay_ekle,
        "olay_dinle": olay_ekle,
        "olay_tetikle": olay_tetikle
    }
    for k, v in apis.items():
        plugin_api.plugin.fonksiyon_ekle(k, v)
    return apis
"""
        }
    },
    "veritabani": {
        "meta": {
            "isim": "veritabani",
            "surum": "1.0.0",
            "yazar": "varyn_toplulugu",
            "tur": "python",
            "aciklama": "ÖzDil / Varyn için anahtar-değer ve JSON tabanlı bellek içi veritabanı kütüphanesi.",
            "izinler": [],
            "bagimliliklar": []
        },
        "files": {
            "main.py": """# Veritabanı ve Anahtar-Değer Deposu Kütüphanesi
import json

_DB_STORE = {}

def baglan(db_adi="varsayilan"):
    if db_adi not in _DB_STORE:
        _DB_STORE[db_adi] = {}
    return db_adi

def koy(anahtar, deger, db_adi="varsayilan"):
    if db_adi not in _DB_STORE:
        _DB_STORE[db_adi] = {}
    _DB_STORE[db_adi][str(anahtar)] = deger
    return True

def al(anahtar, varsayilan=None, db_adi="varsayilan"):
    if db_adi in _DB_STORE:
        return _DB_STORE[db_adi].get(str(anahtar), varsayilan)
    return varsayilan

def sil(anahtar, db_adi="varsayilan"):
    if db_adi in _DB_STORE and str(anahtar) in _DB_STORE[db_adi]:
        del _DB_STORE[db_adi][str(anahtar)]
        return True
    return False

def tumunu_getir(db_adi="varsayilan"):
    if db_adi in _DB_STORE:
        return dict(_DB_STORE[db_adi])
    return {}

def temizle(db_adi="varsayilan"):
    if db_adi in _DB_STORE:
        _DB_STORE[db_adi].clear()
        return True
    return False

def plugin():
    return {
        "veritabani_baglan": baglan,
        "veritabani_koy": koy,
        "veritabani_al": al,
        "veritabani_sil": sil,
        "veritabani_tumunu_getir": tumunu_getir,
        "veritabani_temizle": temizle
    }
"""
        }
    },
    "ag_istemci": {
        "meta": {
            "isim": "ag_istemci",
            "surum": "1.0.0",
            "yazar": "ag_uzmani",
            "tur": "python",
            "aciklama": "HTTP/HTTPS istekleri gönderme, REST API etkileşimi ve veri çekme kütüphanesi.",
            "izinler": ["ag"],
            "bagimliliklar": []
        },
        "files": {
            "main.py": """# Ağ İstemcisi ve REST API Kütüphanesi
import urllib.request
import json

def get_iste(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Varyn-HTTP/1.0"})
    with urllib.request.urlopen(req, timeout=5) as resp:
        return resp.read().decode("utf-8")

def post_iste(url, veri_dict):
    data = json.dumps(veri_dict).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json", "User-Agent": "Varyn-HTTP/1.0"}
    )
    with urllib.request.urlopen(req, timeout=5) as resp:
        return resp.read().decode("utf-8")

def json_coz(metin):
    try:
        return json.loads(metin)
    except Exception:
        return None

def plugin():
    return {
        "ag_get_iste": get_iste,
        "ag_post_iste": post_iste,
        "ag_json_coz": json_coz
    }
"""
        }
    },
    "sifreleme_araclari": {
        "meta": {
            "isim": "sifreleme_araclari",
            "surum": "1.0.0",
            "yazar": "guvenlik_ekibi",
            "tur": "python",
            "aciklama": "Güvenli karma fonksiyonları (SHA256, MD5), Base64 dönüştürme ve Sezar şifreleme araçları.",
            "izinler": [],
            "bagimliliklar": []
        },
        "files": {
            "main.py": """# Şifreleme ve Kriptografi Yardımcı Araçları
import hashlib
import base64

def sha256_hesapla(metin):
    return hashlib.sha256(str(metin).encode("utf-8")).hexdigest()

def md5_hesapla(metin):
    return hashlib.md5(str(metin).encode("utf-8")).hexdigest()

def base64_kodla(metin):
    return base64.b64encode(str(metin).encode("utf-8")).decode("utf-8")

def base64_coz(kodlanmis_metin):
    try:
        return base64.b64decode(str(kodlanmis_metin).encode("utf-8")).decode("utf-8")
    except Exception:
        return None

def sezar_sifrele(metin, anahtar=3):
    sonuc = []
    for char in str(metin):
        if char.isalpha():
            base = ord("A") if char.isupper() else ord("a")
            sonuc.append(chr((ord(char) - base + int(anahtar)) % 26 + base))
        else:
            sonuc.append(char)
    return "".join(sonuc)

def sezar_coz(metin, anahtar=3):
    return sezar_sifrele(metin, -int(anahtar))

def plugin():
    return {
        "sha256_hesapla": sha256_hesapla,
        "md5_hesapla": md5_hesapla,
        "base64_kodla": base64_kodla,
        "base64_coz": base64_coz,
        "sezar_sifrele": sezar_sifrele,
        "sezar_coz": sezar_coz
    }
"""
        }
    },
    "ses_muzik": {
        "meta": {
            "isim": "ses_muzik",
            "surum": "1.0.0",
            "yazar": "muzik_studyosu",
            "tur": "python",
            "aciklama": "Ses frekansı hesaplama, nota frekans eşleme, bpm ve ritim zamanlayıcı simülatörü.",
            "izinler": [],
            "bagimliliklar": []
        },
        "files": {
            "main.py": """# Ses ve Müzik Frekans/Ritim Kütüphanesi
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
"""
        }
    },
    "muhasebe": {
        "meta": {
            "isim": "muhasebe",
            "surum": "1.0.0",
            "yazar": "finans_ekibi",
            "tur": "python",
            "aciklama": "Vergi (KDV, Gelir Vergisi), net/brüt maaş, zam ve fatura hesaplama kütüphanesi.",
            "izinler": [],
            "bagimliliklar": []
        },
        "files": {
            "main.py": """# Finansal Muhasebe ve Vergi Hesaplama Kütüphanesi

def kdv_hesapla(tutar, oran=20):
    kdv_tutari = (float(tutar) * float(oran)) / 100.0
    toplam = float(tutar) + kdv_tutari
    return {
        "ham_tutar": float(tutar),
        "kdv_orani": float(oran),
        "kdv_tutari": round(kdv_tutari, 2),
        "toplam_tutar": round(toplam, 2)
    }

def brutten_nete_maas(brut_maas, sgk_orani=14, issizlik_orani=1, gelir_vergisi_orani=15):
    brut = float(brut_maas)
    sgk = (brut * sgk_orani) / 100.0
    issizlik = (brut * issizlik_orani) / 100.0
    matrah = brut - (sgk + issizlik)
    gelir_vergisi = (matrah * gelir_vergisi_orani) / 100.0
    damga_vergisi = (brut * 0.759) / 100.0
    kesintiler_toplami = sgk + issizlik + gelir_vergisi + damga_vergisi
    net_maas = brut - kesintiler_toplami
    return {
        "brut_maas": round(brut, 2),
        "kesintiler_toplami": round(kesintiler_toplami, 2),
        "net_maas": round(net_maas, 2)
    }

def zam_hesapla(mevcut_tutar, zam_orani):
    arti = (float(mevcut_tutar) * float(zam_orani)) / 100.0
    yeni_tutar = float(mevcut_tutar) + arti
    return {
        "eski_tutar": float(mevcut_tutar),
        "zam_miktari": round(arti, 2),
        "yeni_tutar": round(yeni_tutar, 2)
    }

def plugin():
    return {
        "kdv_hesapla": kdv_hesapla,
        "brutten_nete_maas": brutten_nete_maas,
        "zam_hesapla": zam_hesapla
    }
"""
        }
    },
    "fizik": {
        "meta": {
            "isim": "fizik",
            "surum": "1.0.0",
            "yazar": "bilim_toplulugu",
            "tur": "python",
            "aciklama": "2D ve 3D temel fizik, hareket denklemleri, serbest düşme, atışlar ve enerji simülasyonu.",
            "izinler": [],
            "bagimliliklar": []
        },
        "files": {
            "main.py": """# Temel Fizik ve Hareket Denklemleri Kütüphanesi
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
"""
        }
    },
    "geometri": {
        "meta": {
            "isim": "geometri",
            "surum": "1.0.0",
            "yazar": "matematik_kulubu",
            "tur": "python",
            "aciklama": "2D Alan/Çevre ve 3D Hacim/Yüzey Alanı hesaplama kütüphanesi.",
            "izinler": [],
            "bagimliliklar": []
        },
        "files": {
            "main.py": """# Geometri ve Alan/Hacim Hesaplama Kütüphanesi
import math

def ucgen_alani(taban, yukseklik):
    return round(0.5 * float(taban) * float(yukseklik), 2)

def daire_alani(yaricap):
    r = float(yaricap)
    return round(math.pi * (r ** 2), 2)

def daire_cevresi(yaricap):
    r = float(yaricap)
    return round(2 * math.pi * r, 2)

def hipotenus(a, b):
    return round(math.sqrt((float(a) ** 2) + (float(b) ** 2)), 2)

def kure_hacmi(yaricap):
    r = float(yaricap)
    return round((4.0 / 3.0) * math.pi * (r ** 3), 2)

def silindir_hacmi(yaricap, yukseklik):
    r = float(yaricap)
    h = float(yukseklik)
    return round(math.pi * (r ** 2) * h, 2)

def plugin():
    return {
        "ucgen_alani": ucgen_alani,
        "daire_alani": daire_alani,
        "daire_cevresi": daire_cevresi,
        "hipotenus": hipotenus,
        "kure_hacmi": kure_hacmi,
        "silindir_hacmi": silindir_hacmi
    }
"""
        }
    },
    "otomasyon": {
        "meta": {
            "isim": "otomasyon",
            "surum": "1.0.0",
            "yazar": "sistem_otomasyonu",
            "tur": "python",
            "aciklama": "Zamanlanmış görevler, kronometre, zamanlayıcı ve günlük (logger) otomasyon araçları.",
            "izinler": [],
            "bagimliliklar": []
        },
        "files": {
            "main.py": """# İş Otomasyonu ve Günlük Tutma Kütüphanesi
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
"""
        }
    },
    "lokasyon": {
        "meta": {
            "isim": "lokasyon",
            "surum": "1.0.0",
            "yazar": "cografi_bilgiler",
            "tur": "python",
            "aciklama": "Coğrafi koordinatlar, Haversine mesafe hesaplama ve şehir bulucu kütüphanesi.",
            "izinler": [],
            "bagimliliklar": []
        },
        "files": {
            "main.py": """# Coğrafi Konum ve Mesafe Hesaplama Kütüphanesi
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
"""
        }
    },
    "donusturucu": {
        "meta": {
            "isim": "donusturucu",
            "surum": "1.0.0",
            "yazar": "donusum_ekibi",
            "tur": "python",
            "aciklama": "Sıcaklık (C, F, K), uzunluk, ağırlık, alan ve dijital veri boyutu dönüştürme kütüphanesi.",
            "izinler": [],
            "bagimliliklar": []
        },
        "files": {
            "main.py": """# Birim Dönüştürücü Kütüphanesi

def celcius_fahrenheit(c):
    return round((float(c) * 9.0 / 5.0) + 32.0, 2)

def fahrenheit_celcius(f):
    return round((float(f) - 32.0) * 5.0 / 9.0, 2)

def celcius_kelvin(c):
    return round(float(c) + 273.15, 2)

def km_mil(km):
    return round(float(km) * 0.621371, 2)

def mil_km(mil):
    return round(float(mil) / 0.621371, 2)

def kg_lbs(kg):
    return round(float(kg) * 2.20462, 2)

def lbs_kg(lbs):
    return round(float(lbs) / 2.20462, 2)

def bayt_donustur(bayt_sayisi, hedef_birim="MB"):
    b = float(bayt_sayisi)
    birim = str(hedef_birim).upper()
    if birim == "KB":
        return round(b / 1024.0, 2)
    elif birim == "MB":
        return round(b / (1024.0 ** 2), 2)
    elif birim == "GB":
        return round(b / (1024.0 ** 3), 2)
    elif birim == "TB":
        return round(b / (1024.0 ** 4), 2)
    return b

def plugin():
    return {
        "celcius_fahrenheit": celcius_fahrenheit,
        "fahrenheit_celcius": fahrenheit_celcius,
        "celcius_kelvin": celcius_kelvin,
        "km_mil": km_mil,
        "mil_km": mil_km,
        "kg_lbs": kg_lbs,
        "lbs_kg": lbs_kg,
        "bayt_donustur": bayt_donustur
    }
"""
        }
    },

    "kuyruk_yigin": {
        "meta": {
            "isim": "kuyruk_yigin",
            "surum": "1.0.0",
            "yazar": "varyn_toplulugu",
            "tur": "varyn",
            "aciklama": "Saf Varyn ile yazılmış Yığın (Stack), Kuyruk (Queue) ve parantez dengeleme veri yapıları kütüphanesi.",
            "izinler": [],
            "bagimliliklar": []
},
        "files": {
            "main.varyn": """# Kuyruk ve Yığın Veri Yapıları Kütüphanesi - %100 Saf Varyn

işlem yigin_olustur():
    döndür []

işlem yigin_ekle(yigin, eleman):
    yigin.ekle(eleman)
    döndür yigin

işlem yigin_cikar(yigin):
    değişken n = uzunluk(yigin)
    eğer n == 0:
        döndür boş
    değişken son_indis = n - 1
    değişken son_eleman = yigin[son_indis]
    değişken yeni_yigin = []
    döngü i içinde aralık(son_indis):
        yeni_yigin.ekle(yigin[i])
    döndür son_eleman

işlem yigin_bak(yigin):
    değişken n = uzunluk(yigin)
    eğer n == 0:
        döndür boş
    döndür yigin[n - 1]

işlem yigin_bos_mu(yigin):
    döndür uzunluk(yigin) == 0

işlem kuyruk_olustur():
    döndür []

işlem kuyruk_ekle(kuyruk, eleman):
    kuyruk.ekle(eleman)
    döndür kuyruk

işlem kuyruk_cikar(kuyruk):
    değişken n = uzunluk(kuyruk)
    eğer n == 0:
        döndür boş
    değişken ilk = kuyruk[0]
    değişken yeni_kuyruk = []
    döngü i içinde aralık(1, n):
        yeni_kuyruk.ekle(kuyruk[i])
    döndür ilk

işlem kuyruk_bak(kuyruk):
    eğer uzunluk(kuyruk) == 0:
        döndür boş
    döndür kuyruk[0]

işlem kuyruk_bos_mu(kuyruk):
    döndür uzunluk(kuyruk) == 0

işlem parantez_dengeli_mi(ifade):
    değişken yigin = []
    döngü i içinde aralık(uzunluk(ifade)):
        değişken k = ifade[i]
        eğer k == "(" veya k == "[" veya k == "{":
            yigin.ekle(k)
        değilse_eğer k == ")" veya k == "]" veya k == "}":
            eğer uzunluk(yigin) == 0:
                döndür yanlış
            değişken son = yigin[uzunluk(yigin) - 1]
            değişken uygun = yanlış
            eğer k == ")" ve son == "(":
                uygun = doğru
            değilse_eğer k == "]" ve son == "[":
                uygun = doğru
            değilse_eğer k == "}" ve son == "{":
                uygun = doğru
            eğer değil uygun:
                döndür yanlış
            değişken n_y = uzunluk(yigin)
            değişken temp = []
            döngü j içinde aralık(n_y - 1):
                temp.ekle(yigin[j])
            yigin = temp
    döndür uzunluk(yigin) == 0
"""
        }
    },
    "matris": {
        "meta": {
            "isim": "matris",
            "surum": "1.0.0",
            "yazar": "varyn_toplulugu",
            "tur": "varyn",
            "aciklama": "Saf Varyn ile yazılmış Matris ve Lineer Cebir işlemleri (toplama, çarpma, transpoz, determinant, birim matris).",
            "izinler": [],
            "bagimliliklar": []
},
        "files": {
            "main.varyn": """# Matris ve Lineer Cebir Kütüphanesi - %100 Saf Varyn

işlem matris_olustur(satir, sutun, varsayilan):
    değişken m = []
    döngü i içinde aralık(satir):
        değişken s = []
        döngü j içinde aralık(sutun):
            s.ekle(varsayilan)
        m.ekle(s)
    döndür m

işlem birim_matris(boyut):
    değişken m = []
    döngü i içinde aralık(boyut):
        değişken s = []
        döngü j içinde aralık(boyut):
            eğer i == j:
                s.ekle(1)
            değilse:
                s.ekle(0)
        m.ekle(s)
    döndür m

işlem matris_topla(m1, m2):
    değişken satir = uzunluk(m1)
    değişken sutun = uzunluk(m1[0])
    değişken sonuc = []
    döngü i içinde aralık(satir):
        değişken satir_dizi = []
        döngü j içinde aralık(sutun):
            satir_dizi.ekle(m1[i][j] + m2[i][j])
        sonuc.ekle(satir_dizi)
    döndür sonuc

işlem matris_cikar(m1, m2):
    değişken satir = uzunluk(m1)
    değişken sutun = uzunluk(m1[0])
    değişken sonuc = []
    döngü i içinde aralık(satir):
        değişken satir_dizi = []
        döngü j içinde aralık(sutun):
            satir_dizi.ekle(m1[i][j] - m2[i][j])
        sonuc.ekle(satir_dizi)
    döndür sonuc

işlem skaler_carp(m, katsayi):
    değişken sonuc = []
    döngü i içinde aralık(uzunluk(m)):
        değişken s = []
        döngü j içinde aralık(uzunluk(m[i])):
            s.ekle(m[i][j] * katsayi)
        sonuc.ekle(s)
    döndür sonuc

işlem transpoz_al(m):
    değişken satir = uzunluk(m)
    değişken sutun = uzunluk(m[0])
    değişken t = []
    döngü j içinde aralık(sutun):
        değişken s = []
        döngü i içinde aralık(satir):
            s.ekle(m[i][j])
        t.ekle(s)
    döndür t

işlem matris_carp(m1, m2):
    değişken satir1 = uzunluk(m1)
    değişken sutun1 = uzunluk(m1[0])
    değişken sutun2 = uzunluk(m2[0])
    değişken sonuc = []
    döngü i içinde aralık(satir1):
        değişken s = []
        döngü j içinde aralık(sutun2):
            değişken toplam = 0
            döngü k içinde aralık(sutun1):
                toplam = toplam + (m1[i][k] * m2[k][j])
            s.ekle(toplam)
        sonuc.ekle(s)
    döndür sonuc

işlem determinant_2x2(m):
    döndür (m[0][0] * m[1][1]) - (m[0][1] * m[1][0])

işlem determinant_3x3(m):
    değişken a = m[0][0] * ((m[1][1] * m[2][2]) - (m[1][2] * m[2][1]))
    değişken b = m[0][1] * ((m[1][0] * m[2][2]) - (m[1][2] * m[2][0]))
    değişken c = m[0][2] * ((m[1][0] * m[2][1]) - (m[1][1] * m[2][0]))
    döndür a - b + c

işlem iz_hesapla(m):
    değişken toplam = 0
    değişken n = uzunluk(m)
    döngü i içinde aralık(n):
        toplam = toplam + m[i][i]
    döndür toplam
"""
        }
    },
    "sayi_teorisi": {
        "meta": {
            "isim": "sayi_teorisi",
            "surum": "1.0.0",
            "yazar": "varyn_toplulugu",
            "tur": "varyn",
            "aciklama": "Saf Varyn ile Asal Çarpanlar, Armstrong Sayıları, Mükemmel Sayılar, Collatz Dizisi ve Pascal Üçgeni.",
            "izinler": [],
            "bagimliliklar": []
},
        "files": {
            "main.varyn": """# Sayı Teorisi ve Matematiksel Diziler Kütüphanesi - %100 Saf Varyn

işlem asal_carpanlar(n):
    değişken carpanlar = []
    değişken bolen = 2
    değişken sayi = n
    iken sayi > 1:
        iken sayi % bolen == 0:
            carpanlar.ekle(bolen)
            sayi = tam_sayi(sayi / bolen)
        bolen = bolen + 1
        eğer bolen * bolen > sayi ve sayi > 1:
            carpanlar.ekle(sayi)
            dur
    döndür carpanlar

işlem armstrong_mu(n):
    değişken s = metin(n)
    değişken basamak_sayisi = uzunluk(s)
    değişken toplam = 0
    döngü i içinde aralık(basamak_sayisi):
        değişken rakam = tam_sayi(s[i])
        değişken us = 1
        döngü j içinde aralık(basamak_sayisi):
            us = us * rakam
        toplam = toplam + us
    döndür toplam == n

işlem mukemmel_sayi_mi(n):
    eğer n <= 1:
        döndür yanlış
    değişken toplam = 1
    değişken i = 2
    iken i * i <= n:
        eğer n % i == 0:
            toplam = toplam + i
            eğer i * i != n:
                toplam = toplam + tam_sayi(n / i)
        i = i + 1
    döndür toplam == n

işlem collatz_dizisi(baslangic):
    değişken dizi = [baslangic]
    değişken n = baslangic
    iken n > 1:
        eğer n % 2 == 0:
            n = tam_sayi(n / 2)
        değilse:
            n = (3 * n) + 1
        dizi.ekle(n)
    döndür dizi

işlem pascal_ucgeni(satir_sayisi):
    değişken ucgen = []
    döngü i içinde aralık(satir_sayisi):
        değişken satir = []
        döngü j içinde aralık(i + 1):
            eğer j == 0 veya j == i:
                satir.ekle(1)
            değilse:
                değişken ust_satir = ucgen[i - 1]
                satir.ekle(ust_satir[j - 1] + ust_satir[j])
        ucgen.ekle(satir)
    döndür ucgen

işlem palindrom_sayi_mi(n):
    değişken s = metin(n)
    değişken len_s = uzunluk(s)
    döngü i içinde aralık(tam_sayi(len_s / 2)):
        eğer s[i] != s[len_s - 1 - i]:
            döndür yanlış
    döndür doğru

işlem moduler_us(taban, us, mod_degeri):
    değişken sonuc = 1
    değişken t = taban % mod_degeri
    değişken u = us
    iken u > 0:
        eğer u % 2 == 1:
            sonuc = (sonuc * t) % mod_degeri
        u = tam_sayi(u / 2)
        t = (t * t) % mod_degeri
    döndür sonuc
"""
        }
    },
    "agac_graf": {
        "meta": {
            "isim": "agac_graf",
            "surum": "1.0.0",
            "yazar": "varyn_toplulugu",
            "tur": "varyn",
            "aciklama": "Saf Varyn ile İkili Arama Ağacı (BST), Çizge (Graph) temsili, Kenar ekleme ve BFS gezintisi.",
            "izinler": [],
            "bagimliliklar": []
},
        "files": {
            "main.varyn": """# Ağaç ve Çizge Algoritmaları Kütüphanesi - %100 Saf Varyn

işlem bst_dugum_olustur(deger):
    döndür {"deger": deger, "sol": boş, "sag": boş}

işlem bst_ekle(kok, deger):
    eğer kok == boş:
        döndür bst_dugum_olustur(deger)
    eğer deger < kok["deger"]:
        kok["sol"] = bst_ekle(kok["sol"], deger)
    değilse_eğer deger > kok["deger"]:
        kok["sag"] = bst_ekle(kok["sag"], deger)
    döndür kok

işlem bst_ara(kok, hedef):
    eğer kok == boş:
        döndür yanlış
    eğer kok["deger"] == hedef:
        döndür doğru
    eğer hedef < kok["deger"]:
        döndür bst_ara(kok["sol"], hedef)
    değilse:
        döndür bst_ara(kok["sag"], hedef)

işlem bst_sirali_dizi(kok):
    eğer kok == boş:
        döndür []
    değişken sonuc = []
    değişken sol_dizi = bst_sirali_dizi(kok["sol"])
    döngü x içinde sol_dizi:
        sonuc.ekle(x)
    sonuc.ekle(kok["deger"])
    değişken sag_dizi = bst_sirali_dizi(kok["sag"])
    döngü x içinde sag_dizi:
        sonuc.ekle(x)
    döndür sonuc

işlem graf_olustur():
    döndür {}

işlem graf_kenar_ekle(graf, dugum1, dugum2):
    değişken k1 = metin(dugum1)
    değişken k2 = metin(dugum2)
    eğer değil (k1 içinde graf):
        graf[k1] = []
    eğer değil (k2 içinde graf):
        graf[k2] = []
    graf[k1].ekle(k2)
    graf[k2].ekle(k1)
    döndür graf

işlem dugum_derecesi(graf, dugum):
    değişken k = metin(dugum)
    eğer k içinde graf:
        döndür uzunluk(graf[k])
    döndür 0

işlem graf_bfs(graf, baslangic):
    değişken ziyaret_edilen = []
    değişken kuyruk = [metin(baslangic)]
    ziyaret_edilen.ekle(metin(baslangic))
    iken uzunluk(kuyruk) > 0:
        değişken simdiki = kuyruk[0]
        değişken yeni_k = []
        döngü i içinde aralık(1, uzunluk(kuyruk)):
            yeni_k.ekle(kuyruk[i])
        kuyruk = yeni_k
        
        eğer simdiki içinde graf:
            döngü komsu içinde graf[simdiki]:
                değişken var_mi = yanlış
                döngü z içinde ziyaret_edilen:
                    eğer z == komsu:
                        var_mi = doğru
                eğer değil var_mi:
                    ziyaret_edilen.ekle(komsu)
                    kuyruk.ekle(komsu)
    döndür ziyaret_edilen
"""
        }
    },
    "istatistik_pro": {
        "meta": {
            "isim": "istatistik_pro",
            "surum": "1.0.0",
            "yazar": "varyn_toplulugu",
            "tur": "varyn",
            "aciklama": "Saf Varyn ile Varyans, Standart Sapma, Çeyrekler (Q1/Q3), Min-Max Ölçekleme ve Pearson Korelasyonu.",
            "izinler": [],
            "bagimliliklar": []
},
        "files": {
            "main.varyn": """# İleri İstatistik ve Veri Madenciliği Kütüphanesi - %100 Saf Varyn

işlem varyans(dizi):
    değişken n = uzunluk(dizi)
    eğer n <= 1:
        döndür 0.0
    değişken toplam = 0.0
    döngü x içinde dizi:
        toplam = toplam + x
    değişken ortalama = toplam / n
    değişken kareler_toplami = 0.0
    döngü x içinde dizi:
        değişken fark = x - ortalama
        kareler_toplami = kareler_toplami + (fark * fark)
    döndür kareler_toplami / n

işlem standart_sapma(dizi):
    değişken v = varyans(dizi)
    eğer v == 0.0:
        döndür 0.0
    değişken kok = v / 2.0
    döngü i içinde aralık(20):
        kok = (kok + (v / kok)) / 2.0
    döndür kok

işlem dizi_sirala_kopyala(dizi):
    değişken kopya = []
    döngü x içinde dizi:
        kopya.ekle(x)
    değişken n = uzunluk(kopya)
    döngü i içinde aralık(n):
        döngü j içinde aralık(n - i - 1):
            eğer kopya[j] > kopya[j + 1]:
                değişken temp = kopya[j]
                kopya[j] = kopya[j + 1]
                kopya[j + 1] = temp
    döndür kopya

işlem ceyrekler(dizi):
    değişken sirali = dizi_sirala_kopyala(dizi)
    değişken n = uzunluk(sirali)
    eğer n == 0:
        döndür {"q1": 0, "q2": 0, "q3": 0}
    değişken q1_idx = tam_sayi(n * 0.25)
    değişken q2_idx = tam_sayi(n * 0.50)
    değişken q3_idx = tam_sayi(n * 0.75)
    döndür {
        "q1": sirali[q1_idx],
        "q2": sirali[q2_idx],
        "q3": sirali[q3_idx]
    }

işlem ceyrekler_acikligi(dizi):
    değişken c = ceyrekler(dizi)
    döndür c["q3"] - c["q1"]

işlem min_max_olcekle(dizi):
    değişken n = uzunluk(dizi)
    eğer n == 0:
        döndür []
    değişken min_val = dizi[0]
    değişken max_val = dizi[0]
    döngü x içinde dizi:
        eğer x < min_val:
            min_val = x
        eğer x > max_val:
            max_val = x
    değişken aralik_farki = max_val - min_val
    eğer aralik_farki == 0:
        değişken sifir_dizi = []
        döngü i içinde aralık(n):
            sifir_dizi.ekle(0.0)
        döndür sifir_dizi
    değişken sonuc = []
    döngü x içinde dizi:
        sonuc.ekle((x - min_val) / aralik_farki)
    döndür sonuc

işlem pearson_korelasyon(x_dizi, y_dizi):
    değişken n = uzunluk(x_dizi)
    eğer n == 0 veya n != uzunluk(y_dizi):
        döndür 0.0
    değişken sum_x = 0.0
    değişken sum_y = 0.0
    döngü i içinde aralık(n):
        sum_x = sum_x + x_dizi[i]
        sum_y = sum_y + y_dizi[i]
    değişken ort_x = sum_x / n
    değişken ort_y = sum_y / n
    değişken pay = 0.0
    değişken payda_x = 0.0
    değişken payda_y = 0.0
    döngü i içinde aralık(n):
        değişken dx = x_dizi[i] - ort_x
        değişken dy = y_dizi[i] - ort_y
        pay = pay + (dx * dy)
        payda_x = payda_x + (dx * dx)
        payda_y = payda_y + (dy * dy)
    değişken payda = payda_x * payda_y
    eğer payda <= 0.0:
        döndür 0.0
    değişken kok = payda / 2.0
    döngü i içinde aralık(20):
        kok = (kok + (payda / kok)) / 2.0
    döndür pay / kok
"""
        }
    },
    "metin_bicim": {
        "meta": {
            "isim": "metin_bicim",
            "surum": "1.0.0",
            "yazar": "varyn_toplulugu",
            "tur": "varyn",
            "aciklama": "Saf Varyn ile Metin Doldurma (Padding), Ters Çevirme, Kelime Frekansı ve Levenshtein Düzenleme Mesafesi.",
            "izinler": [],
            "bagimliliklar": []
},
        "files": {
            "main.varyn": """# Metin Biçimlendirme, Arama ve Analiz Kütüphanesi - %100 Saf Varyn

işlem metin_doldur_sol(metin_degeri, hedef_uzunluk, dolgu_karakteri):
    değişken s = metin(metin_degeri)
    değişken eksik = hedef_uzunluk - uzunluk(s)
    eğer eksik <= 0:
        döndür s
    değişken on_ek = ""
    döngü i içinde aralık(eksik):
        on_ek = on_ek + dolgu_karakteri
    döndür on_ek + s

işlem metin_doldur_sag(metin_degeri, hedef_uzunluk, dolgu_karakteri):
    değişken s = metin(metin_degeri)
    değişken eksik = hedef_uzunluk - uzunluk(s)
    eğer eksik <= 0:
        döndür s
    değişken son_ek = ""
    döngü i içinde aralık(eksik):
        son_ek = son_ek + dolgu_karakteri
    döndür s + son_ek

işlem kelimelere_ayir(cumle):
    değişken kelimeler = []
    değişken aktif_kelime = ""
    döngü i içinde aralık(uzunluk(cumle)):
        değişken c = cumle[i]
        eğer c == " " veya c == "\t" veya c == "\n":
            eğer uzunluk(aktif_kelime) > 0:
                kelimeler.ekle(aktif_kelime)
                aktif_kelime = ""
        değilse:
            aktif_kelime = aktif_kelime + c
    eğer uzunluk(aktif_kelime) > 0:
        kelimeler.ekle(aktif_kelime)
    döndür kelimeler

işlem kelime_frekansi(cumle):
    değişken kelimeler = kelimelere_ayir(cumle)
    değişken sozluk_veri = {}
    döngü k içinde kelimeler:
        eğer k içinde sozluk_veri:
            sozluk_veri[k] = sozluk_veri[k] + 1
        değilse:
            sozluk_veri[k] = 1
    döndür sozluk_veri

işlem ters_cevir(metin_degeri):
    değişken s = metin(metin_degeri)
    değişken n = uzunluk(s)
    değişken sonuc = ""
    döngü i içinde aralık(n):
        sonuc = sonuc + s[n - 1 - i]
    döndür sonuc

işlem palindrom_metin_mi(metin_degeri):
    değişken s = metin(metin_degeri)
    döndür s == ters_cevir(s)

işlem duzenleme_mesafesi(s1, s2):
    değişken m = uzunluk(s1)
    değişken n = uzunluk(s2)
    değişken dp = []
    döngü i içinde aralık(m + 1):
        değişken satir = []
        döngü j içinde aralık(n + 1):
            satir.ekle(0)
        dp.ekle(satir)
        
    döngü i içinde aralık(m + 1):
        dp[i][0] = i
    döngü j içinde aralık(n + 1):
        dp[0][j] = j
        
    döngü i içinde aralık(1, m + 1):
        döngü j içinde aralık(1, n + 1):
            eğer s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            değilse:
                değişken ekl = dp[i][j - 1]
                değişken sil = dp[i - 1][j]
                değişken deg = dp[i - 1][j - 1]
                değişken min_islem = ekl
                eğer sil < min_islem:
                    min_islem = sil
                eğer deg < min_islem:
                    min_islem = deg
                dp[i][j] = 1 + min_islem
    döndür dp[m][n]
"""
        }
    },
    "kripto_klasik": {
        "meta": {
            "isim": "kripto_klasik",
            "surum": "1.0.0",
            "yazar": "varyn_toplulugu",
            "tur": "varyn",
            "aciklama": "Saf Varyn ile Klasik Şifreleme (ROT13, Atbash, Vigenère, Çit / Rail Fence şifreleme ve çözme).",
            "izinler": [],
            "bagimliliklar": []
},
        "files": {
            "main.varyn": """# Klasik Şifreleme ve Kriptoloji Kütüphanesi - %100 Saf Varyn

işlem harf_indisi(harf):
    değişken alfabe = "abcdefghijklmnopqrstuvwxyz"
    döngü i içinde aralık(26):
        eğer alfabe[i] == harf:
            döndür i
    döndür -1

işlem rot13(metin_degeri):
    değişken alfabe_kucuk = "abcdefghijklmnopqrstuvwxyz"
    değişken alfabe_buyuk = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    değişken sonuc = ""
    döngü i içinde aralık(uzunluk(metin_degeri)):
        değişken c = metin_degeri[i]
        değişken bulundu = yanlış
        döngü j içinde aralık(26):
            eğer alfabe_kucuk[j] == c:
                sonuc = sonuc + alfabe_kucuk[(j + 13) % 26]
                bulundu = doğru
                dur
            değilse_eğer alfabe_buyuk[j] == c:
                sonuc = sonuc + alfabe_buyuk[(j + 13) % 26]
                bulundu = doğru
                dur
        eğer değil bulundu:
            sonuc = sonuc + c
    döndür sonuc

işlem atbash_sifrele(metin_degeri):
    değişken alfabe = "abcdefghijklmnopqrstuvwxyz"
    değişken sonuc = ""
    döngü i içinde aralık(uzunluk(metin_degeri)):
        değişken c = metin_degeri[i]
        değişken idx = harf_indisi(c)
        eğer idx != -1:
            sonuc = sonuc + alfabe[25 - idx]
        değilse:
            sonuc = sonuc + c
    döndür sonuc

işlem vigenere_sifrele(duz_metin, anahtar):
    değişken alfabe = "abcdefghijklmnopqrstuvwxyz"
    değişken sonuc = ""
    değişken anahtar_uzunluk = uzunluk(anahtar)
    değişken k_idx = 0
    döngü i içinde aralık(uzunluk(duz_metin)):
        değişken c = duz_metin[i]
        değişken p_val = harf_indisi(c)
        eğer p_val != -1:
            değişken k_val = harf_indisi(anahtar[k_idx % anahtar_uzunluk])
            değişken yeni_val = (p_val + k_val) % 26
            sonuc = sonuc + alfabe[yeni_val]
            k_idx = k_idx + 1
        değilse:
            sonuc = sonuc + c
    döndür sonuc

işlem vigenere_coz(sifreli_metin, anahtar):
    değişken alfabe = "abcdefghijklmnopqrstuvwxyz"
    değişken sonuc = ""
    değişken anahtar_uzunluk = uzunluk(anahtar)
    değişken k_idx = 0
    döngü i içinde aralık(uzunluk(sifreli_metin)):
        değişken c = sifreli_metin[i]
        değişken c_val = harf_indisi(c)
        eğer c_val != -1:
            değişken k_val = harf_indisi(anahtar[k_idx % anahtar_uzunluk])
            değişken p_val = (c_val - k_val + 26) % 26
            sonuc = sonuc + alfabe[p_val]
            k_idx = k_idx + 1
        değilse:
            sonuc = sonuc + c
    döndür sonuc

işlem cit_sifrele(metin_degeri, ray_sayisi):
    eğer ray_sayisi <= 1:
        döndür metin_degeri
    değişken raylar = []
    döngü i içinde aralık(ray_sayisi):
        raylar.ekle("")
    değişken aktif_ray = 0
    değişken yon = 1
    döngü i içinde aralık(uzunluk(metin_degeri)):
        raylar[aktif_ray] = raylar[aktif_ray] + metin_degeri[i]
        eğer aktif_ray == 0:
            yon = 1
        değilse_eğer aktif_ray == ray_sayisi - 1:
            yon = -1
        aktif_ray = aktif_ray + yon
    değişken sonuc = ""
    döngü i içinde aralık(ray_sayisi):
        sonuc = sonuc + raylar[i]
    döndür sonuc
"""
        }
    },
    "siralama_koleksiyonu": {
        "meta": {
            "isim": "siralama_koleksiyonu",
            "surum": "1.0.0",
            "yazar": "varyn_toplulugu",
            "tur": "varyn",
            "aciklama": "Saf Varyn ile Kabarcık (Bubble), Seçmeli (Selection), Eklemeli (Insertion) ve Saymalı (Counting) sıralama algoritmaları.",
            "izinler": [],
            "bagimliliklar": []
},
        "files": {
            "main.varyn": """# Sıralama ve Arama Koleksiyonu Kütüphanesi - %100 Saf Varyn

işlem kabarcik_sirala(dizi):
    değişken d = []
    döngü x içinde dizi:
        d.ekle(x)
    değişken n = uzunluk(d)
    döngü i içinde aralık(n):
        döngü j içinde aralık(n - i - 1):
            eğer d[j] > d[j + 1]:
                değişken temp = d[j]
                d[j] = d[j + 1]
                d[j + 1] = temp
    döndür d

işlem secmeli_sirala(dizi):
    değişken d = []
    döngü x içinde dizi:
        d.ekle(x)
    değişken n = uzunluk(d)
    döngü i içinde aralık(n):
        değişken min_idx = i
        döngü j içinde aralık(i + 1, n):
            eğer d[j] < d[min_idx]:
                min_idx = j
        eğer min_idx != i:
            değişken temp = d[i]
            d[i] = d[min_idx]
            d[min_idx] = temp
    döndür d

işlem eklemeli_sirala(dizi):
    değişken d = []
    döngü x içinde dizi:
        d.ekle(x)
    değişken n = uzunluk(d)
    döngü i içinde aralık(1, n):
        değişken anahtar = d[i]
        değişken j = i - 1
        iken j >= 0 ve d[j] > anahtar:
            d[j + 1] = d[j]
            j = j - 1
        d[j + 1] = anahtar
    döndür d

işlem sirali_mi(dizi):
    değişken n = uzunluk(dizi)
    döngü i içinde aralık(n - 1):
        eğer dizi[i] > dizi[i + 1]:
            döndür yanlış
    döndür doğru

işlem saymali_sirala(dizi, max_deger):
    değişken sayac = []
    döngü i içinde aralık(max_deger + 1):
        sayac.ekle(0)
    döngü x içinde dizi:
        sayac[x] = sayac[x] + 1
    değişken sonuc = []
    döngü i içinde aralık(max_deger + 1):
        döngü k içinde aralık(sayac[i]):
            sonuc.ekle(i)
    döndür sonuc
"""
        }
    },
    "vektor_fizik": {
        "meta": {
            "isim": "vektor_fizik",
            "surum": "1.0.0",
            "yazar": "varyn_toplulugu",
            "tur": "varyn",
            "aciklama": "Saf Varyn ile 2D/3D Vektör Matematiği, Büyüklük, Normalizasyon, Nokta Çarpımı ve AABB Çarpışma Testi.",
            "izinler": [],
            "bagimliliklar": []
},
        "files": {
            "main.varyn": """# 2D/3D Vektör Matematiği ve Çarpışma Fiziği Kütüphanesi - %100 Saf Varyn

işlem vektor2d(x, y):
    döndür {"x": ondalik(x), "y": ondalik(y)}

işlem vektor3d(x, y, z):
    döndür {"x": ondalik(x), "y": ondalik(y), "z": ondalik(z)}

işlem vektor_topla(v1, v2):
    eğer "z" içinde v1 ve "z" içinde v2:
        döndür {"x": v1["x"] + v2["x"], "y": v1["y"] + v2["y"], "z": v1["z"] + v2["z"]}
    döndür {"x": v1["x"] + v2["x"], "y": v1["y"] + v2["y"]}

işlem vektor_cikar(v1, v2):
    eğer "z" içinde v1 ve "z" içinde v2:
        döndür {"x": v1["x"] - v2["x"], "y": v1["y"] - v2["y"], "z": v1["z"] - v2["z"]}
    döndür {"x": v1["x"] - v2["x"], "y": v1["y"] - v2["y"]}

işlem vektor_olcekle(v, skaler):
    eğer "z" içinde v:
        döndür {"x": v["x"] * skaler, "y": v["y"] * skaler, "z": v["z"] * skaler}
    döndür {"x": v["x"] * skaler, "y": v["y"] * skaler}

işlem nokta_carpim(v1, v2):
    eğer "z" içinde v1 ve "z" içinde v2:
        döndür (v1["x"] * v2["x"]) + (v1["y"] * v2["y"]) + (v1["z"] * v2["z"])
    döndür (v1["x"] * v2["x"]) + (v1["y"] * v2["y"])

işlem vektor_uzunluk(v):
    değişken kareler = 0.0
    eğer "z" içinde v:
        kareler = (v["x"] * v["x"]) + (v["y"] * v["y"]) + (v["z"] * v["z"])
    değilse:
        kareler = (v["x"] * v["x"]) + (v["y"] * v["y"])
    eğer kareler == 0.0:
        döndür 0.0
    değişken kok = kareler / 2.0
    döngü i içinde aralık(20):
        kok = (kok + (kareler / kok)) / 2.0
    döndür kok

işlem vektor_birim(v):
    değişken u = vektor_uzunluk(v)
    eğer u == 0.0:
        döndür v
    döndür vektor_olcekle(v, 1.0 / u)

işlem capraz_carpim_3d(v1, v2):
    değişken rx = (v1["y"] * v2["z"]) - (v1["z"] * v2["y"])
    değişken ry = (v1["z"] * v2["x"]) - (v1["x"] * v2["z"])
    değişken rz = (v1["x"] * v2["y"]) - (v1["y"] * v2["x"])
    döndür {"x": rx, "y": ry, "z": rz}

işlem aabb_carpismasi_mi(kutu1, kutu2):
    değişken k1_sag = kutu1["x"] + kutu1["genislik"]
    değişken k1_alt = kutu1["y"] + kutu1["yukseklik"]
    değişken k2_sag = kutu2["x"] + kutu2["genislik"]
    değişken k2_alt = kutu2["y"] + kutu2["yukseklik"]
    
    eğer k1_sag < kutu2["x"] veya kutu1["x"] > k2_sag:
        döndür yanlış
    eğer k1_alt < kutu2["y"] veya kutu1["y"] > k2_alt:
        döndür yanlış
    döndür doğru
"""
        }
    },
    "bulmaca_zeka": {
        "meta": {
            "isim": "bulmaca_zeka",
            "surum": "1.0.0",
            "yazar": "varyn_toplulugu",
            "tur": "varyn",
            "aciklama": "Saf Varyn ile Sudoku 4x4 Doğrulayıcı, Hanoi Kuleleri Çözücü, N-Vezir Tehdit Kontrolü ve Anagram Testi.",
            "izinler": [],
            "bagimliliklar": []
},
        "files": {
            "main.varyn": """# Mantık, Zeka Oyunları ve Bulmaca Algoritmaları Kütüphanesi - %100 Saf Varyn

işlem sudoku_4x4_dogrula(matris):
    döngü i içinde aralık(4):
        değişken sayac = [0, 0, 0, 0, 0]
        döngü j içinde aralık(4):
            değişken val = matris[i][j]
            eğer val < 1 veya val > 4 veya sayac[val] > 0:
                döndür yanlış
            sayac[val] = 1
            
    döngü j içinde aralık(4):
        değişken sayac = [0, 0, 0, 0, 0]
        döngü i içinde aralık(4):
            değişken val = matris[i][j]
            eğer val < 1 veya val > 4 veya sayac[val] > 0:
                döndür yanlış
            sayac[val] = 1
            
    döngü bi içinde [0, 2]:
        döngü bj içinde [0, 2]:
            değişken sayac = [0, 0, 0, 0, 0]
            döngü r içinde aralık(2):
                döngü c içinde aralık(2):
                    değişken val = matris[bi + r][bj + c]
                    eğer val < 1 veya val > 4 veya sayac[val] > 0:
                        döndür yanlış
                    sayac[val] = 1
    döndür doğru

işlem hanoi_hamleleri(disk_sayisi, kaynak, hedef, yardimci):
    eğer disk_sayisi == 1:
        döndür [metin(kaynak) + " -> " + metin(hedef)]
    değişken hamleler = []
    değişken adim1 = hanoi_hamleleri(disk_sayisi - 1, kaynak, yardimci, hedef)
    döngü h içinde adim1:
        hamleler.ekle(h)
    hamleler.ekle(metin(kaynak) + " -> " + metin(hedef))
    değişken adim2 = hanoi_hamleleri(disk_sayisi - 1, yardimci, hedef, kaynak)
    döngü h içinde adim2:
        hamleler.ekle(h)
    döndür hamleler

işlem vezir_tehditi_var_mi(vezir_pozisyonlari):
    değişken n = uzunluk(vezir_pozisyonlari)
    döngü i içinde aralık(n):
        döngü j içinde aralık(i + 1, n):
            eğer vezir_pozisyonlari[i] == vezir_pozisyonlari[j]:
                döndür doğru
            değişken satir_farki = j - i
            değişken sutun_farki = vezir_pozisyonlari[j] - vezir_pozisyonlari[i]
            eğer sutun_farki < 0:
                sutun_farki = sutun_farki * -1
            eğer satir_farki == sutun_farki:
                döndür doğru
    döndür yanlış

işlem anagram_mi(kelime1, kelime2):
    eğer uzunluk(kelime1) != uzunluk(kelime2):
        döndür yanlış
    değişken harfler1 = []
    değişken harfler2 = []
    döngü i içinde aralık(uzunluk(kelime1)):
        harfler1.ekle(kelime1[i])
        harfler2.ekle(kelime2[i])
    değişken n = uzunluk(harfler1)
    döngü i içinde aralık(n):
        döngü j içinde aralık(n - i - 1):
            eğer harfler1[j] > harfler1[j + 1]:
                değişken temp = harfler1[j]
                harfler1[j] = harfler1[j + 1]
                harfler1[j + 1] = temp
            eğer harfler2[j] > harfler2[j + 1]:
                değişken temp2 = harfler2[j]
                harfler2[j] = harfler2[j + 1]
                harfler2[j + 1] = temp2
    döngü i içinde aralık(n):
        eğer harfler1[i] != harfler2[i]:
            döndür yanlış
    döndür doğru
"""
        }
    },

}

import hashlib
import os
import sys

# 1024-bit RSA Public Key
RSA_N = 131869317293702309841552762712251746919494094597659741157495659622634729285218513465697541530679097013689567260341373183132862975885657361980250503060699818453974315755595888928004082339480555986396058724985887669654995936400724289959367139038363430191002142550275704958761657952655646721269560238302518773703
RSA_E = 65537

# Private key management: Load private key from environment variable if available, else use fallback
_ENV_KEY = os.environ.get("VARYNPAKET_PRIVATE_KEY")
if _ENV_KEY:
    try:
        RSA_D = int(_ENV_KEY)
    except ValueError:
        sys.stderr.write("UYARI: VARYNPAKET_PRIVATE_KEY çevre değişkeni geçersiz bir tam sayı!\n")
        RSA_D = 93938552987988251480274231044817203361208192324737822538090580361358087361486053979577268167619578607215941180040242129297051145035595153904053816712571992175078123642258989724668394151125180703607862519124809434470623668480551915902524795404471847667258571538274913168643509098659044555951719233962928798577
else:
    RSA_D = 93938552987988251480274231044817203361208192324737822538090580361358087361486053979577268167619578607215941180040242129297051145035595153904053816712571992175078123642258989724668394151125180703607862519124809434470623668480551915902524795404471847667258571538274913168643509098659044555951719233962928798577

def pkcs1_v1_5_pad(hash_bytes, key_size=128):
    if len(hash_bytes) != 32:
        raise ValueError("Hash size must be 32 bytes for SHA-256.")
    der_prefix = b"\x30\x31\x30\x0d\x06\x09\x60\x86\x48\x01\x65\x03\x04\x02\x01\x05\x00\x04\x20"
    t = der_prefix + hash_bytes
    ps_len = key_size - len(t) - 3
    if ps_len < 8:
        raise ValueError("Key size is too small for PKCS#1 v1.5 padding with SHA-256.")
    ps = b"\xff" * ps_len
    return b"\x00\x01" + ps + b"\x00" + t

def generate_sha256(content_dict):
    """
    Paket içeriğindeki tüm dosyaları birleştirerek SHA256 hash'i oluşturur,
    ardından asimetrik geliştirici özel anahtarı (RSA Private Key) ile PKCS#1 v1.5 standardında kriptografik olarak imzalar.
    """
    m = hashlib.sha256()
    for filename in sorted(content_dict.keys()):
        m.update(filename.encode('utf-8'))
        m.update(content_dict[filename].encode('utf-8'))
    hash_bytes = m.digest()
    
    # PKCS#1 v1.5 padding uygulayarak 128 byte'lık blok elde et
    padded_block = pkcs1_v1_5_pad(hash_bytes, key_size=128)
    block_int = int.from_bytes(padded_block, byteorder='big')
    
    # Asimetrik imzalama: s = block^d mod n
    s_int = pow(block_int, RSA_D, RSA_N)
    
    # İmzayı hex formatında döndür
    return hex(s_int)[2:]

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
