# ÖzDil Paket ve Eklenti Sistemi Dokümantasyonu 📚

ÖzDil, Python tabanlı eklentileri (plugins) ve yerel ÖzDil kütüphanelerini yönetebilen, tam uyumlu bir paket yönetim ekosistemine sahiptir. Bu sistem, Python'ın `pip` + `import` mantığıyla çalışır ve güvenlik için AST tabanlı bir Sandbox denetimi barındırır.

---

## 📂 Dosya Yapısı

Gelişmiş paket yönetim mimarisi aşağıdaki modüllerden oluşur:

- `ozdil/ozdil.py`: ÖzDil Interpreter/Compiler köprüsü.
- `ozdil/ozpip.py`: `ozpip` paket yöneticisi komut satırı arayüzü (CLI).
- `ozdil/plugin_api.py`: Python eklentilerinin ÖzDil ile entegre olmasını sağlayan dinamik API ve Event (Olay) sistemi.
- `ozdil/package_manager.py`: Bağımlılık çözme, sürüm uyumluluğu ve imza doğrulaması yapan çekirdek kütüphane.
- `ozdil/sandbox.py`: Güvenli çalışma ortamı sunan, AST tabanlı Python kod analizcisi.
- `ozdil/repository.py` & `repository.json`: Paket deposu ve metadata veritabanı simülasyonu.

---

## 1. ÖzDil Paketi Nasıl Yapılır? (`tur: "ozdil"`)

Yerel bir ÖzDil paketi, yalnızca ÖzDil dilinde yazılmış kodlardan oluşur.

### Adım 1: Klasör ve ozpaket.json Hazırlama
Öncelikle `oz_packages/` veya küresel paketler dizininde paket ismiyle bir klasör oluşturun ve içine `ozpaket.json` yerleştirin:

```json
{
  "isim": "geometri",
  "surum": "1.0.0",
  "yazar": "ozdil_gelistirici",
  "tur": "ozdil",
  "aciklama": "Geometrik şekillerin alan hesaplamalarını yapan ÖzDil paketi.",
  "izinler": [],
  "bagimliliklar": []
}
```

### Adım 2: ÖzDil Kodunu Yazma (`geometri.oz` veya `main.oz`)
Aynı klasörde paketin ana kodunu oluşturun:

```ozdil
# geometri.oz
işlem kare_alani(kenar):
    döndür kenar * kenar

işlem daire_alani(yari_cap):
    # pi sayısı yaklaşık
    döndür 3.14 * yari_cap * yari_cap
```

### Adım 3: Kullanım
ÖzDil ana programında bu paketi şu şekilde içe aktarabilir ve kullanabilirsiniz:

```ozdil
getir geometri

değişken alan = geometri.kare_alani(5)
yazdır("Karenin Alanı: " + metin(alan))
```

---

## 2. Python Eklentisi Nasıl Yazılır? (`tur: "python"`)

Python eklentileri, ÖzDil'in sınırlarını genişleterek Python'ın geniş kütüphane ekosistemini ÖzDil içinde kullanmanızı sağlar.

### Adım 1: ozpaket.json Tanımlama
Python eklentileri için `tur` alanı `"python"` olmalıdır. Eğer eklenti tehlikeli kütüphaneler kullanacaksa gerekli güvenlik izinleri `izinler` kısmında bildirilmelidir:

```json
{
  "isim": "sistem_yardimcisi",
  "surum": "1.1.0",
  "yazar": "sistem_mimari",
  "tur": "python",
  "aciklama": "Sistem zamanı ve donanım bilgilerine erişim sağlayan eklenti.",
  "izinler": ["sistem"],
  "bagimliliklar": []
}
```

### Adım 2: Python Kodunu Yazma (`main.py`)
Eklentinin ÖzDil'e fonksiyon veya komut sunabilmesi için bir `plugin()` fonksiyonu barındırması ve bu fonksiyonun dışa aktarılacak arabirimleri içeren bir sözlük (dictionary) dönmesi gerekir.

```python
# main.py
import plugin_api
import platform # "sistem" izni gerektirir

def isletim_sistemi():
    return platform.system()

def eklenti_bilgisi():
    return "Sistem Yardımcısı Eklentisi v1.1.0"

def plugin():
    # 1. API Üzerinden Doğrudan Global Fonksiyon Ekleme (yazdır(isletim_sistemi()) için)
    plugin_api.plugin.fonksiyon_ekle("isletim_sistemi", isletim_sistemi)
    
    # 2. Namespace Üzerinden Erişim İçin Sözlük Dönme (getir sistem_yardimcisi -> sistem_yardimcisi.eklenti_bilgisi() için)
    return {
        "isletim_sistemi": isletim_sistemi,
        "eklenti_bilgisi": eklenti_bilgisi
    }
```

### Adım 3: ÖzDil İçinden Kullanım
Python eklentisi içe aktarıldığında kayıt edilen fonksiyonlar hem **global alanda** doğrudan, hem de **paket ad alanı (namespace)** altında çağrılabilir hale gelir:

```ozdil
getir sistem_yardimcisi

# Global alandan doğrudan çağırma
değişken os_adi = isletim_sistemi()
yazdır("İşletim Sistemi: " + os_adi)

# Paket ad alanından çağırma
yazdır(sistem_yardimcisi.eklenti_bilgisi())
```

---

## 3. Gelişmiş Eklenti API'si ve Olay (Event) Sistemi

Eklentiler, ÖzDil'in çalışma zamanı olaylarını dinleyebilir. `plugin_api` içinde sunulan olay kancaları şunlardır:

1. `program_basladi`: ÖzDil kodu yorumlanmaya başlamadan hemen önce tetiklenir.
2. `paket_yuklendi`: Bir paket/eklenti başarıyla yüklendiğinde tetiklenir (parametre: `paket_adi`).
3. `hata_olustu`: Çalışma zamanında veya derleme sırasında hata meydana geldiğinde tetiklenir (parametre: `hata_metni`).
4. `program_bitti`: Program başarıyla sonlandığında tetiklenir.

### Event Dinleyicisi Tanımlama Örneği:

```python
# main.py içindeki olay dinleyicisi tanımı
import plugin_api

def baslangic_kancasi():
    print("[Eklenti Olayı] ÖzDil programı şu an başladı!")

def hata_kancasi(hata):
    print(f"[Eklenti Olayı] Hata algılandı: {hata}")

def plugin():
    plugin_api.plugin.event_ekle("program_basladi", baslangic_kancasi)
    plugin_api.plugin.event_ekle("hata_olustu", hata_kancasi)
    return {}
```

---

## 4. Güvenlik Kuralları ve Python Sandbox

ÖzDil, eklentilerin sisteme zarar vermesini engellemek için **AST (Abstract Syntax Tree)** tabanlı son derece güvenli bir süzgeç barındırır. 

### Yasaklı İşlemler ve İzinler:
Bir Python eklentisinde izin bildirilmeden aşağıdaki işlemler yapılırsa, interpreter çalışmayı durdurur ve **Güvenlik Hatası (SecurityError)** üretir:

| Yasaklı Kütüphane / İşlem | Gerekli İzin |
| :--- | :--- |
| `os`, `shutil`, `pathlib`, `open()` | `dosya_sistemi` |
| `subprocess`, `sys`, `ctypes`, `platform` | `sistem` |
| `socket`, `urllib`, `requests` | `ag` |
| `eval()`, `exec()` | **Kesinlikle Yasak (İzin Verilemez)** |

### AST Güvenlik Süzgeci Nasıl Çalışır?
Sandbox kontrolü yalnızca metinsel arama yapmaz. Kodun ağaç yapısını analiz eder. Dolayısıyla aşağıdaki gizleme yöntemlerinin tamamı süzgeç tarafından yakalanır:

- ❌ `import os` (Yasaklı İçe Aktarma)
- ❌ `__import__("os")` (Dinamik İçe Aktarma)
- ❌ `import_module("os")` (Dinamik import_module)
- ❌ `exec("import os")` (Exec Bloğu)

---

## 5. Paket İmzalama ve SHA256 Doğrulaması

Paketlerin bütünlüğünü korumak ve yetkisiz değiştirilmelerini (örneğin zararlı kod enjekte edilmesini) önlemek amacıyla paketler SHA256 ile imzalanır.

1. Bir paket kurulurken veya `ozpaket paketle` komutuyla paketlenirken, paketin içerdiği tüm dosyaların içeriği ve yolları birleştirilerek SHA256 hash'i (imza) üretilir.
2. Bu imza `ozpaket.json` içerisine yazılır ve merkezi depoda saklanır.
3. Paket `getir` ile yüklenirken, yerel dosyaların SHA256 hash'leri tekrar hesaplanır. Eğer beklenen imza ile hesaplanan imza eşleşmezse, **Bozuk veya Yetkisiz Paket Hatası** verilir ve paket çalıştırılmaz.

---

## 6. Geliştirici ve Paketleme Araçları (`ozpaket.py`)

Geliştiricilerin hızlıca eklenti yazabilmesi ve paketleyebilmesi için hazır CLI araçları sunulmuştur.

### 1) Yeni Eklenti Şablonu Oluşturma:
```bash
python3 ozpaket.py oluştur <eklenti_adi>
```
Bu komut, belirtilen isimde bir klasör oluşturur ve içine standart `ozpaket.json`, `main.py`, `README.md` ve `test.oz` şablonlarını otomatik yerleştirir.

### 2) Eklentiyi Test Etme:
Paket dizininizin içindeyken şu komutu çalıştırarak testleri koşturabilirsiniz:
```bash
python3 ozpaket.py test
```
Bu komut `test.oz` dosyasını ÖzDil interpreter'ı ile çalıştırarak çıktıları gösterir.

### 3) Dağıtıma Hazır Paketleme:
```bash
python3 ozpaket.py paketle
```
Paket dosyalarını sıkıştırarak `<isim>-<surum>.zip` formatında bir arşiv dosyası üretir ve SHA256 imzasını konsola yazdırır.
