# 🚀 Varyn (ÖzDil) Programlama Dili ve Ekosistemi

**Varyn (ÖzDil)**, Türkçe sözdizimine (syntax) sahip, yüksek performanslı özel bir Bytecode Sanal Makinesi (VM) ve CPython yorumlayıcısı ile çalışan, asimetrik RSA imzalı paket yöneticisine ve güçlü sandbox mimarisine sahip modüler bir programlama dili ve ekosistemidir.

---

## 📌 İçindekiler
1. [Genel Bakış ve Mimari](#1-genel-bakış-ve-mimari)
2. [Çekirdek Dili Sözdizimi ve Temel Yapılar](#2-çekirdek-dili-sözdizimi-ve-temel-yapılar)
3. [Yerleşik (Built-in) Çekirdek Fonksiyonlar](#3-yerleşik-built-in-çekirdek-fonksiyonlar)
4. [Sanal Makine (VM) ve Güvenlik Sandboxı](#4-sanal-makine-vm-ve-güvenlik-sandboxı)
5. [Yetenek ve İzin (Capability) Yönetimi](#5-yetenek-ve-i̇zin-capability-yönetimi)
6. [Tüm Ekosistem Kütüphaneleri ve Fonksiyon Referansı (36 Paket)](#6-tüm-ekosistem-kütüphaneleri-ve-fonksiyon-referansı-36-paket)
    - [Saf (.varyn) Kütüphaneleri (11 Paket)](#-saf-varyn-kütüphaneleri)
    - [Uzantı ve Sistem Kütüphaneleri (25 Paket)](#-uzantı-ve-sistem-kütüphaneleri)
7. [Paket Yönetim Araçları (varynpaket & varynpip)](#7-paket-yönetim-araçları-varynpaket--varynpip)
8. [GUI Editörü ve Örnek Programlar](#8-gui-editörü-ve-örnek-programlar)

---

## 1. Genel Bakış ve Mimari

Varyn sistemi, kaynak kodu doğrudan çalıştırmak veya Bytecode opcodelarına derleyerek Sanal Makine üzerinde yürütmek üzere çift katmanlı bir altyapı sunar.

```text
  [ Varyn Kod (.varyn) ]
            │
            ▼
      [ Lexer / Tokalaştırıcı ]  ──> Token Listesi
            │
            ▼
       [ Parser / Ayrıştırıcı ]  ──> Soyut Sözdizim Ağacı (AST)
            │
      ┌─────┴─────────────────────────┐
      ▼                               ▼
[ Bytecode Derleyici (VM) ]    [ AST Yorumlayıcı (Legacy) ]
      │
      ▼
[ Varyn VM Yürütücü ] <────> [ Güvenlik Sandboxı & İzin Filtresi ]
```

### Ana Sistem Bileşenleri:
- **`compiler.py`**: Derleme önbelleği (`CompilationCache`) ile performanslı kod yürütme arayüzü.
- **`varyn_core/lexer.py`**: Türkçe anahtar kelimeleri ve sembolleri çözümleyen tokalaştırıcı.
- **`varyn_core/parser.py`**: Operator önceliklerini ve dil dilimlerini çözen parser.
- **`varyn_core/vm.py`**: Yığın tabanlı (stack-based) çalıştırma motoru ve bytecode işlemcisi.
- **`varyn_core/package_loader.py`**: Yerel/global paket yükleyici, RSA dijital imza doğrulayıcı ve SSRF koruyucu.
- **`varyn_core/sandbox.py`**: Python eklentilerini AST seviyesinde analiz eden güvenlik süzgeci.

---

## 2. Çekirdek Dili Sözdizimi ve Temel Yapılar

### Değişken ve Sabit Tanımlama
```varyn
değişken x = 10
değişken isim = "Varyn"
sabit PI = 3.14159
```

### Koşullu İfadeler
```varyn
değişken puan = 85

eger puan >= 90:
    yazdır("Mükemmel")
degilse_eger puan >= 70:
    yazdır("Başarılı")
degilse:
    yazdır("Geliştirilmeli")
```

### Döngüler
```varyn
# İken (While) Döngüsü
değişken sayac = 0
iken sayac < 5:
    yazdır(sayac)
    sayac = sayac + 1

# Aralık Döngüsü (For-in)
dongu i icinde aralik(0, 5):
    yazdır(i)
```

### Fonksiyonlar ve Sınıflar
```varyn
islem topla(a, b):
    dondur a + b

sinif Kisi:
    islem __init__(self, isim):
        self.isim = isim
    
    islem selamla(self):
        yazdır("Merhaba, " + self.isim)
```

---

## 3. Yerleşik (Built-in) Çekirdek Fonksiyonlar

Varyn çekirdeğinde herhangi bir kütüphane içe aktarmadan (`getir`) doğrudan kullanılabilen fonksiyonlar:

| Fonksiyon | Açıklama ve Kullanım |
| :--- | :--- |
| `yazdır(...)` / `yazdir(...)` | Ekrana / konsola metin veya nesne çıktısı verir. |
| `girdi(mesaj)` | Konsoldan kullanıcı girdisi alır. |
| `uzunluk(dizi_veya_metin)` | Metin, liste veya sözlüğün eleman sayısını döner (`len`). |
| `aralık(basla, bitir, adim)` | Sayı aralığı dizisi üretir (`range`). |
| `tam_sayi(deger)` | Değeri tam sayıya (`int`) dönüştürür. |
| `ondalik(deger)` | Değeri ondalıklı sayıya (`float`) dönüştürür. |
| `metin(deger)` | Değeri metne (`str`) dönüştürür. |
| `mantiksal(deger)` | Değeri boolean (`bool`) tipe dönüştürür. |
| `liste(koleksiyon)` | Yeni liste oluşturur veya dönüştürür. |
| `sozluk()` | Yeni sözlük oluşturur. |
| `mutlak(sayi)` | Sayının mutlak değerini (`abs`) döner. |
| `yuvarla(sayi, basamak)` | Sayıyı belirtilen basamağa yuvarlar (`round`). |
| `min_bul(dizi)` | Koleksiyondaki en küçük elemanı döner. |
| `max_bul(dizi)` | Koleksiyondaki en büyük elemanı döner. |

---

## 4. Sanal Makine (VM) ve Güvenlik Sandboxı

Varyn Sanal Makinesi (`varyn_core/vm.py`), komutları özel yığın mimarisinde (Stack VM) yürütür.

### Güvenlik Sınırları ve Koruma:
1. **Maksimum Yürütme Talimatı**: Sonsuz döngülere karşı varsayılan `1.000.000` komut limiti.
2. **Maksimum Çağrı Derinliği**: `1.000` özyineleme (recursion) derinliği sınırı.
3. **Maksimum Bellek / Dizi Boyutu**: Liste eleman sayısı `100.000`, metin uzunluğu `1.000.000` karakter.
4. **AST Sandbox Denetimi**: Python ile yazılmış eklentilerde `os.system`, `subprocess`, `eval`, `exec`, `open` gibi tehlikeli çağrılar ve dunder (`__subclasses__`) yöntemleri AST seviyesinde engellenir.
5. **Kriptografik RSA Doğrulaması**: Tüm paketlerin bütünlüğü 1024-bit RSA PKCS#1 v1.5 dijital imzasıyla doğrulanır.

---

## 5. Yetenek ve İzin (Capability) Yönetimi

Varyn paketleri güvenlik açısından yetenek tabanlı izinler gerektirebilir:
- `cap:network`: Ağ / HTTP istekleri (`ag_istemci`, `web`)
- `cap:filesystem`: Dosya sistemi işlemleri (`dosya`, `veritabani`)
- `cap:camera`: Kamera aygıtı erişimi (`kamera`)
- `cap:location`: Coğrafi konum verisi (`lokasyon`)

---

## 6. Tüm Ekosistem Kütüphaneleri ve Fonksiyon Referansı (36 Paket)

### 🌿 Saf (.varyn) Kütüphaneleri

Bu kütüphaneler herhangi bir Python bağımlılığı olmadan, **%100 saf Varyn sözdizimi** ile yazılmıştır.

#### 1. `algoritma` (v1.1.0)
*Saf Varyn temel algoritma kütüphanesi.*
- `sirala(dizi)`: Küçükten büyüğe sıralama yapar.
- `ikili_ara(dizi, hedef)`: Sıralı listede ikili arama yapar, hedef indisini döner.
- `en_buyuk(dizi)` / `en_kucuk(dizi)`: Uç değerleri bulur.
- `toplam(dizi)` / `ortalama(dizi)`: Aritmetik toplam ve ortalama hesaplar.
- `tersine_cevir(dizi)`: Diziyi tersine çevirir.
- `asal_mi(sayi)`: Sayının asal olup olmadığını kontrol eder.
- `ebob(a, b)` / `ekok(a, b)`: Ortak bölen ve katları hesaplar.
- `benzersizler(dizi)`: Tekrarlayan elemanları ayıklar.
- `fibonacci(n)`: N terimli Fibonacci dizisi döner.

#### 2. `kuyruk_yigin` (v1.0.0)
*Saf Varyn veri yapıları.*
- `yigin_olustur()`: Boş bir yığın (Stack) başlatır.
- `yigin_ekle(y, eleman)`: Yığının tepesine eleman ekler (`push`).
- `yigin_cikar(y)`: Yığının tepesindeki elemanı çıkarıp döner (`pop`).
- `yigin_bak(y)`: Yığının tepesindeki elemana bakar (`peek`).
- `yigin_bos_mu(y)`: Yığının boş olup olmadığını kontrol eder.
- `kuyruk_olustur()`: Boş bir kuyruk (Queue) başlatır.
- `kuyruk_ekle(k, eleman)`: Kuyruğun sonuna eleman ekler (`enqueue`).
- `kuyruk_cikar(k)`: Kuyruğun başındaki elemanı çıkarır (`dequeue`).
- `kuyruk_bak(k)`: Kuyruğun başındaki elemana bakar.
- `kuyruk_bos_mu(k)`: Kuyruğun boş olup olmadığını kontrol eder.
- `parantez_dengeli_mi(ifade)`: `()`, `[]`, `{}` parantezlerinin matematiksel denkliğini yığınla denetler.

#### 3. `matris` (v1.0.0)
*Saf Varyn lineer cebir ve matris matematiği.*
- `matris_olustur(satir, sutun, varsayilan)`: Belirtilen boyutta matris oluşturur.
- `birim_matris(boyut)`: NxN boyutunda birim matris (`Identity`) üretir.
- `matris_topla(m1, m2)`: İki matrisi toplar.
- `matris_cikar(m1, m2)`: İki matrisi çıkarır.
- `skaler_carp(m, katsayi)`: Matrisi skaler sayı ile çarpar.
- `transpoz_al(m)`: Matrisin satır ve sütunlarını yer değiştirir ($M^T$).
- `matris_carp(m1, m2)`: İki matrisin matris çarpımını ($M_1 \times M_2$) hesaplar.
- `determinant_2x2(m)`: 2x2 matrisin determinantını ($ad - bc$) hesaplar.
- `determinant_3x3(m)`: 3x3 matrisin determinantını Sarrus kuralıyla hesaplar.
- `iz_hesapla(m)`: Matrisin asal köşegen elemanlarının toplamını (`trace`) döner.

#### 4. `sayi_teorisi` (v1.0.0)
*Saf Varyn sayı teorisi ve matematiksel diziler.*
- `asal_carpanlar(n)`: Sayının tüm asal bölenlerini liste halinde döner.
- `armstrong_mu(n)`: Sayının Armstrong sayısı olup olmadığını denetler (örn: 153).
- `mukemmel_sayi_mi(n)`: Sayının tam bölenleri toplamına eşitliğini kontrol eder (örn: 28).
- `collatz_dizisi(baslangic)`: $3n+1$ Collatz adımlarını listeler.
- `pascal_ucgeni(satir_sayisi)`: N satırlı Pascal üçgeni üretir.
- `palindrom_sayi_mi(n)`: Sayının tersten okunuşunun eşitliğini kontrol eder.
- `moduler_us(taban, us, mod)`: Büyük sayılar için modüler üs alma ($a^b \pmod m$) yapar.

#### 5. `agac_graf` (v1.0.0)
*Saf Varyn ikili arama ağaçları ve çizge algoritmaları.*
- `bst_dugum_olustur(deger)`: Ağaç düğümü nesnesi üretir.
- `bst_ekle(kok, deger)`: İkili arama ağacına (BST) yeni eleman ekler.
- `bst_ara(kok, hedef)`: BST içinde aranan değerin varlığını `doğru`/`yanlış` olarak sorgular.
- `bst_sirali_dizi(kok)`: Ağaçtaki tüm elemanları sıralı (In-order) liste olarak döner.
- `graf_olustur()`: Boş bir Çizge (Graph) haritası oluşturur.
- `graf_kenar_ekle(graf, d1, d2)`: İki düğüm arasına yönsüz kenar ekler.
- `dugum_derecesi(graf, dugum)`: Düğümün komşu sayısını döner.
- `graf_bfs(graf, baslangic)`: Genişlik Öncelikli Arama (Breadth-First Search) ile çizgeyi gezer.

#### 6. `istatistik_pro` (v1.0.0)
*Saf Varyn ileri düzey istatistik ve korelasyon.*
- `varyans(dizi)`: Veri kümesinin varyansını ($\sigma^2$) hesaplar.
- `standart_sapma(dizi)`: Standart sapmayı ($\sigma$) Newton-Raphson kareköküyle bulur.
- `ceyrekler(dizi)`: Q1 (25%), Q2 (Medyan), Q3 (75%) kartil değerlerini hesaplar.
- `ceyrekler_acikligi(dizi)`: $IQR = Q3 - Q1$ değerini hesaplar.
- `min_max_olcekle(dizi)`: Verileri $[0.0, 1.0]$ aralığına normalize eder.
- `pearson_korelasyon(x, y)`: İki veri seti arasındaki Pearson korelasyon katsayısını ($r$) hesaplar.

#### 7. `metin_bicim` (v1.0.0)
*Saf Varyn metin dolgulama, biçimleme ve düzenleme mesafesi.*
- `metin_doldur_sol(metin, uzunluk, karakter)`: Metnin soluna dolgu ekler (`ljust`/`zfill`).
- `metin_doldur_sag(metin, uzunluk, karakter)`: Metnin sağına dolgu ekler (`rjust`).
- `kelimelere_ayir(cumle)`: Boşluklardan ayırarak kelime listesi yapar.
- `kelime_frekansi(cumle)`: Kelimelerin kullanım sayılarını sözlük olarak döner.
- `ters_cevir(metin)`: Metni tersine çevirir.
- `palindrom_metin_mi(metin)`: Metnin tersten okunuşunun aynılığını kontrol eder.
- `duzenleme_mesafesi(s1, s2)`: İki kelime arasındaki Levenshtein Düzenleme Mesafesini dinamik programlama ile hesaplar.

#### 8. `kripto_klasik` (v1.0.0)
*Saf Varyn klasik şifreleme yöntemleri.*
- `rot13(metin)`: Metni 13 harf kaydırarak ROT13 şifreler veya çözer.
- `atbash_sifrele(metin)`: Alfabeyi tersine çevirerek ($A \leftrightarrow Z$) Atbash şifrelemesi yapar.
- `vigenere_sifrele(metin, anahtar)`: Çok alfabeli (Polyalphabetic) Vigenère şifrelemesi yapar.
- `vigenere_coz(sifreli, anahtar)`: Vigenère şifreli metni anahtarla çözer.
- `cit_sifrele(metin, ray_sayisi)`: Zikzak ray (Rail Fence) transpozisyon şifrelemesi uygular.

#### 9. `siralama_koleksiyonu` (v1.0.0)
*Saf Varyn sıralama algoritmaları koleksiyonu.*
- `kabarcik_sirala(dizi)`: Kabarcık sıralaması (Bubble Sort) uygular.
- `secmeli_sirala(dizi)`: Seçmeli sıralama (Selection Sort) uygular.
- `eklemeli_sirala(dizi)`: Eklemeli sıralama (Insertion Sort) uygular.
- `saymali_sirala(dizi, max_deger)`: Saymalı sıralama (Counting Sort) uygular.
- `sirali_mi(dizi)`: Dizinin küçükten büyüğe sıralı olup olmadığını $O(n)$ sürede doğrular.

#### 10. `vektor_fizik` (v1.0.0)
*Saf Varyn 2D/3D vektör fiziği ve çarpışma motoru.*
- `vektor2d(x, y)`: 2D vektör nesnesi üretir.
- `vektor3d(x, y, z)`: 3D vektör nesnesi üretir.
- `vektor_topla(v1, v2)` / `vektor_cikar(v1, v2)`: Vektörel toplama ve çıkarma yapar.
- `vektor_olcekle(v, skaler)`: Vektörü skaler sayı ile genişletir/daraltır.
- `nokta_carpim(v1, v2)`: İç çarpım (Dot Product) hesaplar.
- `vektor_uzunluk(v)`: Vektörün Öklid normunu (büyüklüğünü) hesaplar.
- `vektor_birim(v)`: Vektörü normalize ederek birim vektör ($u = v / \|v\|$) yapar.
- `capraz_carpim_3d(v1, v2)`: 3D vektörlerin dik vektörel çapraz çarpımını ($v_1 \times v_2$) bulur.
- `aabb_carpismasi_mi(kutu1, kutu2)`: 2D Eksenle Hizalı Kutu (AABB) çarpışma denetimi yapar.

#### 11. `bulmaca_zeka` (v1.0.0)
*Saf Varyn zeka oyunları ve mantık algoritmaları.*
- `sudoku_4x4_dogrula(matris)`: 4x4 Sudoku tahtasının satır, sütun ve 2x2 blok kural geçerliliğini doğrular.
- `hanoi_hamleleri(disk_sayisi, kaynak, hedef, yardimci)`: Hanoi Kuleleri için gereken optimal disk taşıma adımlarını üretir.
- `vezir_tehditi_var_mi(pozisyonlar)`: N-Vezir probleminde satranç tahtasında vezirlerin birbirini tehdit edip etmediğini kontrol eder.
- `anagram_mi(kelime1, kelime2)`: İki kelimenin birbirinin harf diziliminden oluşup oluşmadığını denetler.

---

### 📦 Uzantı ve Sistem Kütüphaneleri

Python uzantısı ile çalışan, güvenli sanal alanda izole edilmiş zengin yardımcı modüller.

#### 12. `program` (Masaüstü & Pencere GUI Framework)
- `olustur(baslik, genislik, yukseklik, tema, ikon)`: Masaüstü penceresi başlatır.
- `menu_cubugu(ogeler)`: Üst menü barı ekler.
- `arac_cubugu(butonlar)`: Hızlı erişim araç butonları ekler.
- `kart(baslik, deger, alt_metin, ikon)`: İstatistik kartı ekler.
- `tablo(basliklar, satirlar)`: Dinamik veri tablosu (Grid) oluşturur.
- `metin_kutusu(etiket, deger, ipucu)` / `sayi_kutusu(...)` / `onay_kutusu(...)`: Form giriş alanları ekler.
- `terminal_kutusu(loglar)`: Konsol log akış alanı ekler.
- `durum_cubugu(sol, sag, durum)`: Alt durum bildirim çubuğu ekler.

#### 13. `telefon` (Mobil Simülatör GUI)
- `baslik(metin)`: Mobil üst başlık barı.
- `yazi(metin, stil)`: Mobil ekrana stilize metin ekler.
- `buton(metin, mesaj)`: Etkileşimli buton bileşeni ekler.
- `kart(baslik, icerik)`: Mobil kart bileşeni ekler.

#### 14. `yapay_zeka`
- `dogrusal_regresyon_egit(x, y)`: Lineer regresyon modeli eğitir.
- `dogrusal_regresyon_tahmin_et(model, x)`: Eğitilmiş modelle tahmin yapar.
- `k_ortalama_kumele(noktalar, k, iterasyon)`: K-Means kümeleme algoritması.
- `knn_siniflandir(egitim, test, k)`: K-En Yakın Komşu sınıflandırması.
- `yapay_sinir_hucresi(girdiler, agirliklar, sapma, aktivasyon)`: Perseptron simülatörü.

#### 15. `finans`
- `faiz_hesapla(anapara, oran, yil)`: Bileşik faiz getirisi hesaplar.
- `doviz_cevir(tutar, kur)`: Para birimi dönüştürür.
- `enflasyon_etkisi(tutar, oran, yil)`: Alım gücü erimesini hesaplar.
- `kredi_taksit(tutar, faiz, vade)`: Aylık eşit taksit tutarı çıkarır.

#### 16. `geometri`
- `daire_alani(r)` / `daire_cevresi(r)`: Daire hesaplamaları.
- `ucgen_alani(taban, h)`: Üçgen alanı.
- `hipotenus(a, b)`: Pisagor teoremi ile hipotenüs bulur.
- `kure_hacmi(r)`: Küre hacmi hesaplar.

#### 17. `fizik`
- `hiz(yol, zaman)`: Ortalama hız hesabı.
- `kuvvet(kutle, ivme)`: $F = m \cdot a$ Newton yasası.
- `kinetik_enerji(m, v)` / `potansiyel_enerji(m, h, g)`: Enerji denklemleri.
- `serbest_dusme_mesafesi(t, g)`: Yerçekimi serbest düşüşü.

#### 18. `veri_analizi`
- `medyan(dizi)` / `mod(dizi)` / `aciklik(dizi)`: Tanımlayıcı istatistikler.
- `z_skoru(dizi)`: Verilerin Z standart puanlarını çıkarır.

#### 19. `oyun`
- `tas_kagit_makas(secim)`: Bilgisayara karşı oyun oynatır.
- `sayi_tahmin_et(hedef, tahmin)`: Tahmin rehberi sağlar.
- `zar_at()`: 1-6 arası zar simülasyonu.
- `skor_tablosu(oyuncular, puanlar)`: Skor sıralaması yapar.

#### 20. `renkler`
- `rgb_to_hex(r, g, b)` / `hex_to_rgb(hex_kod)`: Renk uzayı dönüşümleri.
- `renk_karistir(r1, g1, b1, r2, g2, b2, oran)`: İki rengi harmanlar.

#### 21. `hesap`
- `yuzde_hesapla(sayi, yuzde)` / `kdv_ekle(fiyat, oran)` / `indirim_uygula(fiyat, indirim)`: Ticari hesaplamalar.

#### 22. `grafik` (Canvas GUI)
- `cizgi(x1, y1, x2, y2, renk)` / `dikdortgen(x, y, w, h, renk)` / `daire(cx, cy, r, renk)`: 2D çizim ilkel nesneleri.

#### 23. `veritabani` (Anahtar-Değer Deposu)
- `ayarla(anahtar, deger)` / `al(anahtar, varsayilan)` / `sil(anahtar)` / `tumunu_al()`: Kalıcı veri saklama.

#### 24. `muhasebe`
- `gelir_gider_raporu(gelirler, giderler)`: Net kar/zarar ve bilanço çıkarır.
- `amortisman_hesapla(maliyet, hurda_deger, faydali_omur)`: Yıllık amortisman payını hesaplar.

#### 25. `ses_muzik`
- `nota_frekansi(nota)`: Nota isminden (örn: "A4", "C4") Hz frekansını döner.
- `akor_notalari(kok, tur)`: Akor dizilimi oluşturur.

#### 26. `sifreleme_araclari`
- `morse_kodla(metin)` / `morse_coz(kod)`: Mors alfabesi dönüştürücü.
- `ikili_kodla(metin)` / `ikili_coz(ikili)`: İkili (Binary 0101) çevirici.

#### 27. `otomasyon`
- `gorev_zamanla(ad, saniye)`: Zamanlanmış görev tanımlar.
- `is_akisi_calistir(adimlar)`: Sıralı süreç zinciri işletir.

#### 28. `ag_istemci` (`cap:network`)
- `get_istegi(url)`: Güvenli HTTP GET isteği gönderir.
- `post_istegi(url, veri)`: JSON gövdeli HTTP POST isteği gönderir.

#### 29. `kamera` (`cap:camera`)
- `kamera_baslat()` / `kare_yakala()` / `kamera_kapat()`: Sanal kamera aygıtı arayüzü.

#### 30. `lokasyon` (`cap:location`)
- `mevcut_konum()` / `haversine_mesafe(lat1, lon1, lat2, lon2)`: Coğrafi koordinat ve mesafe hesabı.

#### 31. `donusturucu`
- `celcius_fahrenheit(c)` / `km_mil(km)` / `kg_libre(kg)` / `bayt_donustur(bayt, birim)`: Birim dönüştürücüler.

#### 32. `matematik`
- `karekök(x)`, `faktöriyel(n)`, `sinüs(x)`, `kosinüs(x)`, `derece(r)`, `radyan(d)`, `ebob(a,b)`.

#### 33. `rastgele`
- `tamsayı_seç(min, max)`, `ondalık_seç()`, `seç(liste)`, `karıştır(liste)`, `sifre_olustur(uzunluk)`.

#### 34. `tarih_saat`
- `simdi()`, `turkce_tarih(y, m, d)`, `gun_farki(t1, t2)`, `gun_ekle(t, gun)`, `artik_yil_mi(yil)`.

#### 35. `metin_isleme`
- `turkce_kucult(s)`, `turkce_buyut(s)`, `slug_yap(s)`, `sesli_say(s)`, `kelime_say(s)`.

#### 36. `kripto`
- `md5_uret(s)`, `sha256_uret(s)`, `sha1_uret(s)`, `base64_kodla(s)`, `base64_coz(s)`, `sezar_sifrele(s, key)`.

---

## 7. Paket Yönetim Araçları (varynpaket & varynpip)

Varyn paketleri bağımsız dizinler halinde `varyn_packages/` altında tutulur ve merkezi `varyn/repository.py` deposu üzerinden yönetilir.

### CLI Komutları:
```bash
# Depodaki tüm paketleri listele
python3 -m varyn.varynpip listele

# Paket ara
python3 -m varyn.varynpip ara matris

# Paketi doğrula ve yükle
python3 -m varyn.varynpip yukle kuyruk_yigin

# Kurulu paketi kaldır
python3 -m varyn.varynpip kaldir kuyruk_yigin

# Paket bilgilerini incele
python3 -m varyn.varynpip bilgi sayi_teorisi
```

---

## 8. GUI Editörü ve Örnek Programlar

Varyn Web IDE arayüzü; Kod Editörü, Konsol Çıktısı, Bytecode Görüntüleyici, Sözlük/Kütüphane Rehberi, Paket Yöneticisi ve Örnekler sekmesinden oluşur.

IDE üzerindeki **Örnekler** menüsünden 36 paketin her birine ait hazır test kodları tek tıkla editöre yüklenebilir ve anında çalıştırılabilir!
