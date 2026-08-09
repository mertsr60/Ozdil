import { KeywordInfo, ExampleCode } from "./types";

export const KEYWORDS: KeywordInfo[] = [
  { keyword: 'yazdir', pythonEquivalent: 'print', description: 'Ekrana veya konsola çıktı verir.', usage: 'yazdir("Merhaba!")' },
  { keyword: 'eger', pythonEquivalent: 'if', description: 'Bir koşul bloğunu başlatır.', usage: 'eger x > 0:' },
  { keyword: 'degilse_eger', pythonEquivalent: 'elif', description: 'Önceki koşul sağlanmadığında yeni bir koşul kontrol eder.', usage: 'degilse_eger x == 0:' },
  { keyword: 'degilse', pythonEquivalent: 'else', description: 'Yukarıdaki hiçbir koşul sağlanmadığında çalışır.', usage: 'degilse:' },
  { keyword: 'dongu', pythonEquivalent: 'for', description: 'Belirli bir koleksiyonun tüm elemanlarını gezer (Döngü).', usage: 'dongu i icinde aralik(5):' },
  { keyword: 'her', pythonEquivalent: 'for', description: 'Elemanlar üzerinde dönmek için alternatif döngü kelimesi.', usage: 'her sayi icinde liste:' },
  { keyword: 'iken', pythonEquivalent: 'while', description: 'Belirtilen koşul doğru (dogru) olduğu sürece çalışır.', usage: 'iken x > 0:' },
  { keyword: 'fonksiyon', pythonEquivalent: 'def', description: 'Yeni bir fonksiyon tanımlar.', usage: 'fonksiyon topla(a, b):' },
  { keyword: 'islem', pythonEquivalent: 'def', description: 'Fonksiyon tanımlamak için alternatif anahtar kelime.', usage: 'islem kare_al(x):' },
  { keyword: 'dondur', pythonEquivalent: 'return', description: 'Fonksiyonun çalışmasını bitirip bir değer geri gönderir.', usage: 'dondur a + b' },
  { keyword: 'dogru', pythonEquivalent: 'True', description: 'Mantıksal DOĞRU boolean değeri.', usage: 'aktif = dogru' },
  { keyword: 'yanlis', pythonEquivalent: 'False', description: 'Mantıksal YANLIŞ boolean değeri.', usage: 'bitti = yanlis' },
  { keyword: 've', pythonEquivalent: 'and', description: 'Mantıksal VE operatörü. İki koşul da doğru olmalıdır.', usage: 'eger x ve y:' },
  { keyword: 'veya', pythonEquivalent: 'or', description: 'Mantıksal VEYA operatörü. Koşullardan biri doğru olmalıdır.', usage: 'eger x veya y:' },
  { keyword: 'degil', pythonEquivalent: 'not', description: 'Mantıksal DEĞİL (tersini alma) operatörü.', usage: 'eger degil bitti:' },
  { keyword: 'icinde', pythonEquivalent: 'in', description: 'Bir elemanın koleksiyonda olup olmadığını sorgular.', usage: 'eger "elma" icinde meyveler:' },
  { keyword: 'sinif', pythonEquivalent: 'class', description: 'Nesne tabanlı programlama (OOP) sınıfı tanımlar.', usage: 'sinif Araba:' },
  { keyword: 'dene', pythonEquivalent: 'try', description: 'Hata kontrolü yapılacak kod bloğunu başlatır.', usage: 'dene:' },
  { keyword: 'hata_yakala', pythonEquivalent: 'except', description: 'Oluşan bir hatayı yakalar ve programın çökmesini önler.', usage: 'hata_yakala ZeroDivisionError:' },
  { keyword: 'aralik', pythonEquivalent: 'range', description: 'Belirtilen sınırlar arasında sayı dizisi oluşturur.', usage: 'aralik(1, 11)' },
  { keyword: 'uzunluk', pythonEquivalent: 'len', description: 'Metin, liste veya sözlüğün eleman sayısını verir.', usage: 'uzunluk("Merhaba")' },
  { keyword: 'ekle', pythonEquivalent: 'append', description: 'Listenin sonuna yeni bir eleman ekler.', usage: 'sayilar.ekle(10)' },
  { keyword: 'tam_sayi', pythonEquivalent: 'int', description: 'Bir değeri tam sayı tipine dönüştürür.', usage: 'tam_sayi("123")' },
  { keyword: 'metin', pythonEquivalent: 'str', description: 'Bir değeri metin (string) tipine dönüştürür.', usage: 'metin(456)' },
  { keyword: 'ondalik', pythonEquivalent: 'float', description: 'Bir değeri ondalıklı sayı tipine dönüştürür.', usage: 'ondalik("3.14")' },
  { keyword: 'liste', pythonEquivalent: 'list', description: 'Yeni bir liste (dizi) tanımlar.', usage: 'liste = [1, 2, 3]' },
  { keyword: 'sozluk', pythonEquivalent: 'dict', description: 'Anahtar-değer çiftlerinden oluşan yeni bir sözlük tanımlar.', usage: 'sozluk = {"ad": "Mert"}' },
  { keyword: 'olarak', pythonEquivalent: 'as', description: 'Hata nesnesi veya modül için takma isim atar.', usage: 'hata_yakala ValueError olarak h:' },
  { keyword: 'getir', pythonEquivalent: 'import', description: 'Harici bir Python modülünü içe aktarır.', usage: 'getir math' },
  { keyword: 'dur', pythonEquivalent: 'break', description: 'Aktif döngüyü anında sonlandırır.', usage: 'dur' },
  { keyword: 'devam_et', pythonEquivalent: 'continue', description: 'Döngünün geri kalanını atlayıp sonraki tura geçer.', usage: 'devam_et' },
  { keyword: 'bos', pythonEquivalent: 'None', description: 'Değersizliği veya boşluğu ifade eder (None).', usage: 'sonuc = bos' }
];

export const EXAMPLES: ExampleCode[] = [
  {
    title: "Merhaba Dünya",
    description: "Yeni dilinizdeki ilk programınız! Ekrana yazı yazdırmayı ve basit değişkenleri öğrenin.",
    code: `# ÖzDil ile ilk programım!
ad = "Mert"
yazdir("Merhaba, Dünya!")
yazdir("Kodlama dilimize hoş geldin, " + ad + "!")
`
  },
  {
    title: "Eğer/Değilse Koşulları",
    description: "Sayısal karşılaştırmalar yapın ve 'eger', 'degilse_eger' ve 'degilse' bloklarını inceleyin.",
    code: `# Koşul kontrolleri
hava_durumu = "yagmurlu"
sicaklik = 14

yazdir("Hava Raporu:")
yazdir("Sıcaklık: " + metin(sicaklik) + " derece")

eger sicaklik < 10:
    yazdir("Hava oldukça soğuk, sıkı giyin!")
degilse_eger sicaklik >= 10 ve sicaklik < 20:
    yazdir("Ilık bir hava var.")
degilse:
    yazdir("Hava sıcak, keyfini çıkar!")

eger hava_durumu == "yagmurlu":
    yazdir("Şemsiyeni almayı unutma! ☔")
`
  },
  {
    title: "Sayı Döngüsü (Aralık)",
    description: "Belirli bir aralıktaki sayıları dönerek yazdırma ve toplama işlemleri.",
    code: `# Döngü ve Aralık Kullanımı
toplam = 0

# 1'den 10'a kadar olan sayıları topla (10 dahil değil)
dongu sayi icinde aralik(1, 10):
    yazdir("Şu anki sayı: " + metin(sayi))
    toplam = toplam + sayi

yazdir("1'den 9'a kadar olan sayıların toplamı: " + metin(toplam))
`
  },
  {
    title: "Faktöriyel Hesaplayıcı",
    description: "Özyinelemeli (recursive) bir fonksiyon ile faktöriyel hesabını gerçekleştirin.",
    code: `# Fonksiyon tanımlama ve özyineleme
fonksiyon faktoriyel_hesapla(n):
    # Sıfır veya bir durumunda 1 döndür
    eger n <= 1:
        dondur 1
    
    # n * (n-1)! hesapla
    dondur n * faktoriyel_hesapla(n - 1)

# Test edelim
sayi = 5
sonuc = faktoriyel_hesapla(sayi)
yazdir(metin(sayi) + " sayısının faktöriyeli = " + metin(sonuc))
`
  },
  {
    title: "Geri Sayım (while döngüsü)",
    description: "'iken' ifadesini kullanarak koşullu döngüler kurmayı öğrenin.",
    code: `# iken (while) döngüsü ile geri sayım
sayac = 5

yazdir("Geri sayım başlıyor...")
iken sayac > 0:
    yazdir("Kalan süre: " + metin(sayac) + " saniye")
    sayac = sayac - 1

yazdir("Fırlatma başarılı! 🚀")
`
  },
  {
    title: "Sınıf ve Nesne Yapısı",
    description: "Nesne tabanlı programlama (OOP) mantığını ve 'sinif' anahtar kelimesini kavrayın.",
    code: `# Sınıf (Sınıf / Class) Yapısı
sinif Kahraman:
    fonksiyon __init__(kendisi, ad, guc):
        kendisi.ad = ad
        kendisi.guc = guc
        kendisi.can = 100
        
    fonksiyon saldir(kendisi):
        dondur kendisi.ad + " " + metin(kendisi.guc) + " güç ile saldırdı! ⚔️"
        
    fonksiyon hasar_al(kendisi, miktar):
        kendisi.can = kendisi.can - miktar
        dondur kendisi.ad + " " + metin(miktar) + " hasar aldı, kalan can: " + metin(kendisi.can)

# Kahramanımızı yaratalım
savasci = Kahraman("Tarkan", 35)

yazdir("Kahraman adımız: " + savasci.ad)
yazdir(savasci.saldir())
yazdir(savasci.hasar_al(20))
`
  },
  {
    title: "Hata Yakalama (Try-Except)",
    description: "Beklenmeyen hatalara karşı 'dene' ve 'hata_yakala' kullanarak önlem alın.",
    code: `# Hata yakalama (try-except)
sayi_metni = "otuz_bes"

dene:
    # Sayıya çevirme hatası tetiklenecek
    sayi = tam_sayi(sayi_metni)
    yazdir("Başarıyla çevrildi: " + metin(sayi))
hata_yakala ValueError olarak hata:
    yazdir("Dönüştürme Hatası Yakalandı! Detay: " + metin(hata))
    yazdir("Lütfen geçerli bir sayısal metin giriniz.")
`
  }
];
