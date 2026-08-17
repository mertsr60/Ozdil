import { KeywordInfo, ExampleCode } from "./types";

export const KEYWORDS: KeywordInfo[] = [
  { keyword: 'yazdir', pythonEquivalent: 'print', description: 'Ekrana veya konsola çıktı verir.', usage: 'yazdir("Merhaba!")' },
  { keyword: 'girdi', pythonEquivalent: 'input', description: 'Kullanıcıdan konsol aracılığıyla etkileşimli girdi alır.', usage: 'ad = girdi("Adınızı girin: ")' },
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
  { keyword: 'bos', pythonEquivalent: 'None', description: 'Değersizliği veya boşluğu ifade eder (None).', usage: 'sonuc = bos' },
  // Built-in Libraries
  { keyword: 'matematik', pythonEquivalent: 'math', description: 'Matematiksel fonksiyonlar ve sabitler kütüphanesi.', usage: 'getir matematik' },
  { keyword: 'karekök', pythonEquivalent: 'sqrt', description: 'Bir sayının karekökünü hesaplar.', usage: 'matematik.karekök(16)' },
  { keyword: 'faktöriyel', pythonEquivalent: 'factorial', description: 'Bir tam sayının faktöriyelini hesaplar.', usage: 'matematik.faktöriyel(5)' },
  { keyword: 'üs', pythonEquivalent: 'pow', description: 'Tabanın belirtilen üssünü alır (x^y).', usage: 'matematik.üs(2, 3)' },
  { keyword: 'sinüs', pythonEquivalent: 'sin', description: 'Radyan cinsinden açının sinüsünü hesaplar.', usage: 'matematik.sinüs(0.5)' },
  { keyword: 'kosinüs', pythonEquivalent: 'cos', description: 'Radyan cinsinden açının kosinüsünü hesaplar.', usage: 'matematik.kosinüs(0.5)' },
  { keyword: 'tanjant', pythonEquivalent: 'tan', description: 'Radyan cinsinden açının tanjantını hesaplar.', usage: 'matematik.tanjant(0.5)' },
  { keyword: 'radyan', pythonEquivalent: 'radians', description: 'Derece cinsinden bir açıyı radyana çevirir.', usage: 'matematik.radyan(180)' },
  { keyword: 'derece', pythonEquivalent: 'degrees', description: 'Radyan cinsinden bir açıyı dereceye çevirir.', usage: 'matematik.derece(3.14)' },
  { keyword: 'aşağı_yuvarla', pythonEquivalent: 'floor', description: 'Bir ondalıklı sayıyı en yakın küçük tam sayıya yuvarlar.', usage: 'matematik.aşağı_yuvarla(3.8)' },
  { keyword: 'yukarı_yuvarla', pythonEquivalent: 'ceil', description: 'Bir ondalıklı sayıyı en yakın büyük tam sayıya yuvarlar.', usage: 'matematik.yukarı_yuvarla(3.1)' },
  { keyword: 'ebob', pythonEquivalent: 'gcd', description: 'İki tam sayının En Büyük Ortak Bölenini (EBOB) verir.', usage: 'matematik.ebob(12, 18)' },
  { keyword: 'mutlak_deger', pythonEquivalent: 'abs', description: 'Bir sayının mutlak değerini hesaplar.', usage: 'matematik.mutlak_deger(-5)' },
  { keyword: 'faktoriyel', pythonEquivalent: 'factorial (alternative)', description: 'Bir sayının faktöriyelini hesaplar (Türkçe karakter içermeyen alternatif kullanım).', usage: 'matematik.faktoriyel(5)' },
  { keyword: 'rastgele', pythonEquivalent: 'random', description: 'Rastgele sayı ve seçim işlemleri kütüphanesi.', usage: 'getir rastgele' },
  { keyword: 'tamsayı_seç', pythonEquivalent: 'randint', description: 'Belirlenen iki sınır arasında rastgele bir tam sayı seçer (sınırlar dahil).', usage: 'rastgele.tamsayı_seç(1, 10)' },
  { keyword: 'ondalık_seç', pythonEquivalent: 'random', description: '0.0 ile 1.0 arasında rastgele ondalıklı bir sayı üretir.', usage: 'rastgele.ondalık_seç()' },
  { keyword: 'seç', pythonEquivalent: 'choice', description: 'Bir listeden rastgele bir eleman seçer.', usage: 'rastgele.seç(["elma", "armut", "muz"])' },
  { keyword: 'karıştır', pythonEquivalent: 'shuffle', description: 'Bir listenin elemanlarının sırasını rastgele karıştırır.', usage: 'rastgele.karıştır(liste)' },
  { keyword: 'örnek_seç', pythonEquivalent: 'sample', description: 'Bir koleksiyondan belirtilen miktarda benzersiz rastgele eleman seçer.', usage: 'rastgele.örnek_seç(liste, 2)' },
  { keyword: 'zaman', pythonEquivalent: 'time', description: 'Zaman ve tarih işlemleri kütüphanesi.', usage: 'getir zaman' },
  { keyword: 'bekle', pythonEquivalent: 'sleep', description: 'Programı belirtilen saniye boyunca duraklatır.', usage: 'zaman.bekle(2)' },
  { keyword: 'yerel_zaman', pythonEquivalent: 'localtime', description: 'Mevcut yerel saat ve tarih yapısını döner.', usage: 'zaman.yerel_zaman()' },
  { keyword: 'tarih_saat', pythonEquivalent: 'ctime', description: 'Mevcut zamanı okunabilir bir metin formatında verir.', usage: 'zaman.tarih_saat()' },
  { keyword: 'web', pythonEquivalent: 'urllib', description: 'İnternet ve web işlemleri kütüphanesi.', usage: 'getir web' },
  { keyword: 'getir', pythonEquivalent: 'get', description: 'Belirtilen URL adresinden GET isteği yaparak yanıtı metin olarak döner.', usage: 'web.getir("https://example.com")' },
  { keyword: 'gönder', pythonEquivalent: 'post', description: 'Belirtilen URL adresine POST isteği ile veri gönderir.', usage: 'web.gönder("https://httpbin.org/post", {"veri": "değer"})' },
  { keyword: 'sistem', pythonEquivalent: 'sys/os', description: 'İşletim sistemi ve program çalıştırma ortamı kütüphanesi.', usage: 'getir sistem' },
  { keyword: 'dosya_var_mı', pythonEquivalent: 'exists', description: 'Belirtilen yolda bir dosyanın mevcut olup olmadığını kontrol eder.', usage: 'sistem.dosya_var_mı("kodumuz.varyn")' },
  { keyword: 'çıkış', pythonEquivalent: 'exit', description: 'Programı belirtilen durum kodu ile anında sonlandırır.', usage: 'sistem.çıkış(0)' },
  { keyword: 'json', pythonEquivalent: 'json', description: 'JSON formatında veri işleme kütüphanesi.', usage: 'getir json' },
  { keyword: 'çöz', pythonEquivalent: 'loads', description: 'JSON formatındaki bir metni Varyn sözlüğüne veya listesine dönüştürür.', usage: 'json.çöz(\'{"ad": "Mert"}\')' },
  { keyword: 'kodla', pythonEquivalent: 'dumps', description: 'Varyn listesini veya sözlüğünü JSON formatında bir metne dönüştürür.', usage: 'json.kodla({"ad": "Mert"})' },
  { keyword: 'dosya', pythonEquivalent: 'open', description: 'Dosya okuma, yazma ve ekleme işlemleri kütüphanesi.', usage: 'getir dosya' },
  { keyword: 'oku', pythonEquivalent: 'read', description: 'Belirtilen dosyanın içeriğini metin olarak okur.', usage: 'dosya.oku("veri.txt")' },
  { keyword: 'yaz', pythonEquivalent: 'write', description: 'Belirtilen dosyaya metin yazar (öncekileri siler).', usage: 'dosya.yaz("veri.txt", "Merhaba!")' },
  { keyword: 'ekle', pythonEquivalent: 'append', description: 'Belirtilen dosyanın sonuna metin ekler.', usage: 'dosya.ekle("veri.txt", "Yeni satır")' },
  // New Libraries
  { keyword: 'telefon', pythonEquivalent: 'telefon', description: 'Mobil telefon GUI kütüphanesini içe aktarmak veya kullanmak için anahtar kelime.', usage: 'getir telefon' },
  { keyword: 'baslik', pythonEquivalent: 'baslik', description: 'Simüle edilen telefon ekranına başlık barı ekler.', usage: 'telefon.baslik("Benim Uygulamam")' },
  { keyword: 'yazi', pythonEquivalent: 'yazi', description: 'Telefon ekranına metin ekler (baslik, alt_baslik, uyari, basarili stilleri desteklenir).', usage: 'telefon.yazi("Merhaba Varyn!", "normal")' },
  { keyword: 'buton', pythonEquivalent: 'buton', description: 'Telefon ekranına etkileşimli bir buton ekler. Tıklandığında bildirim tetikler.', usage: 'telefon.buton("Giriş Yap", "Giriş işlemi başlatıldı!")' },
  { keyword: 'kart', pythonEquivalent: 'kart', description: 'Telefon ekranına şık bir kart bileşeni ekler.', usage: 'telefon.kart("Haberler", "Varyn kütüphaneleri genişliyor!")' },
  { keyword: 'tarih_saat', pythonEquivalent: 'datetime', description: 'Gelişmiş Türkçe tarih, zaman ve gün farkı kütüphanesi.', usage: 'getir tarih_saat' },
  { keyword: 'simdi', pythonEquivalent: 'now', description: 'Mevcut tarih ve saat bileşenlerini içeren bir sözlük döndürür.', usage: 'tarih_saat.simdi()' },
  { keyword: 'turkce_tarih', pythonEquivalent: 'strftime (TR)', description: 'Tarihi Türkçe gün ve ay isimleriyle biçimlendirir.', usage: 'turkce_tarih(2026, 8, 4)' },
  { keyword: 'gun_farki', pythonEquivalent: 'timedelta', description: 'İki tarih (YYYY-MM-DD) arasındaki gün farkını hesaplar.', usage: 'gun_farki("2026-08-01", "2026-08-10")' },
  { keyword: 'gun_ekle', pythonEquivalent: 'date addition', description: 'Belirtilen tarihe gün sayısı ekleyerek yeni bir tarih döndürür.', usage: 'tarih_saat.gun_ekle("2026-08-08", 10)' },
  { keyword: 'artik_yil_mi', pythonEquivalent: 'is leap year', description: 'Verilen yılın artık yıl olup olmadığını kontrol eder (doğru/yanlış döner).', usage: 'tarih_saat.artik_yil_mi(2024)' },
  { keyword: 'metin_isleme', pythonEquivalent: 'str utils', description: 'Türkçe karakter duyarlı metin dönüştürme ve analiz kütüphanesi.', usage: 'getir metin_isleme' },
  { keyword: 'turkce_kucult', pythonEquivalent: 'lower', description: 'Türkçe I/ı ve İ/i harflerini doğru şekilde küçültür.', usage: 'turkce_kucult("İSTANBUL")' },
  { keyword: 'turkce_buyut', pythonEquivalent: 'upper', description: 'Türkçe I/ı ve İ/i harflerini doğru şekilde büyütür.', usage: 'turkce_buyut("istanbul")' },
  { keyword: 'slug_yap', pythonEquivalent: 'slugify', description: 'Metni Türkçe uyumlu URL / SEO dostu slug formatına çevirir.', usage: 'slug_yap("Varyn Harika Bir Dil!")' },
  { keyword: 'sesli_say', pythonEquivalent: 'vowel count', description: 'Metindeki sesli harflerin sayısını bulur.', usage: 'sesli_say("Varyn")' },
  { keyword: 'kelime_say', pythonEquivalent: 'word count', description: 'Metindeki kelime sayısını hesaplar.', usage: 'metin_isleme.kelime_say("Varyn Harika!")' },
  { keyword: 'ters_cevir', pythonEquivalent: 'reverse string', description: 'Metni tersine çevirir.', usage: 'metin_isleme.ters_cevir("Varyn")' },
  { keyword: 'kripto', pythonEquivalent: 'hashlib/base64', description: 'Veri özetleme, kodlama/çözme ve Sezar şifreleme kütüphanesi.', usage: 'getir kripto' },
  { keyword: 'md5_uret', pythonEquivalent: 'md5', description: 'Metnin MD5 özet değerini üretir.', usage: 'kripto.md5_uret("şifre")' },
  { keyword: 'sha256_uret', pythonEquivalent: 'sha256', description: 'Metnin SHA256 özet değerini üretir.', usage: 'kripto.sha256_uret("şifre")' },
  { keyword: 'sha1_uret', pythonEquivalent: 'sha1', description: 'Metnin SHA1 özet değerini üretir.', usage: 'kripto.sha1_uret("şifre")' },
  { keyword: 'base64_kodla', pythonEquivalent: 'b64encode', description: 'Metni Base64 formatında kodlar.', usage: 'kripto.base64_kodla("özdil")' },
  { keyword: 'base64_coz', pythonEquivalent: 'b64decode', description: 'Base64 formatında kodlanmış metni çözer.', usage: 'kripto.base64_coz("b3pkaWw=")' },
  { keyword: 'sezar_sifrele', pythonEquivalent: 'caesar cipher', description: 'Metni belirtilen anahtar kadar kaydırarak Sezar şifrelemesi uygular.', usage: 'kripto.sezar_sifrele("merhaba", 3)' },
  { keyword: 'sezar_coz', pythonEquivalent: 'caesar decipher', description: 'Şifrelenmiş metni belirtilen anahtarla çözer.', usage: 'kripto.sezar_coz("phukded", 3)' },
  { keyword: 'rastgele_sayi', pythonEquivalent: 'randint', description: 'Rastgele sayı kütüphanesinden iki sınır arasında tam sayı üretir.', usage: 'rastgele.rastgele_sayi(10, 50)' },
  { keyword: 'sifre_olustur', pythonEquivalent: 'password generator', description: 'İstenen uzunlukta harf, rakam ve sembollerden oluşan güvenli şifre üretir.', usage: 'rastgele.sifre_olustur(12)' },
  { keyword: 'rastgele_renk', pythonEquivalent: 'hex color', description: 'Rastgele altı haneli onaltılık (hex) renk kodu üretir.', usage: 'rastgele.rastgele_renk()' },
  { keyword: 'bozuk_para_at', pythonEquivalent: 'coin flip', description: 'Yazı veya tura şeklinde yazı sonucu simüle eder.', usage: 'rastgele.bozuk_para_at()' },
  // Finans Kütüphanesi
  { keyword: 'finans', pythonEquivalent: 'finans', description: 'Bileşik faiz hesaplama, döviz çevirme, enflasyon etkisi ve kredi taksit tablosu çıkaran finansal analiz kütüphanesi.', usage: 'getir finans' },
  { keyword: 'faiz_hesapla', pythonEquivalent: 'compound interest', description: 'Bileşik faiz formülü kullanarak toplam birikimi hesaplar.', usage: 'finans.faiz_hesapla(10000, 15, 3)' },
  { keyword: 'doviz_cevir', pythonEquivalent: 'currency convert', description: 'Verilen tutarı belirtilen döviz kuru ile çarparak çevirir.', usage: 'finans.doviz_cevir(100, 33.45)' },
  { keyword: 'enflasyon_etkisi', pythonEquivalent: 'inflation impact', description: 'Enflasyon oranı karşısında paranın alım gücündeki değişimi hesaplar.', usage: 'finans.enflasyon_etkisi(50000, 45, 2)' },
  { keyword: 'kredi_taksit', pythonEquivalent: 'loan installment', description: 'Verilen kredi tutarı, yıllık faiz oranı ve vadeye göre aylık taksiti hesaplar.', usage: 'finans.kredi_taksit(120000, 36, 12)' },
  // Oyun Kütüphanesi
  { keyword: 'oyun', pythonEquivalent: 'oyun', description: 'Taş-kağıt-makas simülasyonu, sayı tahmin rehberliği, şans zarları ve skor tablosu oluşturucu içeren eğlenceli oyun araçları.', usage: 'getir oyun' },
  { keyword: 'tas_kagit_makas', pythonEquivalent: 'rock paper scissors', description: 'Bilgisayara karşı taş, kağıt, makas oyunu oynatır.', usage: 'oyun.tas_kagit_makas("tas")' },
  { keyword: 'sayi_tahmin_et', pythonEquivalent: 'number guessing guide', description: 'Girilen tahminin hedefe göre durumunu "yukarı", "aşağı" veya "doğru" şeklinde döndürür.', usage: 'oyun.sayi_tahmin_et(42, 35)' },
  { keyword: 'zar_at', pythonEquivalent: 'roll dice', description: '1 ile 6 arasında rastgele bir zar atma simülasyonu yapar.', usage: 'oyun.zar_at()' },
  { keyword: 'skor_tablosu', pythonEquivalent: 'leaderboard formatter', description: 'Oyuncu isimleri ve puan listelerini şık bir liderlik tablosu formatında birleştirir.', usage: 'oyun.skor_tablosu(["Alper", "Buse"], [1500, 2450])' },
  // Algoritma Kütüphanesi (%100 Varyn ile yazılmıştır)
  { keyword: 'algoritma', pythonEquivalent: 'algorithms', description: 'Tamamen Varyn ile yazılmış ilk kütüphane. Sıralama, arama, istatistik ve sayı teorisi algoritmaları barındırır.', usage: 'getir algoritma' },
  { keyword: 'sirala', pythonEquivalent: 'bubble sort', description: 'Verilen listeyi sıralama algoritmasıyla küçükten büyüğe sıralar.', usage: 'algoritma.sirala([5, 2, 9, 1, 7])' },
  { keyword: 'ikili_ara', pythonEquivalent: 'binary search', description: 'Sıralı bir listede hedef değeri ikili arama algoritmasıyla arar; indisini veya -1 döndürür.', usage: 'algoritma.ikili_ara([1, 2, 5, 7, 9], 7)' },
  { keyword: 'en_buyuk', pythonEquivalent: 'find max', description: 'Verilen listenin en büyük elemanını bulur.', usage: 'algoritma.en_buyuk([5, 2, 9, 1, 7])' },
  { keyword: 'en_kucuk', pythonEquivalent: 'find min', description: 'Verilen listenin en küçük elemanını bulur.', usage: 'algoritma.en_kucuk([5, 2, 9, 1, 7])' },
  { keyword: 'toplam', pythonEquivalent: 'sum', description: 'Listenin elemanlarının toplamını hesaplar.', usage: 'algoritma.toplam([5, 2, 9, 1, 7])' },
  { keyword: 'ortalama', pythonEquivalent: 'average', description: 'Listenin elemanlarının aritmetik ortalamasını hesaplar.', usage: 'algoritma.ortalama([5, 2, 9, 1, 7])' },
  { keyword: 'tersine_cevir', pythonEquivalent: 'reverse', description: 'Verilen listenin elemanlarının sırasını tersine çevirir.', usage: 'algoritma.tersine_cevir([5, 2, 9, 1, 7])' },
  { keyword: 'asal_mi', pythonEquivalent: 'is_prime', description: 'Bir sayının asal olup olmadığını kontrol eder (doğru/yanlış döner).', usage: 'algoritma.asal_mi(17)' },
  { keyword: 'ebob', pythonEquivalent: 'gcd', description: 'İki tam sayının En Büyük Ortak Bölenini (EBOB) hesaplar.', usage: 'algoritma.ebob(12, 18)' },
  { keyword: 'ekok', pythonEquivalent: 'lcm', description: 'İki tam sayının En Küçük Ortak Katını (EKOK) hesaplar.', usage: 'algoritma.ekok(12, 18)' },
  { keyword: 'benzersizler', pythonEquivalent: 'unique elements', description: 'Listedeki yinelenen elemanları temizleyerek sadece benzersiz elemanları içeren yeni bir liste döndürür.', usage: 'algoritma.benzersizler([1, 2, 2, 3, 3, 4])' },
  { keyword: 'fibonacci', pythonEquivalent: 'fibonacci sequence', description: 'N elemanlı Fibonacci sayı dizisi üretir.', usage: 'algoritma.fibonacci(10)' },
  // Yapay Zeka Kütüphanesi (%100 Varyn ile yazılmıştır)
  { keyword: 'yapay_zeka', pythonEquivalent: 'artificial intelligence / ML', description: 'Tamamen %100 Varyn ile yazılmış yapay zeka ve makine öğrenmesi kütüphanesi.', usage: 'getir yapay_zeka' },
  { keyword: 'dogrusal_regresyon_egit', pythonEquivalent: 'train linear regression', description: 'Verilen X ve Y koordinatları için doğrusal regresyon modeli eğiterek eğim ve kesim noktasını döndürür.', usage: 'yapay_zeka.dogrusal_regresyon_egit([1, 2, 3], [2, 4, 5])' },
  { keyword: 'dogrusal_regresyon_tahmin_et', pythonEquivalent: 'predict linear regression', description: 'Eğitilmiş model üzerinden X değeri için tahminde bulunur.', usage: 'yapay_zeka.dogrusal_regresyon_tahmin_et(model, 4)' },
  { keyword: 'k_ortalama_kumele', pythonEquivalent: 'K-Means clustering', description: 'Çok boyutlu veri noktalarını K gruba kümeleyen makine öğrenmesi algoritması.', usage: 'yapay_zeka.k_ortalama_kumele([[1,1], [5,5]], 2, 5)' },
  { keyword: 'knn_siniflandir', pythonEquivalent: 'K-Nearest Neighbors classification', description: 'En yakın K adet eğitim örneğine bakarak test noktasının kategorisini sınıflandırır.', usage: 'yapay_zeka.knn_siniflandir(egitim, test, 3)' },
  { keyword: 'yapay_sinir_hucresi', pythonEquivalent: 'artificial neuron simulation', description: 'Girdiler, ağırlıklar, sapma ve aktivasyon fonksiyonu (relu, adim, yok) ile yapay sinir hücresini (perseptron) simüle eder.', usage: 'yapay_zeka.yapay_sinir_hucresi([0.5, 0.2], [1, -1], 0.1, "relu")' },
  // Masaüstü ve Pencere Programı Kütüphanesi (program)
  { keyword: 'program', pythonEquivalent: 'gui window software framework', description: 'ÖzDil ile tam donanımlı masaüstü programları, form uygulamaları, veri panelleri ve pencereli yazılımlar geliştirme kütüphanesi.', usage: 'getir program' },
  { keyword: 'olustur', pythonEquivalent: 'create window', description: 'Yeni bir masaüstü pencere uygulaması başlatır.', usage: 'program.olustur("Program Adı", 640, 480, "karanlik")' },
  { keyword: 'menu_cubugu', pythonEquivalent: 'menubar', description: 'Pencerenin üstüne Dosya, Düzenle gibi masaüstü menü çubuğu ekler.', usage: 'program.menu_cubugu(["Dosya", "Düzenle", "Görünüm", "Yardım"])' },
  { keyword: 'arac_cubugu', pythonEquivalent: 'toolbar', description: 'Pencereye hızlı erişim araç çubuğu butonları ekler.', usage: 'program.arac_cubugu(["Yeni", "Kaydet", "Çalıştır", "Ayarlar"])' },
  { keyword: 'metin_kutusu', pythonEquivalent: 'input text field', description: 'Kullanıcıdan metin girdisi almak için form kutusu ekler.', usage: 'program.metin_kutusu("Kullanıcı Adı", "Mert", "Adınızı yazın")' },
  { keyword: 'sayi_kutusu', pythonEquivalent: 'number spinbox', description: 'Sayısal giriş kutusu ekler.', usage: 'program.sayi_kutusu("Miktar", 1, 100, 10)' },
  { keyword: 'onay_kutusu', pythonEquivalent: 'checkbox', description: 'Onay kutusu (Checkbox) ekler.', usage: 'program.onay_kutusu("Beni Hatırla", dogru)' },
  { keyword: 'secim_kutusu', pythonEquivalent: 'dropdown combobox', description: 'Açılır seçim kutusu (Dropdown) ekler.', usage: 'program.secim_kutusu("Kategori", ["Elektronik", "Giyim", "Kitap"])' },
  { keyword: 'kaydirici', pythonEquivalent: 'slider', description: 'Değer aralığı kaydırıcısı (Slider) ekler.', usage: 'program.kaydirici("Ses Düzeyi", 0, 100, 75)' },
  { keyword: 'tablo', pythonEquivalent: 'data table grid', description: 'Dinamik veri tablosu / grid bileşeni oluşturur.', usage: 'program.tablo(["ID", "Ürün", "Fiyat"], [["1", "Laptop", "25.000 TL"]])' },
  { keyword: 'kod_kutusu', pythonEquivalent: 'code viewer / editor', description: 'Program içine kod düzenleme ve görüntüleme alanı ekler.', usage: 'program.kod_kutusu("# Kod buraya", "varyn")' },
  { keyword: 'terminal_kutusu', pythonEquivalent: 'embedded terminal / logs', description: 'Pencere içine gömülü konsol ve log akış alanı ekler.', usage: 'program.terminal_kutusu(["[Sistem] Hazır..."])' },
  { keyword: 'durum_cubugu', pythonEquivalent: 'statusbar', description: 'Pencerenin altına durum çubuğu ekler.', usage: 'program.durum_cubugu("Hazır", "v1.0.0", "tamam")' },
  { keyword: 'ornek_program', pythonEquivalent: 'run preset program template', description: 'Hazır program şablonlarını çalıştırır (hesap_makinesi, not_defteri, gorev_yoneticisi, veri_tablosu).', usage: 'program.ornek_program("hesap_makinesi")' },
  // Saf Varyn Veri Yapıları ve Matematik Kütüphaneleri (%100 Saf .varyn)
  { keyword: 'kuyruk_yigin', pythonEquivalent: 'stack & queue data structures', description: 'Saf Varyn ile Yığın (LIFO), Kuyruk (FIFO) ve parantez sözdizimi doğrulayıcı kütüphanesi.', usage: 'getir kuyruk_yigin' },
  { keyword: 'matris', pythonEquivalent: 'matrix linear algebra', description: 'Saf Varyn ile matris toplama, çarpma, determinant, transpoz ve birim matris kütüphanesi.', usage: 'getir matris' },
  { keyword: 'sayi_teorisi', pythonEquivalent: 'number theory & sequences', description: 'Saf Varyn ile asal çarpanlar, Armstrong sayıları, Collatz dizisi, Pascal üçgeni ve mükemmel sayılar.', usage: 'getir sayi_teorisi' },
  { keyword: 'agac_graf', pythonEquivalent: 'binary search tree & graph', description: 'Saf Varyn ile İkili Arama Ağacı (BST), Çizge temsili, kenar ekleme ve BFS genişlik öncelikli arama.', usage: 'getir agac_graf' },
  { keyword: 'istatistik_pro', pythonEquivalent: 'advanced statistics & correlation', description: 'Saf Varyn ile varyans, standart sapma, kartiller/çeyrekler, min-max ölçekleme ve Pearson korelasyonu.', usage: 'getir istatistik_pro' },
  { keyword: 'metin_bicim', pythonEquivalent: 'string formatting & levenshtein', description: 'Saf Varyn ile metin dolgulama, ters çevirme, kelime frekansı ve Levenshtein düzenleme mesafesi.', usage: 'getir metin_bicim' },
  { keyword: 'kripto_klasik', pythonEquivalent: 'classical cryptography', description: 'Saf Varyn ile ROT13, Atbash, Vigenère ve Çit (Rail Fence) şifreleme algoritmaları.', usage: 'getir kripto_klasik' },
  { keyword: 'siralama_koleksiyonu', pythonEquivalent: 'sorting algorithms collection', description: 'Saf Varyn ile Kabarcık, Seçmeli, Eklemeli ve Saymalı sıralama algoritmaları koleksiyonu.', usage: 'getir siralama_koleksiyonu' },
  { keyword: 'vektor_fizik', pythonEquivalent: '2D/3D vector math & AABB physics', description: 'Saf Varyn ile 2D/3D vektör toplamı, nokta çarpım, birim vektör ve AABB kutu çarpışma testi.', usage: 'getir vektor_fizik' },
  { keyword: 'bulmaca_zeka', pythonEquivalent: 'puzzle & logic algorithms', description: 'Saf Varyn ile 4x4 Sudoku doğrulayıcı, Hanoi kuleleri adımları, N-Vezir tehdit kontrolü ve anagram testi.', usage: 'getir bulmaca_zeka' }
];

export const EXAMPLES: ExampleCode[] = [
  {
    title: "Merhaba Dünya",
    description: "Yeni dilinizdeki ilk programınız! Ekrana yazı yazdırmayı ve basit değişkenleri öğrenin.",
    code: `# Varyn ile ilk programım!
ad = "Mert"
yazdir("Merhaba, Dünya!")
yazdir("Kodlama dilimize hoş geldin, " + ad + "!")
`
  },
  {
    title: "Etkileşimli Girdi (girdi)",
    description: "Konsoldan veri okuyarak etkileşimli yaş ve isim hesaplamaları yapın.",
    code: `# Kullanıcıdan girdi alma örneği
ad = girdi("Adınızı girin: ")
yas_metni = girdi("Yaşınızı girin: ")

yas = tam_sayi(yas_metni)

yazdir("Merhaba, " + ad + "!")
yazdir("Şu an " + yas_metni + " yaşındasınız.")

gelecek_yas = yas + 5
yazdir("5 yıl sonra " + metin(gelecek_yas) + " yaşında olacaksınız!")
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
  },
  {
    title: "Kütüphane Kullanımı (math, random, time)",
    description: "Matematik, Rastgele ve Zaman modüllerini Türkçe kodlayarak harika uygulamalar yapın.",
    code: `# Türkçe Kütüphane Paketlerinin Kullanımı

getir matematik
getir rastgele
getir zaman

yazdir("--- Matematik Kütüphanesi ---")
yazdir("Pi Sayısı: " + metin(matematik.pi))
yazdir("9 sayısının karekökü: " + metin(matematik.karekök(9)))
yazdir("5 sayısının faktöriyeli: " + metin(matematik.faktöriyel(5)))
yazdir("Dereceyi radyana çevir (180): " + metin(matematik.radyan(180)))

yazdir("")
yazdir("--- Rastgele Kütüphanesi ---")
rastgele_sayi = rastgele.tamsayı_seç(1, 100)
yazdir("1 ile 100 arasında rastgele sayı: " + metin(rastgele_sayi))

meyveler = ["elma", "armut", "muz", "çilek"]
secilen_meyve = rastgele.seç(meyveler)
yazdir("Sizin için rastgele seçilen meyve: " + secilen_meyve)

yazdir("")
yazdir("--- Zaman Kütüphanesi ---")
yazdir("Tarih ve Saat: " + zaman.tarih_saat())
yazdir("Zamanlayıcı başlatılıyor. 1.5 saniye bekleniyor...")
zaman.bekle(1.5)
yazdir("Bekleme süresi doldu! Program başarıyla tamamlandı. 🎉")
`
  },
  {
    title: "Gelişmiş Kütüphaneler",
    description: "Yeni eklenen tarih_saat, metin_isleme, kripto ve rastgele paketlerini deneyin.",
    code: `# Gelişmiş Standart Kütüphanelerimizin Kullanımı
# Not: varynpip sekmesinden bu kütüphaneleri (örn: tarih_saat) kurabilirsiniz.

getir tarih_saat
getir metin_isleme
getir kripto
getir rastgele

yazdir("--- Tarih ve Saat Paketleri ---")
zaman_sozlugu = tarih_saat.simdi()
yazdir("Şimdi (Sözlük):", zaman_sozlugu)
yazdir("Örnek Türkçe Tarih:", turkce_tarih(2026, 8, 4))
yazdir("Bugün:", turkce_tarih())
yazdir("Gün Farkı:", gun_farki("2026-08-01", "2026-08-10"))

yazdir("")
yazdir("--- Gelişmiş Türkçe Metin İşleme ---")
yazdir("Büyük Harf Çevirisi (istanbul):", turkce_buyut("istanbul"))
yazdir("Küçük Harf Çevirisi (İSTANBUL):", turkce_kucult("İSTANBUL"))
yazdir("URL / Slug Oluşturma:", slug_yap("Varyn Harika Bir Programlama Dili!"))
yazdir("Sesli Harf Sayısı:", sesli_say("Varyn Türkçe"))

yazdir("")
yazdir("--- Kripto ve Güvenlik ---")
metin_degeri = "varyn_sifreleme_123"
yazdir("MD5 Özeti  :", kripto.md5_uret(metin_degeri))
yazdir("SHA256 Özeti:", kripto.sha256_uret(metin_degeri))
b64 = kripto.base64_kodla(metin_degeri)
yazdir("Base64 Kodlu:", b64)
yazdir("Base64 Çözülmüş:", kripto.base64_coz(b64))
yazdir("Sezar Şifreleme (anahtar: 3):", kripto.sezar_sifrele("merhaba", 3))

yazdir("")
yazdir("--- Rastgele Veri ve Şifre Üretici ---")
yazdir("Rastgele Sayı (100-500):", rastgele.rastgele_sayi(100, 500))
yazdir("Rastgele Seçim (renkler):", rastgele.rastgele_sec(["kırmızı", "yeşil", "mavi", "sarı"]))
yazdir("Rastgele Güvenli Şifre (16 hane):", rastgele.sifre_olustur(16))
`
  },
  {
    title: "Finans Analizi",
    description: "Bileşik faiz hesaplama, döviz çevirme, kredi taksitleri ve enflasyonun alım gücü etkilerini analiz edin.",
    code: `# Varyn Finans Analiz Kütüphanesi Örneği
getir finans

yazdir("=== ÖZDİL FİNANS ANALİZ ARACI ===")

# 1. Bileşik Faiz Hesaplama (Ana Para: 10000 TL, Yıllık Faiz: %15, Süre: 3 Yıl)
ana_para = 10000
faiz_orani = 15
yil = 3
bilesik_bakiye = finans.faiz_hesapla(ana_para, faiz_orani, yil)
yazdir(metin(yil) + " yıl sonunda bileşik faizli toplam bakiye: " + metin(bilesik_bakiye) + " TL")

# 2. Döviz Çevirici (Dolar kuru: 33.45, Elimizdeki Tutar: 250 USD)
usd_tutari = 250
usd_kuru = 33.45
tl_tutari = finans.doviz_cevir(usd_tutari, usd_kuru)
yazdir(metin(usd_tutari) + " USD = " + metin(tl_tutari) + " TL")

# 3. Enflasyonun Alım Gücüne Etkisi (Tutar: 50000 TL, Yıllık Enflasyon: %45, Süre: 2 Yıl)
para = 50000
enflasyon = 45
sure_yil = 2
gelecek_alim_gucu = finans.enflasyon_etkisi(para, enflasyon, sure_yil)
yazdir("Bugünkü " + metin(para) + " TL'nin " + metin(sure_yil) + " yıl sonraki alım gücü: " + metin(gelecek_alim_gucu) + " TL")

# 4. Kredi Taksit Hesaplayıcı (Kredi Tutarı: 120000 TL, Yıllık Faiz Oranı: %36, Vade: 12 Ay)
kredi_miktari = 120000
kredi_faiz_yillik = 36
vade_ay = 12
aylik_taksit = finans.kredi_taksit(kredi_miktari, kredi_faiz_yillik, vade_ay)
toplam_geri_odeme = aylik_taksit * vade_ay
yazdir("Aylık Kredi Taksiti (120bin TL / 12 ay): " + metin(aylik_taksit) + " TL")
yazdir("Toplam Kredi Geri Ödemesi: " + metin(toplam_geri_odeme) + " TL")
`
  },
  {
    title: "Retro Oyunlar",
    description: "Taş-kağıt-makas simülasyonu, şans zarları, sayı tahmin ipuçları ve dinamik skor tablosu.",
    code: `# Varyn Retro Oyun Paketleri Örneği
getir oyun

yazdir("=== ÖZDİL EĞLENCELİ RETRO OYUNLAR ===")

# 1. Taş-Kağıt-Makas Oyunu
yazdir("--- Taş-Kağıt-Makas Oyunu ---")
yazdir(oyun.tas_kagit_makas("tas"))
yazdir(oyun.tas_kagit_makas("kağıt"))

# 2. Şans Zarları
yazdir("")
yazdir("--- Şans Zarları ---")
zar1 = oyun.zar_at()
zar2 = oyun.zar_at()
yazdir("1. Zar: " + metin(zar1) + " | 2. Zar: " + metin(zar2))
eger zar1 + zar2 == 12:
    yazdir("Tebrikler, düşeş attınız! 🎲🎉")
degilse_eger zar1 == zar2:
    yazdir("Çift attınız! 🎲")

# 3. Sayı Tahmin Yardımcısı
yazdir("")
yazdir("--- Sayı Tahmin Yardımcısı ---")
gizli_sayi = 42
tahmin = 35
ipucu = oyun.sayi_tahmin_et(gizli_sayi, tahmin)
yazdir("Gizli sayı: " + metin(gizli_sayi) + ", Tahmininiz: " + metin(tahmin) + " -> Hedef için yön: " + ipucu)

# 4. Skor Tablosu Oluşturucu
yazdir("")
yazdir("--- Skor Tablosu ---")
oyuncular = ["Alper", "Buse", "Can", "Derin"]
skorlar = [1500, 2450, 1820, 2980]
tablo = oyun.skor_tablosu(oyuncular, skorlar)
yazdir(tablo)
`
  },
  {
    title: "Mobil Profil Kartı Tasarımı",
    description: "Varyn 'telefon' kütüphanesi kullanarak şık bir profil kartı arayüzü tasarlayın.",
    code: `# Varyn Mobil GUI Kütüphanesi - Profil Tasarımı
getir telefon

# Profil şablonunu otomatik yükle
telefon.ornekler("profil")

yazdir("Profil arayüzü başarıyla oluşturuldu! Sonuçları sağdaki Telefon Ekranında görebilirsiniz.")
`
  },
  {
    title: "Mobil Hava Durumu Ekranı",
    description: "Varyn 'telefon' kütüphanesinin ilerleme çubukları ve özel hava durumu stillerini inceleyin.",
    code: `# Varyn Mobil GUI Kütüphanesi - Hava Durumu Tasarımı
getir telefon

# Hava durumu şablonunu otomatik yükle
telefon.ornekler("hava_durumu")

yazdir("Hava durumu arayüzü başarıyla yüklendi! Sağdaki Telefon Ekranına göz atın.")
`
  },
  {
    title: "Özel Mobil Giriş Formu",
    description: "Girdiler, anahtarlar ve butonlar içeren etkileşimli bir giriş formu arayüzü oluşturun.",
    code: `# Varyn Mobil GUI Kütüphanesi - Giriş Formu Tasarımı
getir telefon

# Arka planı kirli beyaz yapalım
telefon.arka_plan("kirli_beyaz")

# Başlık ve açıklama yazıları ekleyelim
telefon.baslik("Varyn Giriş Ekranı")
telefon.yazi("Hesabınıza Giriş Yapın", "baslik")
telefon.yazi("Lütfen bilgilerinizi eksiksiz doldurun.", "alt_baslik")

# Giriş alanları (girdiler) ekleyelim
telefon.girdi("Kullanıcı Adı")
telefon.girdi("Parola")

# Seçenek anahtarları ekleyelim
telefon.anahtar("Beni Hatırla", dogru)
telefon.anahtar("Kullanım Sözleşmesini Kabul Ediyorum", yanlis)

# Bir ilerleme çubuğuyla şifre gücünü simüle edelim
telefon.yazi("Şifre Gücü: %85", "normal")
telefon.ilerleme(85)

# Tıklanabilir bir buton ekleyelim (ikinci parametre tıklama uyarısıdır)
telefon.buton("Giriş Yap", "Giriş talebi iletildi! Hoş geldiniz. 🎉")

# Kayıt formu arayüzü oluşturuldu. Telefon Ekranında butona tıklayarak bildirimleri tetikleyebilirsiniz!")
`
  },
  {
    title: "Sistem Hız Testi (Benchmark)",
    description: "Tüm kütüphaneleri (matematik, kripto, rastgele, veri_analizi, metin_isleme, zaman) kullanarak sistemin işlem hızını ölçün.",
    code: `# Varyn Sistem Performans & Benchmark Hız Testi
getir zaman
getir telefon
getir kripto
getir rastgele
getir veri_analizi
getir metin_isleme

yazdir("==========================================")
yazdir("    ÖZDİL SİSTEM PERFORMANS TESTİ BAŞLADI  ")
yazdir("==========================================")

# Başlangıç zamanını milisaniye cinsinden kaydet
baslangic = zaman.zaman_damgasi()

# 1. TEST: MATEMATİK & DÖNGÜ HIZI
yazdir("[1/5] Matematik ve Döngü performansı test ediliyor...")
toplam = 0
dongu i icinde aralik(1, 1000):
    kare = karekok(i)
    kup = us(i, 3)
    toplam = toplam + kare + kup

# 2. TEST: KRİPTOGRAFİ HASH ÜRETİMİ
yazdir("[2/5] Kriptografik hash fonksiyonları test ediliyor...")
metin_ornek = "Turkce ozgundur ve Varyn ile kodlanir! 1234567890"
md5_sonuc = kripto.md5_uret(metin_ornek)
sha256_sonuc = kripto.sha256_uret(metin_ornek)

dongu j icinde aralik(1, 100):
    dummy_hash = kripto.sha256_uret(metin_ornek + metin(j))

# 3. TEST: RASTGELE SAYI & LİSTE İŞLEMLERİ
yazdir("[3/5] Rastgele sayı üretimi ve dizi karıştırma test ediliyor...")
sayilar = []
dongu k icinde aralik(1, 50):
    rast_sayi = rastgele.rastgele_sayi(1, 1000)
    sayilar.append(rast_sayi)

rastgele.rastgele_karistir(sayilar)

# 4. TEST: VERİ ANALİZİ İSTATİSTİKLERİ
yazdir("[4/5] Veri analizi kütüphanesi ile istatistik çıkarılıyor...")
ortalama_deger = veri_analizi.ortalama(sayilar)
medyan_deger = veri_analizi.medyan(sayilar)

# 5. TEST: METİN İŞLEME VE DİL İŞLEVLERİ
yazdir("[5/5] Türkçe metin işleme ve slug dönüşümleri yapılıyor...")
buyuk_metin = metin_isleme.turkce_buyut("özdil ile kodlama dili hızı muhteşem!")
slug_metin = metin_isleme.slug_yap("özdil ile kodlama dili hızı muhteşem!")

# Bitiş zamanı ve geçen süreyi hesapla
bitis = zaman.zaman_damgasi()
gecen_sure = bitis - baslangic

# Performans puanı hesapla (gecen_sure ne kadar az ise puan o kadar yüksek)
# 0.1 saniye (100 ms) altı mükemmel kabul edilir
puan = 100 - (gecen_sure * 150)
eger puan > 100:
    puan = 100
degilse_eger puan < 10:
    puan = 10

puan_tamsayi = tam_sayi(puan)

yazdir("==========================================")
yazdir("             TEST SONUÇLARI               ")
yazdir("==========================================")
yazdir("Toplam Geçen Süre: " + metin(gecen_sure) + " saniye")
yazdir("Hesaplama Matematik Toplamı: " + metin(toplam))
yazdir("Üretilen MD5: " + md5_sonuc)
yazdir("Üretilen SHA-256: " + sha256_sonuc)
yazdir("Rastgele Sayılar Ortalaması: " + metin(ortalama_deger))
yazdir("Rastgele Sayılar Medyanı: " + metin(medyan_deger))
yazdir("Dönüştürülen Başlık: " + buyuk_metin)
yazdir("Dönüştürülen Web Adresi: " + slug_metin)
yazdir("Sistem Performans Puanı: " + metin(puan_tamsayi) + " / 100")
yazdir("==========================================")

# TELEFON GUI RAPORU
# Telefon ekranında sonuçları zengin bir dashboard ile sunalım
telefon.arka_plan("gok_mavisi")
telefon.baslik("Varyn Hız Testi")

telefon.yazi("Hız Ölçüm Raporu", "baslik")
telefon.yazi("Tüm kütüphaneler başarıyla benchmark edildi.", "alt_baslik")

telefon.kart("Süre Analizi", "Tüm algoritmalar ve eklentiler " + metin(gecen_sure) + " saniyede başarıyla tamamlandı.")

# Skor çubuğu
telefon.yazi("Performans Skoru: %" + metin(puan_tamsayi), "normal")
telefon.ilerleme(puan_tamsayi)

eger puan_tamsayi >= 90:
    telefon.yazi("Sistem Hızı: MÜKEMMEL (Ultra Hızlı)", "basarili")
degilse_eger puan_tamsayi >= 70:
    telefon.yazi("Sistem Hızı: ÇOK İYİ (Hızlı)", "basarili")
degilse:
    telefon.yazi("Sistem Hızı: NORMAL (Yeterli)", "normal")

# Ölçülen diğer değerleri kart olarak gösterelim
telefon.kart("Kriptografi", "SHA256: " + sha256_sonuc)
telefon.kart("İstatistik", "Ort: " + metin(ortalama_deger) + " | Medyan: " + metin(medyan_deger))

telefon.buton("Testi Tekrarla", "Performans testi ve benchmark yeniden koşturuluyor... ⚡")
`
  },
  {
    title: "Etkileşimli Canlı Renk Paleti",
    description: "Canlı olay dinleyicileri (event listeners) kullanarak butona tıklanınca rengi ve içeriği dinamik olarak güncelleyin.",
    code: `# Varyn Mobil GUI - Canlı Etkileşimli Olay Sistemi (Event Listeners)
getir telefon

telefon.arka_plan("kirli_beyaz")
telefon.baslik("Etkileşimli Renk Paleti")
telefon.yazi("Canlı Olay Sistemi", "baslik")
telefon.yazi("Butonlara tıklayarak canlı durum değişikliklerini tetikleyin!", "alt_baslik")

# Olay fonksiyonları tanımlayalım
fonksiyon mavi_yap():
    telefon.arka_plan("gok_mavisi")
    telefon.yazi("Arka plan gök mavisi olarak güncellendi! 💙", "basarili")

fonksiyon kirmizi_yap():
    telefon.arka_plan("gece_mavisi")
    telefon.yazi("Arka plan gece mavisine büründü! 🌌", "basarili")

fonksiyon sifirla():
    telefon.arka_plan("kirli_beyaz")
    telefon.yazi("Renk paleti sıfırlandı! 🤍", "normal")

# Olayları kütüphaneye bağlayalım
telefon.olay_ekle("mavi_olay", mavi_yap)
telefon.olay_ekle("kirmizi_olay", kirmizi_yap)
telefon.olay_ekle("sifirla_olay", sifirla)

# Butonlarımızı oluşturalım ve olay kimliklerini bağlayalım
telefon.buton("Gök Mavisi Yap", "mavi_olay")
telefon.buton("Gece Mavisi Yap", "kirmizi_olay")
telefon.buton("Sıfırla", "sifirla_olay")

yazdir("Etkileşimli renk paleti hazırlandı! Telefon Simülatöründe butonlara basarak deneyin.")
`
  },
  {
    title: "Varyn Saf Algoritmalar (%100 Varyn Kütüphanesi)",
    description: "Tamamen Varyn ile yazılmış ilk kütüphane olan 'algoritma' modülü ile sıralama, ikili arama, istatistik ve sayı teorisi işlemlerini gerçekleştirin.",
    code: `# %100 Varyn ile kodlanmış ilk kütüphane (algoritma.varyn) kullanımı!
getir algoritma

yazdir("==========================================")
yazdir("     ÖZDİL ALGORİTMALAR KÜTÜPHANESİ TESTİ  ")
yazdir("==========================================")

# 1. Sıralama ve Arama Testi
sayilar = [12, 5, 29, 1, 77, 4, 33]
yazdir("Orijinal Sayılar:", sayilar)

sirali = algoritma.sirala(sayilar)
yazdir("Sıralanmış Sayılar:", sirali)

hedef = 29
indis = algoritma.ikili_ara(sirali, hedef)
yazdir("Değer: " + metin(hedef) + " | Sıralı Listedeki İndisi: " + metin(indis))

# 2. İstatistiksel Hesaplamalar
en_b = algoritma.en_buyuk(sayilar)
en_k = algoritma.en_kucuk(sayilar)
toplam_deger = algoritma.toplam(sayilar)
ortalama_deger = algoritma.ortalama(sayilar)

yazdir("------------------------------------------")
yazdir("En Büyük Değer : " + metin(en_b))
yazdir("En Küçük Değer : " + metin(en_k))
yazdir("Eleman Toplamı : " + metin(toplam_deger))
yazdir("Aritmetik Ort. : " + metin(ortalama_deger))

# 3. Liste İşlemleri
ters_sayilar = algoritma.tersine_cevir(sayilar)
yazdir("Ters Çevrilmiş : " + metin(ters_sayilar))

yinelenenler = [1, 5, 5, 2, 2, 2, 7, 1, 9]
benzersiz = algoritma.benzersizler(yinelenenler)
yazdir("Yinelenenli Dizi:", yinelenenler)
yazdir("Benzersiz Dizi   :", benzersiz)

# 4. Matematik & Sayı Teorisi
yazdir("------------------------------------------")
ebob_sonuc = algoritma.ebob(48, 18)
ekok_sonuc = algoritma.ekok(12, 15)

yazdir("EBOB(48, 18)    : " + metin(ebob_sonuc))
yazdir("EKOK(12, 15)    : " + metin(ekok_sonuc))

yazdir("13 sayısı asal mı? : " + metin(algoritma.asal_mi(13)))
yazdir("21 sayısı asal mı? : " + metin(algoritma.asal_mi(21)))
yazdir("==========================================")
`
  },
  {
    title: "Yapay Zeka (%100 Varyn Makine Öğrenmesi)",
    description: "Tamamen Varyn ile yazılmış 'yapay_zeka' modülü ile regresyon, K-Means kümeleme, k-NN sınıflandırma ve yapay sinir hücresi simülasyonu yapın.",
    code: `# %100 Varyn ile kodlanmış Yapay Zeka kütüphanesi (yapay_zeka.varyn) kullanımı!
getir yapay_zeka

yazdir("==========================================")
yazdir("     ÖZDİL YAPAY ZEKA VE ML TESTİ         ")
yazdir("==========================================")

# 1. Doğrusal Regresyon (Linear Regression)
yazdir("[1] DOĞRUSAL REGRESYON (TAHMİN MODELİ)")
değişken ev_buyuklukleri = [50, 70, 90, 110, 130]
değişken ev_fiyatlari = [1500, 2100, 2600, 3100, 3800]

değişken model = yapay_zeka.dogrusal_regresyon_egit(ev_buyuklukleri, ev_fiyatlari)
yazdir("Eğitilen Model Parametreleri:")
yazdir(" - Eğim (w):", model["egim"])
yazdir(" - Kesim Noktası (b):", model["kesim_noktasi"])

değişken yeni_ev = 100
değişken tahmin_fiyat = yapay_zeka.dogrusal_regresyon_tahmin_et(model, yeni_ev)
yazdir(" -> " + metin(yeni_ev) + " m2 ev için fiyat tahmini: " + metin(tahmin_fiyat) + " bin TL")
yazdir("------------------------------------------")

# 2. K-Means Clustering (Kümeleme)
yazdir("[2] K-MEANS KÜMELEME ALGORİTMASI")
değişken veri_noktalari = [
    [1.0, 1.0], [1.5, 1.2], [1.2, 0.8],
    [5.0, 5.0], [5.5, 5.2], [4.8, 4.9]
]

değişken k_sonuc = yapay_zeka.k_ortalama_kumele(veri_noktalari, 2, 5)
yazdir("Bulunan Küme Merkezleri:")
yazdir(" - Merkez 1:", k_sonuc["merkezler"][0])
yazdir(" - Merkez 2:", k_sonuc["merkezler"][1])
yazdir("------------------------------------------")

# 3. K-Nearest Neighbors (k-NN Sınıflandırma)
yazdir("[3] K-EN YAKIN KOMŞU (k-NN) SINIFLANDIRMA")
değişken egitim_seti = [
    [[1, 2], "meyve"], [[1.5, 1.8], "meyve"],
    [[8, 9], "sebze"], [[9, 10], "sebze"]
]
değişken test_nesnesi = [1.2, 2.1]
değişken sinif_sonucu = yapay_zeka.knn_siniflandir(egitim_seti, test_nesnesi, 3)
yazdir("Test Nesnesi [1.2, 2.1] Sınıflandırma Sonucu:", sinif_sonucu)
yazdir("------------------------------------------")

# 4. Yapay Sinir Hücresi (Single Perceptron Node)
yazdir("[4] YAPAY SİNİR HÜCRESİ SİMÜLASYONU")
değişken girdiler = [0.8, -0.5]
değişken agirliklar = [2.0, 1.2]
değişken sapma = -0.4

değişken sonuc_relu = yapay_zeka.yapay_sinir_hucresi(girdiler, agirliklar, sapma, "relu")
değişken sonuc_adim = yapay_zeka.yapay_sinir_hucresi(girdiler, agirliklar, sapma, "adim")

yazdir("Yapay Sinir Hücresi Çıktıları:")
yazdir(" - ReLU Aktivasyonlu:", sonuc_relu)
yazdir(" - Adım (Step) Aktivasyonlu:", sonuc_adim)
yazdir("==========================================")
`
  },
  {
    title: "Masaüstü Envanter ve Stok Yönetim Programı (program)",
    description: "Yeni 'program' kütüphanesini kullanarak menü çubuğu, araçlar, arama kutusu, veri tablosu ve istatistik kartları içeren tam donanımlı masaüstü yazılımı oluşturun.",
    code: `# Yeni 'program' kütüphanesi ile Masaüstü Envanter ve Satış Yönetim Programı!
getir program

# 1. Uygulama Penceresi Oluştur
program.olustur("Envanter & Depo Yönetim Sistemi v2.0", 720, 520, "karanlik", "kutu")

# 2. Üst Menü Çubuğu
program.menu_cubugu(["Dosya", "Kayıtlar", "Raporlar", "Veri Tabanı", "Yardım"])

# 3. Hızlı Eylem Araç Çubuğu
program.arac_cubugu(["Yeni Ürün", "Dışa Aktar (CSV)", "Filtrele", "Yedek Al"])

# 4. Program Başlığı ve Açıklaması
program.baslik("Depo ve Stok Kontrol Merkezi", "Gerçek zamanlı ürün ve stok takip yazılımı")

# 5. Özet İstatistik Kartları
program.kart("Toplam Ciro", "148.500 ₺", "+%14 Bu Hafta", "para")
program.kart("Kritik Stok Uyarıları", "2 Ürün", "Dikkat", "uyari")

# 6. Dinamik Veri Tablosu (Grid)
program.tablo(["Barkod", "Ürün Adı", "Kategori", "Birim Fiyat", "Stok"], [
    ["869001", "Varyn Ultra Dizüstü", "Bilgisayar", "32.500 ₺", "14 Adet"],
    ["869002", "RGB Mekanik Klavye", "Donanım", "1.450 ₺", "85 Adet"],
    ["869003", "Kablosuz Oyuncu Faresi", "Aksesuar", "420 ₺", "110 Adet"],
    ["869004", "27 inç 165Hz Monitör", "Ekran", "6.900 ₺", "4 Adet"]
])

# 7. Form Alanları ve Etkileşim Butonu
program.metin_kutusu("Hızlı Ürün Arama", "", "Ürün adı veya barkod giriniz...")
program.buton("Yeni Ürün Kaydı Ekle", "yeni_urun_ac", "basari", "arti")

# 8. Pencereli Durum Çubuğu
program.durum_cubugu("4 Ürün Kaydı Listelendi", "Sistem: Çevrimiçi | v2.0.0", "tamam")

yazdir("Masaüstü envanter programı başarıyla çalıştırıldı!")
`
  },
  {
    title: "Sistem ve Süreç Yöneticisi Programı (program)",
    description: "CPU/RAM metrikleri, işlem tablosu, ilerleme çubukları ve terminal logları içeren gelişmiş bir sistem yönetim aracı.",
    code: `# Sistem ve Görev Yöneticisi Masaüstü Programı
getir program

program.olustur("Varyn Sistem & Süreç Yöneticisi", 700, 500, "karanlik", "sistem")
program.menu_cubugu(["İşlemler", "Performans", "Ağ", "Görünüm", "Yardım"])
program.arac_cubugu(["Yenile", "Süreç Durdur", "Öncelik Ata", "Ayarlar"])

program.baslik("Performans ve Görevler", "Sistem kaynakları optimum seviyede")

program.kart("İşlemci (CPU)", "%16 Aktif (4 Çekirdek)", "Normal", "islemci")
program.kart("Bellek (RAM)", "3.2 GB / 16.0 GB", "%20", "bellek")

program.ilerleme(20, "RAM Kullanım Durumu: %20")

program.tablo(["PID", "İşlem Adı", "Kullanıcı", "CPU %", "RAM"], [
    ["1024", "varyn_ide_core", "mert", "%8.2", "120 MB"],
    ["1082", "python_vm_worker", "sistem", "%4.5", "85 MB"],
    ["1140", "desktop_renderer", "mert", "%3.1", "64 MB"],
    ["1205", "package_guard", "sistem", "%0.2", "18 MB"]
])

program.terminal_kutusu([
    "[09:41:00] Varyn Çekirdeği başlatıldı.",
    "[09:41:02] Tüm modüller ve güvenlik izinleri doğrulandı.",
    "[09:41:05] Sistem izleyici aktif ve dinlemede..."
])

program.durum_cubugu("4 Süreç Aktif", "CPU: 3.4 GHz | UTF-8", "tamam")

yazdir("Sistem yöneticisi programı aktif!")
`
  },
  {
    title: "Yığın, Kuyruk & Parantez Doğrulayıcı (kuyruk_yigin)",
    description: "%100 Saf Varyn ile yazılmış Yığın (Stack - LIFO) ve Kuyruk (Queue - FIFO) veri yapıları ve parantez dengesi denetimi.",
    code: `# Saf Varyn ile Veri Yapıları Testi
getir kuyruk_yigin

yazdir("=== 1. YIĞIN (STACK - LIFO) İŞLEMLERİ ===")
değişken y = kuyruk_yigin.yigin_olustur()
kuyruk_yigin.yigin_ekle(y, "Sayfa 1")
kuyruk_yigin.yigin_ekle(y, "Sayfa 2")
kuyruk_yigin.yigin_ekle(y, "Sayfa 3")

yazdir("Yığının Tepesindeki Eleman:", kuyruk_yigin.yigin_bak(y))
yazdir("Yığından Çıkarılan:", kuyruk_yigin.yigin_cikar(y))
yazdir("Yığının Yeni Tepesi:", kuyruk_yigin.yigin_bak(y))

yazdir("\\n=== 2. KUYRUK (QUEUE - FIFO) İŞLEMLERİ ===")
değişken k = kuyruk_yigin.kuyruk_olustur()
kuyruk_yigin.kuyruk_ekle(k, "Müşteri 1")
kuyruk_yigin.kuyruk_ekle(k, "Müşteri 2")
kuyruk_yigin.kuyruk_ekle(k, "Müşteri 3")

yazdir("Kuyruk Başındaki:", kuyruk_yigin.kuyruk_bak(k))
yazdir("Kuyruktan Hizmet Alan:", kuyruk_yigin.kuyruk_cikar(k))
yazdir("Kuyruktaki Yeni İlk Kişi:", kuyruk_yigin.kuyruk_bak(k))

yazdir("\\n=== 3. SÖZDİZİMİ PARANTEZ DENGESİ TESTİ ===")
değişken kod1 = "{[a + b] * (c - d)}"
değişken kod2 = "((a + b) * [c - d]"

yazdir(kod1, "-> Dengeli mi?:", kuyruk_yigin.parantez_dengeli_mi(kod1))
yazdir(kod2, "-> Dengeli mi?:", kuyruk_yigin.parantez_dengeli_mi(kod2))
`
  },
  {
    title: "Matris & Lineer Cebir Kütüphanesi (matris)",
    description: "%100 Saf Varyn ile matris oluşturma, toplama, çıkarma, çarpma, determinant ve transpoz hesaplamaları.",
    code: `# Saf Varyn ile Matris ve Lineer Cebir Testi
getir matris

yazdir("=== 1. MATRİS VE BİRİM MATRİS OLUŞTURMA ===")
değişken I = matris.birim_matris(3)
yazdir("3x3 Birim Matris:")
döngü satir içinde I:
    yazdir(" ", satir)

yazdir("\\n=== 2. MATRİS TOPLAMA VE ÇIKARMA ===")
değişken A = [[1, 2], [3, 4]]
değişken B = [[5, 6], [7, 8]]

değişken toplam = matris.matris_topla(A, B)
yazdir("A + B Toplamı:", toplam)

yazdir("\\n=== 3. MATRİS ÇARPIMI VE TRANSPOZ ===")
değişken carpim = matris.matris_carp(A, B)
yazdir("A * B Çarpımı:", carpim)

değişken At = matris.transpoz_al(A)
yazdir("A'nın Transpozu:", At)

yazdir("\\n=== 4. DETERMINANT VE İZ (TRACE) ===")
değişken det2 = matris.determinant_2x2(A)
yazdir("det(A):", det2)

değişken iz = matris.iz_hesapla(A)
yazdir("iz(A):", iz)
`
  },
  {
    title: "Sayı Teorisi & Özel Diziler (sayi_teorisi)",
    description: "%100 Saf Varyn ile Asal Çarpanlara Ayırma, Armstrong Sayıları, Collatz Dizisi ve Pascal Üçgeni.",
    code: `# Saf Varyn ile Sayı Teorisi Testi
getir sayi_teorisi

yazdir("=== 1. ASAL ÇARPANLARA AYIRMA ===")
değişken n = 1260
yazdir(n, "sayısının asal çarpanları:", sayi_teorisi.asal_carpanlar(n))

yazdir("\\n=== 2. ARMSTRONG VE MÜKEMMEL SAYILAR ===")
yazdir("153 bir Armstrong sayısı mı?:", sayi_teorisi.armstrong_mu(153))
yazdir("370 bir Armstrong sayısı mı?:", sayi_teorisi.armstrong_mu(370))
yazdir("28 bir Mükemmel Sayı mı?:", sayi_teorisi.mukemmel_sayi_mi(28))

yazdir("\\n=== 3. COLLATZ (3n + 1) DİZİSİ ===")
değişken collatz = sayi_teorisi.collatz_dizisi(13)
yazdir("13 için Collatz adımları (Uzunluk: " + metin(uzunluk(collatz)) + "):")
yazdir(collatz)

yazdir("\\n=== 4. PASCAL ÜÇGENİ ===")
değişken ucgen = sayi_teorisi.pascal_ucgeni(6)
döngü satir içinde ucgen:
    yazdir("  ", satir)
`
  },
  {
    title: "İkili Arama Ağacı ve Çizgeler (agac_graf)",
    description: "%100 Saf Varyn ile İkili Arama Ağacı (BST) ekleme, arama, sıralı gezinti ve Çizge (Graph) BFS araması.",
    code: `# Saf Varyn ile Ağaç ve Çizge Algoritmaları Testi
getir agac_graf

yazdir("=== 1. İKİLİ ARAMA AĞACI (BST) ===")
değişken kok = agac_graf.bst_dugum_olustur(50)
agac_graf.bst_ekle(kok, 30)
agac_graf.bst_ekle(kok, 70)
agac_graf.bst_ekle(kok, 20)
agac_graf.bst_ekle(kok, 40)
agac_graf.bst_ekle(kok, 60)
agac_graf.bst_ekle(kok, 80)

yazdir("Ağaçtaki Elemanların Sıralı Listesi (Inorder):", agac_graf.bst_sirali_dizi(kok))
yazdir("40 ağaçta var mı?:", agac_graf.bst_ara(kok, 40))
yazdir("99 ağaçta var mı?:", agac_graf.bst_ara(kok, 99))

yazdir("\\n=== 2. ÇİZGE (GRAPH) VE BFS GEZİNTİSİ ===")
değişken g = agac_graf.graf_olustur()
agac_graf.graf_kenar_ekle(g, "İstanbul", "Ankara")
agac_graf.graf_kenar_ekle(g, "İstanbul", "İzmir")
agac_graf.graf_kenar_ekle(g, "Ankara", "Konya")
agac_graf.graf_kenar_ekle(g, "İzmir", "Antalya")
agac_graf.graf_kenar_ekle(g, "Konya", "Antalya")

yazdir("İstanbul düğüm derecesi (bağlantı sayısı):", agac_graf.dugum_derecesi(g, "İstanbul"))
değişken bfs_yol = agac_graf.graf_bfs(g, "İstanbul")
yazdir("İstanbul merkezli BFS Gezinti Rotası:", bfs_yol)
`
  },
  {
    title: "İleri İstatistik & Veri Madenciliği (istatistik_pro)",
    description: "%100 Saf Varyn ile Varyans, Standart Sapma, Kartiller (Q1/Q3), Min-Max Normalizasyonu ve Korelasyon.",
    code: `# Saf Varyn ile İleri İstatistik Testi
getir istatistik_pro

değişken veriler = [12, 15, 18, 22, 25, 30, 35, 42, 50, 65]

yazdir("=== 1. TEMEL VE İLERİ İSTATİSTİKLER ===")
yazdir("Veri Kümesi:", veriler)
yazdir("Varyans:", istatistik_pro.varyans(veriler))
yazdir("Standart Sapma:", istatistik_pro.standart_sapma(veriler))

yazdir("\\n=== 2. ÇEYREKLER (KARTİLLER) VE AÇIKLIK ===")
değişken q = istatistik_pro.ceyrekler(veriler)
yazdir("Q1 (25. Yüzdelik):", q["q1"])
yazdir("Q2 (Medyan):", q["q2"])
yazdir("Q3 (75. Yüzdelik):", q["q3"])
yazdir("Çeyrekler Açıklığı (IQR):", istatistik_pro.ceyrekler_acikligi(veriler))

yazdir("\\n=== 3. MİN-MAX NORMALİZASYONU (0.0 - 1.0) ===")
değişken olcekli = istatistik_pro.min_max_olcekle(veriler)
yazdir("Ölçeklenmiş Veriler:", olcekli)

yazdir("\\n=== 4. PEARSON KORELASYON KATSAYISI ===")
değişken x = [1, 2, 3, 4, 5]
değişken y = [2, 4, 6, 8, 10]
yazdir("X ve Y Arasındaki Korelasyon:", istatistik_pro.pearson_korelasyon(x, y))
`
  },
  {
    title: "Metin Biçimlendirme & Levenshtein Mesafesi (metin_bicim)",
    description: "%100 Saf Varyn ile metin dolgulama, kelime frekansı analizi, palindrom testi ve Levenshtein benzerlik algoritması.",
    code: `# Saf Varyn ile Metin Biçimleme ve Analiz Testi
getir metin_bicim

yazdir("=== 1. METİN DOLGULAMA (PADDING) ===")
yazdir("Fatura No:", metin_bicim.metin_doldur_sol("458", 8, "0"))
yazdir("Hizalama :", metin_bicim.metin_doldur_sag("Varyn", 12, ".") + "|")

yazdir("\\n=== 2. KELİME FREKANSI ANALİZİ ===")
değişken metin_icerik = "varyn dili cok guzel ve varyn dili cok hizli calisir"
değişken frekans = metin_bicim.kelime_frekansi(metin_icerik)
yazdir("Metin:", metin_icerik)
yazdir("Kelime Sayımları:", frekans)

yazdir("\\n=== 3. TERS ÇEVİRME VE PALİNDROM ===")
yazdir("'ey edip adanada pide ye' palindrom mu?:", metin_bicim.palindrom_metin_mi("ey edip adanada pide ye"))

yazdir("\\n=== 4. LEVENSHTEIN DÜZENLEME MESAFESİ ===")
değişken s1 = "kitap"
değişken s2 = "katip"
yazdir("'" + s1 + "' ile '" + s2 + "' arasındaki düzenleme mesafesi:", metin_bicim.duzenleme_mesafesi(s1, s2))
`
  },
  {
    title: "Klasik Kriptoloji & Şifreleme (kripto_klasik)",
    description: "%100 Saf Varyn ile ROT13, Atbash, Vigenère ve Çit (Rail Fence) şifreleme ve çözme algoritmaları.",
    code: `# Saf Varyn ile Klasik Şifreleme Kütüphanesi Testi
getir kripto_klasik

değişken gizli_mesaj = "varynprogramlamadili"
değişken anahtar_soz = "anahtar"

yazdir("=== 1. ROT13 ŞİFRELEME ===")
değişken rot_sifreli = kripto_klasik.rot13(gizli_mesaj)
yazdir("Şifreli (ROT13):", rot_sifreli)
yazdir("Geri Çözüldü   :", kripto_klasik.rot13(rot_sifreli))

yazdir("\\n=== 2. ATBASH (ALFABE AYNASI) ŞİFRELEME ===")
değişken atbash_sifreli = kripto_klasik.atbash_sifrele("abcdef")
yazdir("Atbash Çıktısı:", atbash_sifreli)

yazdir("\\n=== 3. VIGENERE POLİALFABETİK ŞİFRELEME ===")
değişken vig_sifreli = kripto_klasik.vigenere_sifrele(gizli_mesaj, anahtar_soz)
değişken vig_cozum = kripto_klasik.vigenere_coz(vig_sifreli, anahtar_soz)
yazdir("Orijinal Metin:", gizli_mesaj)
yazdir("Şifrelenmiş   :", vig_sifreli)
yazdir("Çözülmüş Metin :", vig_cozum)

yazdir("\\n=== 4. ÇİT (RAIL FENCE) ŞİFRELEME ===")
değişken cit_sonuc = kripto_klasik.cit_sifrele("HELLOWORLD", 3)
yazdir("Çit Şifresi (3 Ray):", cit_sonuc)
`
  },
  {
    title: "Sıralama Algoritmaları Koleksiyonu (siralama_koleksiyonu)",
    description: "%100 Saf Varyn ile Kabarcık (Bubble), Seçmeli (Selection), Eklemeli (Insertion) ve Saymalı (Counting) sıralama.",
    code: `# Saf Varyn ile Sıralama Algoritmaları Karşılaştırma Testi
getir siralama_koleksiyonu

değişken ham_dizi = [64, 25, 12, 22, 11, 90, 33, 47]

yazdir("Ham Dizi:", ham_dizi)

yazdir("\\n=== 1. KABARCIK SIRALAMA (BUBBLE SORT) ===")
değişken s1 = siralama_koleksiyonu.kabarcik_sirala(ham_dizi)
yazdir("Sonuç:", s1, "| Sıralı mı?:", siralama_koleksiyonu.sirali_mi(s1))

yazdir("\\n=== 2. SEÇMELİ SIRALAMA (SELECTION SORT) ===")
değişken s2 = siralama_koleksiyonu.secmeli_sirala(ham_dizi)
yazdir("Sonuç:", s2, "| Sıralı mı?:", siralama_koleksiyonu.sirali_mi(s2))

yazdir("\\n=== 3. EKLEMELİ SIRALAMA (INSERTION SORT) ===")
değişken s3 = siralama_koleksiyonu.eklemeli_sirala(ham_dizi)
yazdir("Sonuç:", s3, "| Sıralı mı?:", siralama_koleksiyonu.sirali_mi(s3))

yazdir("\\n=== 4. SAYMALI SIRALAMA (COUNTING SORT) ===")
değişken sayi_dizisi = [4, 2, 2, 8, 3, 3, 1]
değişken s4 = siralama_koleksiyonu.saymali_sirala(sayi_dizisi, 8)
yazdir("Saymalı Sıralama:", s4)
`
  },
  {
    title: "2D/3D Vektör Matematiği ve Çarpışma Fiziği (vektor_fizik)",
    description: "%100 Saf Varyn ile Vektör Toplama, Nokta Çarpım, Vektör Büyüklüğü, Birim Vektör ve 2D Kutu (AABB) Çarpışması.",
    code: `# Saf Varyn ile Vektör Fiziği ve Çarpışma Testi
getir vektor_fizik

yazdir("=== 1. 2D VE 3D VEKTÖR VE BÜYÜKLÜK ===")
değişken v1 = vektor_fizik.vektor2d(3, 4)
değişken v2 = vektor_fizik.vektor2d(1, 2)

yazdir("v1 Büyüklüğü (Hipotenüs):", vektor_fizik.vektor_uzunluk(v1))
yazdir("v1 + v2 Toplamı:", vektor_fizik.vektor_topla(v1, v2))
yazdir("v1 . v2 Nokta Çarpımı:", vektor_fizik.nokta_carpim(v1, v2))

değişken birim_v1 = vektor_fizik.vektor_birim(v1)
yazdir("v1 Birim Vektörü:", birim_v1)

yazdir("\\n=== 2. 3D ÇAPRAZ ÇARPIM (CROSS PRODUCT) ===")
değişken a3 = vektor_fizik.vektor3d(1, 0, 0)
değişken b3 = vektor_fizik.vektor3d(0, 1, 0)
yazdir("a3 x b3 Çapraz Çarpımı:", vektor_fizik.capraz_carpim_3d(a3, b3))

yazdir("\\n=== 3. 2D AABB KUTU ÇARPIŞMA FİZİĞİ ===")
değişken oyuncu = {"x": 10, "y": 10, "genislik": 30, "yukseklik": 30}
değişken engel = {"x": 25, "y": 20, "genislik": 40, "yukseklik": 40}
değişken uzak_nesne = {"x": 100, "y": 100, "genislik": 20, "yukseklik": 20}

yazdir("Oyuncu - Engel Çarpışıyor mu?:", vektor_fizik.aabb_carpismasi_mi(oyuncu, engel))
yazdir("Oyuncu - Uzak Nesne Çarpışıyor mu?:", vektor_fizik.aabb_carpismasi_mi(oyuncu, uzak_nesne))
`
  },
  {
    title: "Mantık Bulmacaları & Zeka Algoritmaları (bulmaca_zeka)",
    description: "%100 Saf Varyn ile 4x4 Sudoku Doğrulayıcı, Hanoi Kuleleri Çözücü Adımları, Vezir Tehdit Kontrolü ve Anagram Testi.",
    code: `# Saf Varyn ile Bulmaca ve Zeka Oyunları Algoritmaları Testi
getir bulmaca_zeka

yazdir("=== 1. 4x4 SUDOKU DOĞRULAYICI ===")
değişken gecerli_sudoku = [
    [1, 2, 3, 4],
    [3, 4, 1, 2],
    [2, 1, 4, 3],
    [4, 3, 2, 1]
]
yazdir("Sudoku Çözümü Geçerli mi?:", bulmaca_zeka.sudoku_4x4_dogrula(gecerli_sudoku))

yazdir("\\n=== 2. HANOİ KULELERİ ÇÖZÜCÜ (3 DİSK) ===")
değişken hamleler = bulmaca_zeka.hanoi_hamleleri(3, "A", "C", "B")
yazdir("Toplam Hamle Sayısı:", uzunluk(hamleler))
döngü h içinde hamleler:
    yazdir("  ->", h)

yazdir("\\n=== 3. 4-VEZİR TEHDİT KONTROLÜ ===")
# [0, 2, 3, 1] sütun pozisyonları
değişken vezirler = [1, 3, 0, 2]
yazdir("Tahtadaki vezirler birbirini tehdit ediyor mu?:", bulmaca_zeka.vezir_tehditi_var_mi(vezirler))

yazdir("\\n=== 4. ANAGRAM KONTROLÜ ===")
yazdir("'karpuz' ve 'puzkar' anagram mı?:", bulmaca_zeka.anagram_mi("karpuz", "puzkar"))
yazdir("'varyn' ve 'python' anagram mı?:", bulmaca_zeka.anagram_mi("varyn", "python"))
`
  }
];
