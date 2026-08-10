# Yapay Zeka Kütüphanesi - 100% ÖzDil ile yazılmış gelişmiş paket!

işlem ortalama(dizi):
    değişken n = uzunluk(dizi)
    eğer n == 0:
        döndür 0
    değişken t = 0
    döngü eleman içinde dizi:
        t = t + eleman
    döndür t / n

işlem uzaklik_hesapla(p1, p2):
    # İki nokta arasındaki Öklid uzaklığı
    değişken fark_x = p1[0] - p2[0]
    değişken fark_y = p1[1] - p2[1]
    değişken toplam_kare = (fark_x * fark_x) + (fark_y * fark_y)
    döndür karekok(toplam_kare)

işlem dogrusal_regresyon_egit(x_listesi, y_listesi):
    değişken n = uzunluk(x_listesi)
    eğer n == 0:
        döndür {"hata": "Veri listeleri boş olamaz."}
    eğer n != uzunluk(y_listesi):
        döndür {"hata": "X ve Y listeleri eşit uzunlukta olmalıdır."}
    
    değişken ort_x = ortalama(x_listesi)
    değişken ort_y = ortalama(y_listesi)
    
    değişken pay = 0
    değişken payda = 0
    
    döngü i içinde aralık(n):
        değişken dx = x_listesi[i] - ort_x
        değişken dy = y_listesi[i] - ort_y
        pay = pay + (dx * dy)
        payda = payda + (dx * dx)
        
    eğer payda == 0:
        değişken egim = 0
    değilse:
        değişken egim = pay / payda
        
    değişken kesim = ort_y - (egim * ort_x)
    
    döndür {"egim": egim, "kesim_noktasi": kesim}

işlem dogrusal_regresyon_tahmin_et(model, x):
    değişken egim = model["egim"]
    değişken kesim = model["kesim_noktasi"]
    döndür (egim * x) + kesim

işlem k_ortalama_kumele(veri_noktalari, k, iterasyon_sayisi):
    değişken n = uzunluk(veri_noktalari)
    eğer n < k:
        döndür {"hata": "Veri noktası sayısı küme sayısından az olamaz."}
        
    # Merkezleri ilk k nokta olarak başlat
    değişken merkezler = []
    döngü i içinde aralık(k):
        merkezler.ekle(veri_noktalari[i])
        
    değişken kumeler = []
    
    döngü iter içinde aralık(iterasyon_sayisi):
        # Kümeleri sıfırla
        kumeler = []
        döngü i içinde aralık(k):
            kumeler.ekle([])
            
        # Her noktayı en yakın merkeze ata
        döngü nokta içinde veri_noktalari:
            değişken en_kucuk_uzaklik = 999999
            değişken en_yakin_kume_indeksi = 0
            döngü i içinde aralık(k):
                değişken uz = uzaklik_hesapla(nokta, merkezler[i])
                eğer uz < en_kucuk_uzaklik:
                    en_kucuk_uzaklik = uz
                    en_yakin_kume_indeksi = i
            kumeler[en_yakin_kume_indeksi].ekle(nokta)
            
        # Yeni merkezleri hesapla (kümelerin ortalaması)
        döngü i içinde aralık(k):
            değişken kume = kumeler[i]
            değişken kume_uzunluk = uzunluk(kume)
            eğer kume_uzunluk > 0:
                değişken toplam_x = 0
                değişken toplam_y = 0
                döngü p içinde kume:
                    toplam_x = toplam_x + p[0]
                    toplam_y = toplam_y + p[1]
                merkezler[i] = [toplam_x / kume_uzunluk, toplam_y / kume_uzunluk]
                
    döndür {"merkezler": merkezler, "kumeler": kumeler}

işlem knn_siniflandir(egitim_verisi, test_noktasi, k_degeri):
    değişken n = uzunluk(egitim_verisi)
    değişken mesafeler = []
    
    döngü i içinde aralık(n):
        değişken nokta = egitim_verisi[i][0]
        değişken sinif_adi = egitim_verisi[i][1]
        değişken d = uzaklik_hesapla(nokta, test_noktasi)
        mesafeler.ekle([d, sinif_adi])
        
    # Bubble sort ile mesafeleri sırala
    döngü i içinde aralık(n):
        değişken sinir = n - i - 1
        döngü j içinde aralık(sinir):
            eğer mesafeler[j][0] > mesafeler[j + 1][0]:
                değişken gecici = mesafeler[j]
                mesafeler[j] = mesafeler[j + 1]
                mesafeler[j + 1] = gecici
                
    değişken en_yakin_siniflar = []
    döngü i içinde aralık(k_degeri):
        en_yakin_siniflar.ekle(mesafeler[i][1])
        
    # En sık geçeni bul
    değişken en_cok_gecen = en_yakin_siniflar[0]
    değişken en_yuksek_sayi = 0
    
    değişken benzersiz_siniflar = []
    döngü s içinde en_yakin_siniflar:
        değişken var_mi = yanlış
        döngü bs içinde benzersiz_siniflar:
            eğer bs == s:
                var_mi = doğru
        eğer değil var_mi:
            benzersiz_siniflar.ekle(s)
            
    döngü bs içinde benzersiz_siniflar:
        değişken sayac = 0
        döngü s içinde en_yakin_siniflar:
            eğer s == bs:
                sayac = sayac + 1
        eğer sayac > en_yuksek_sayi:
            en_yuksek_sayi = sayac
            en_cok_gecen = bs
            
    döndür en_cok_gecen

işlem relu(x):
    eğer x > 0:
        döndür x
    değilse:
        döndür 0

işlem yapay_sinir_hucresi(girdiler, agirliklar, sapma, aktivasyon):
    değişken n = uzunluk(girdiler)
    değişken toplam = 0
    döngü i içinde aralık(n):
        toplam = toplam + (girdiler[i] * agirliklar[i])
    toplam = toplam + sapma
    
    eğer aktivasyon == "relu":
        döndür relu(toplam)
    değilse_eğer aktivasyon == "adim":
        eğer toplam >= 0:
            döndür 1
        değilse:
            döndür 0
    değilse:
        döndür toplam
