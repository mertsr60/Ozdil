# 📚 Varyn Kütüphane ve Eklenti Geliştirme Kılavuzu

Varyn, hem saf **Varyn (`.varyn`)** kodlarıyla yazılmış modülleri hem de arkada güvenli bir sandbox ortamında çalışan güçlü **Python (`.py`)** eklentilerini (plugin) destekleyen genişletilebilir bir dil ekosistemine sahiptir.

Bu kılavuz, kendi Varyn kütüphanelerinizi nasıl sıfırdan oluşturacağınızı, paket yapılandırmasını nasıl tanımlayacağınızı ve **basit yapay zekâ (AI) modellerini** (gerek yerel algoritmalar gerekse dış API'ler ile) Varyn'e nasıl kütüphane olarak entegre edeceğinizi **adım adım, eksiksiz ve en ince ayrıntılarıyla** açıklamaktadır.

---

## 📂 1. Varyn Kütüphane Yapısı ve Anatomisi

Varyn kütüphaneleri, sistemdeki iki ana dizinden birinde barındırılır:
1. **Yerel Proje Paketleri:** Projenizin kök dizinindeki `./varyn_packages/` klasörünün altında.
2. **Global Kullanıcı Paketleri:** Kullanıcı ev dizinindeki `~/.varyn/packages/` klasörünün altında.

Her kütüphane kendi adını taşıyan müstakil bir klasör içerisinde yer almalıdır.

### Örnek Klasör Ağacı:
```text
varyn_packages/
└── yapay_zeka/
    ├── varynpaket.json     # Paket metaverileri ve izin tanımları (Zorunlu)
    └── main.py          # Python eklentisi için ana giriş dosyası (veya main.varyn)
```

---

## ⚙️ 2. Paket Yapılandırma Dosyası: `varynpaket.json`

Kütüphanenizin Varyn Çalışma Zamanı (Runtime) tarafından tanınması ve güvenlik kontrollerinden geçmesi için her paket klasöründe bir `varynpaket.json` bulunmalıdır.

```json
{
  "isim": "yapay_zeka",
  "surum": "1.0.0",
  "yazar": "varyn_gelistirici",
  "tur": "python",
  "aciklama": "Varyn için duygu analizi ve akıllı metin üretimi sağlayan basit bir yapay zekâ kütüphanesi.",
  "izinler": ["ag", "dosya_sistemi"],
  "bagimliliklar": [],
  "imza": "c0af7e0543a3304afdac1d99bbfad50bd06c5a6ceb91ec0052db0b7b690e8148"
}
```

### Parametre Açıklamaları:
*   **`isim`**: Kütüphanenizin çağrılacağı isim. Varyn kodunda `getir yapay_zeka` ifadesindeki isimle birebir eşleşmelidir.
*   **`surum`**: Semantik versiyonlama formatında kütüphane sürümü (örn: `"1.0.0"`).
*   **`tur`**: Kütüphanenin yazıldığı dil. İki değer alabilir:
    *   `"varyn"`: Saf Varyn kodlarından oluşan modüller.
    *   `"python"`: Python ile yazılmış, Varyn fonksiyonları üreten güçlü eklentiler.
*   **`izinler`**: Python eklentilerinin Sandbox güvenlik duvarını aşabilmesi için talep ettiği ayrıcalıklar. Boş bırakılırsa kütüphane en sıkı kısıtlamalarla çalışır:
    *   `"ag"`: İnternet istekleri (`urllib`, `requests`, `socket` vb.) yapabilme izni. (API tabanlı AI modelleri için gereklidir).
    *   `"dosya_sistemi"`: Dosya okuma ve yazma (`open`, `os`, `shutil` vb.) izni. (Yerel yapay zeka ağırlıklarını veya veri kümelerini yüklemek için gereklidir).
    *   `"sistem"`: Alt süreç çalıştırma, işletim sistemi detaylarına erişim izni (`subprocess`, `sys`, `platform`).
*   **`bagimliliklar`**: Bu paket yüklenmeden önce otomatik olarak yüklenmesi gereken diğer Varyn kütüphanelerinin listesi.
*   **`imza`**: Güvenlik doğrulama imzası. Yerel geliştirme ortamında veya `./varyn_packages` dizininde çalışırken imza kontrolü geliştiriciyi engellememek için esnek tutulabilir, ancak paket yayınlanırken `varynpip` paketi doğrulamak için SHA256 imzasını kullanır.

---

## 🛠️ 3. Saf Varyn ile Kütüphane Yazmak (`tur: "varyn"`)

Eğer yapay zeka algoritmanızı doğrudan Varyn sözdizimi ile yazmak isterseniz kütüphane türünü `"varyn"` olarak seçmelisiniz.

### Adım 1: `varyn_packages/tahminci/varynpaket.json`
```json
{
  "isim": "tahminci",
  "surum": "1.0.0",
  "yazar": "akademik_kod",
  "tur": "varyn",
  "aciklama": "Saf Varyn dilinde yazılmış doğrusal regresyon tahmincisi.",
  "izinler": [],
  "bagimliliklar": []
}
```

### Adım 2: `varyn_packages/tahminci/main.varyn`
Varyn dosyasında tanımlanan tüm global değişkenler ve fonksiyonlar, kütüphane içe aktarıldığında bir nesne özniteliği olarak sunulur.

```varyn
# Basit Doğrusal Regresyon Tahmin Fonksiyonu (y = ax + b)
fonksiyon tahmin_et(x, a, b):
    dondur a * x + b

# Ortalama Kare Hata (MSE) Hesaplayıcı
fonksiyon hata_hesapla(gercekler, tahminler):
    değişken toplam_hata = 0
    değişken n = uzunluk(gercekler)
    
    dongu i icinde aralik(0, n):
        değişken fark = gercekler[i] - tahminler[i]
        toplam_hata = toplam_hata + (fark ** 2)
        
    dondur toplam_hata / n
```

### Adım 3: Ana Kodda Kullanımı (`kod.varyn`)
```varyn
getir tahminci

# Girdi verilerimiz
değişken egim = 2.5
değişken kesim = 10.0
değişken girdi = 4

değişken sonuc = tahminci.tahmin_et(girdi, egim, kesim)
yazdir("Girdi 4 için Yapay Zeka Tahmini: " + metin(sonuc)) # Çıktı: 20.0
```

---

## 🚀 4. Python ile Yapay Zekâ Eklentisi Yazmak (`tur: "python"`)

Python'ın sunduğu zengin veri yapıları, matematiksel operasyonlar ve ağ erişimi sayesinde çok daha gelişmiş ve akıllı yapay zeka kütüphaneleri yazabilirsiniz. Python eklentileri yazarken bilmeniz gereken en kritik bileşenler şunlardır:

### 🔒 AST Tabanlı Python Sandbox Kuralları
Varyn çalışma zamanı, eklentinin Python kodunu **AST (Abstract Syntax Tree)** seviyesinde inceler ve kısıtlar.
*   `eval()` ve `exec()` kullanımı kesinlikle **yasaktır**.
*   Ağ istekleri (`urllib`, `requests`) için `varynpaket.json` içinde `"ag"` izni belirtilmelidir.
*   Yerel dosya okuma (`open`) işlemleri için `"dosya_sistemi"` izni belirtilmelidir.

### 🔌 Eklenti API Kayıt Mekanizması (`plugin_api`)
Her Python eklentisi, Varyn interpreter'ına kendi fonksiyonlarını kaydetmek için yerleşik `plugin_api` modülünü kullanır ve bir `plugin()` fonksiyonu tanımlar. Bu fonksiyon, dışa aktarılacak metodları içeren bir Python sözlüğü (`dict`) döndürmelidir.

---

## 🤖 5. Senaryo A: Tamamen Yerel ve Hevristik (Heuristic) Yapay Zekâ Kütüphanesi

Dışarıdan hiçbir kütüphaneye bağımlı olmadan, kelime frekansları ve duygu sözlüğü tabanlı çalışan, tamamen yerel bir **Duygu Analizi (Sentiment Analysis) AI** modeli inşa edelim. Bu yöntem, sunucu maliyeti veya ağ bağlantısı gerektirmeden hızlıca kararlar alabilir.

### Adım 1: `varyn_packages/akilli_analiz/varynpaket.json`
```json
{
  "isim": "akilli_analiz",
  "surum": "1.0.0",
  "yazar": "nlp_ekibi",
  "tur": "python",
  "aciklama": "Hevristik duygu analizi ve kelime kökü tabanlı makine öğrenmesi eklentisi.",
  "izinler": [],
  "bagimliliklar": []
}
```

### Adım 2: `varyn_packages/akilli_analiz/main.py`
```python
# -*- coding: utf-8 -*-
import plugin_api

# Yerel Hevristik AI Duygu Sözlüğü
OLUMLU_KELIMELER = {
    "harika", "mükemmel", "süper", "iyi", "başarılı", "bayıldım", 
    "güzel", "sevdim", "hızlı", "kolay", "tebrik", "muazzam"
}

OLUMSUZ_KELIMELER = {
    "kötü", "berbat", "yavaş", "başarısız", "hata", "rezalet", 
    "bozuk", "zor", "beğenmedim", "nefret", "eksik", "çalışmıyor", "sorun"
}

def metin_temizle(metin):
    """Metindeki noktalama işaretlerini kaldırır ve küçük harfe çevirir."""
    temiz_metin = ""
    for karakter in metin.lower():
        if karakter.isalnum() or karakter.isspace():
            temiz_metin += karakter
    return temiz_metin

def duygu_analizi_yap(metin):
    """
    Basit bir Naive-Bayes benzeri kelime frekans skorlaması yapar.
    Döndürülen değer: Olumlu skor oranı ve sınıf etiketi.
    """
    temiz = metin_temizle(metin)
    kelimeler = temiz.split()
    
    olumlu_skor = 0
    olumsuz_skor = 0
    
    for kelime in kelimeler:
        # Kelimenin kendisini veya kökünü kontrol et
        if kelime in OLUMLU_KELIMELER:
            olumlu_skor += 1
        elif kelime in OLUMSUZ_KELIMELER:
            olumsuz_skor += 1
            
    toplam = olumlu_skor + olumsuz_skor
    if toplam == 0:
        return {"etiket": "NÖTR", "olumlu_oran": 0.5, "skor": 0}
        
    olumlu_oran = olumlu_skor / toplam
    
    if olumlu_skor > olumsuz_skor:
        etiket = "OLUMLU"
    elif olumsuz_skor > olumlu_skor:
        etiket = "OLUMSUZ"
    else:
        etiket = "NÖTR"
        
    return {
        "etiket": etiket,
        "olumlu_oran": round(olumlu_oran, 2),
        "skor": olumlu_skor - olumsuz_skor
    }

def akilli_cevap_uret(kullanici_mesaji):
    """Duygu durumuna göre otomatik AI yanıt şablonu oluşturur."""
    analiz = duygu_analizi_yap(kullanici_mesaji)
    etiket = analiz["etiket"]
    
    if etiket == "OLUMLU":
        return "Harika geri bildiriminiz için teşekkür ederiz! Sizleri mutlu görmek bizi çok sevindirdi. 😊"
    elif etiket == "OLUMSUZ":
        return "Yaşadığınız olumsuz deneyim için çok üzgünüz. Mühendislik ekibimiz sorunu çözmek için hemen çalışmaya başlayacak. 🛠️"
    else:
        return "Geri bildiriminiz sistemimize kaydedildi. Size daha iyi hizmet verebilmek için çalışıyoruz. 👍"

# Varyn Entegrasyonu için Giriş Fonksiyonu
def plugin():
    # Fonksiyonları global Varyn çalışma alanına kaydet
    plugin_api.plugin.fonksiyon_ekle("duygu_analizi", duygu_analizi_yap)
    plugin_api.plugin.fonksiyon_ekle("akilli_cevap", akilli_cevap_uret)
    
    # Kütüphane namespace'inde çağrılabilecek şekilde nesne olarak dön
    return {
        "duygu_analizi": duygu_analizi_yap,
        "akilli_cevap": akilli_cevap_uret
    }
```

### Adım 3: Varyn'de Kullanımı
```varyn
getir akilli_analiz

değişken yorum_1 = "Bu program gerçekten harika ve çok başarılı bir çalışma olmuş, bayıldım!"
değişken yorum_2 = "Sistem çok yavaş çalışıyor, her yerde hata var ve berbat bir arayüzü var."

# 1. Doğrudan analiz etme
değişken sonuc_1 = akilli_analiz.duygu_analizi(yorum_1)
yazdir("Yorum 1 Analizi:")
yazdir("  Etiket      : " + sonuc_1["etiket"])
yazdir("  Olumlu Oran : " + metin(sonuc_1["olumlu_oran"]))

# 2. Akıllı otomatik yanıt üretme
değişken yanit = akilli_analiz.akilli_cevap(yorum_2)
yazdir("\nSistem Yanıtı:")
yazdir(yanit)
```

---

## 🌐 6. Senaryo B: Gemini API Destekli Büyük Dil Modeli (LLM) Kütüphanesi

Eğer gerçek, üretken bir yapay zekâ modelinin (LLM) zekasından yararlanmak istiyorsanız, Varyn içinden güvenli bir API proxy'si kurabilirsiniz.

Bu senaryoda, Python eklentisinde **`urllib.request`** kullanarak Gemini API'sine bir `POST` isteği göndereceğiz.
*Güvenlik Uyarısı: API anahtarı doğrudan koda yazılmamalı, çevre değişkenlerinden (Environment Variables) güvenli bir şekilde okunmalıdır.*

### Adım 1: `varyn_packages/oz_gemini/varynpaket.json`
```json
{
  "isim": "oz_gemini",
  "surum": "1.1.0",
  "yazar": "yapay_zeka_merkezi",
  "tur": "python",
  "aciklama": "Gemini 1.5 Flash API entegrasyonu sağlayan Varyn Yapay Zekâ eklentisi.",
  "izinler": ["ag"],
  "bagimliliklar": []
}
```

### Adım 2: `varyn_packages/oz_gemini/main.py`
```python
# -*- coding: utf-8 -*-
import os
import json
import urllib.request
import urllib.parse
import plugin_api

def gemini_soru_sor(istem_metni):
    """
    Gemini 1.5 Flash API'sine istek göndererek üretken yanıt alır.
    Güvenlik ve sandbox kurallarına tam uyumludur.
    """
    # 1. API Anahtarı kontrolü
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "Hata: GEMINI_API_KEY çevre değişkeni bulunamadı. Lütfen Ayarlar menüsünden API anahtarınızı tanımlayın."
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    # 2. Google Gemini API İstek Gövdesi Formatı
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": istem_metni}
                ]
            }
        ]
    }
    
    # 3. JSON verisini encode etme
    data_bytes = json.dumps(payload).encode('utf-8')
    
    # 4. Request nesnesini hazırlama
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "VarynInterpreter/1.0"
    }
    
    req = urllib.request.Request(url, data=data_bytes, headers=headers, method="POST")
    
    try:
        # 5. İsteği güvenli ağ izniyle gönderme (timeout: 15 saniye)
        with urllib.request.urlopen(req, timeout=15) as response:
            res_body = response.read().decode('utf-8')
            res_json = json.loads(res_body)
            
            # Gemini yanıt yapısını ayrıştırma
            text_response = res_json['candidates'][0]['content']['parts'][0]['text']
            return text_response.strip()
            
    except Exception as e:
        return f"Bağlantı Hatası: Gemini API isteği başarısız oldu. Detay: {str(e)}"

def kod_acikla(varyn_kodu):
    """Varyn kodlarını açıklamak için önceden yapılandırılmış özel bir sistem istemi."""
    sistem_istemi = (
        "Sen Varyn programlama dili asistanısın. Aşağıda verilen Varyn kodunu incele, "
        "ne yaptığını satır satır ve anlaşılır bir Türkçe ile açıkla:\n\n"
    )
    return gemini_soru_sor(sistem_istemi + varyn_kodu)

# Eklentiyi Kaydetme
def plugin():
    plugin_api.plugin.fonksiyon_ekle("yapay_zeka_sor", gemini_soru_sor)
    plugin_api.plugin.fonksiyon_ekle("varyn_acikla", kod_acikla)
    return {
        "sor": gemini_soru_sor,
        "acikla": kod_acikla
    }
```

### Adım 3: Varyn'de Kullanımı
```varyn
getir oz_gemini

yazdir("Gemini API'ye bağlanılıyor...")

değişken soru = "Yapay zekanın gelecekteki gelişim süreçleri hakkında 2 cümlelik özet bilgi yaz."
değişken cevap = oz_gemini.sor(soru)

yazdir("\n--- Yapay Zekâ Yanıtı ---")
yazdir(cevap)

değişken kod = "islem topla(a, b):\n    dondur a + b"
değişken analiz = oz_gemini.acikla(kod)
yazdir("\n--- Kod Analizi ---")
yazdir(analiz)
```

---

## 🔒 7. Kütüphaneleri Hata Yakalama Blokları ile Güvenli Hale Getirmek

Özellikle ağ istekleri içeren AI kütüphaneleri kullanırken internet kopmaları veya hatalı API parametreleri nedeniyle programın çökmesini engellemek için **`dene-hata_yakala`** yapısını kullanmalısınız:

```varyn
getir oz_gemini

dene:
    değişken cevap = oz_gemini.sor("Türkiye'nin başkenti neresidir?")
    yazdir("Cevap: " + cevap)
hata_yakala Exception olarak hata:
    yazdir("Sistemde bir hata oluştu, AI modeline erişilemiyor!")
    yazdir("Hata detayı: " + metin(hata))
```

---

## 🏁 Sonuç ve Paket Dağıtımı

Kendi yazdığınız yerel kütüphaneyi test etmek için tek yapmanız gereken kütüphane klasörünü `./varyn_packages/` altına yerleştirmektir. 

Eğer kütüphanenizi global Varyn topluluğu ile paylaşmak isterseniz:
1. Paket klasörünüzün SHA256 imzasını oluşturup `varynpaket.json` dosyasındaki `"imza"` alanına ekleyin.
2. Paketi ZIP formatına sıkıştırıp Varyn Paket Deposu (Repository) sunucusuna gönderin.
3. Artık tüm dünyadaki Varyn kullanıcıları terminale `python3 varynpip.py yukle <paket_adi>` yazarak kütüphanenizi tek tıkla yükleyip kullanabilir! 🎉
