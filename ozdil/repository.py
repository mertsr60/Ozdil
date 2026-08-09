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
