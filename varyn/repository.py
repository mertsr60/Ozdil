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
    if getattr(plugin_api.plugin, "current_program", None) is not None:
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
    }
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
