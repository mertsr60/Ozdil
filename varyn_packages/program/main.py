# -*- coding: utf-8 -*-
"""
Varyn Masaüstü & Pencere Programı Geliştirme Kütüphanesi (program)
Bu kütüphane sayesinde ÖzDil / Varyn ile pencere tabanlı grafik programlar,
formlar, veri tabloları, menüler, araç çubukları ve etkileşimli yazılımlar geliştirilebilir.
"""

import plugin_api

def _append_element(elem):
    if plugin_api.plugin.current_program is not None:
        plugin_api.plugin.current_program["elements"].append(elem)
    else:
        # Program penceresi henüz açılmadıysa otomatik varsayılan pencere oluştur
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
    """Program penceresini ve tüm bileşenleri sıfırlar."""
    plugin_api.plugin.gui_elements.clear()
    plugin_api.plugin.current_program = None
    return True

def olustur(baslik="Varyn Programı", genislik=640, yukseklik=480, tema="koyu", ikon="uygulama"):
    """
    Yeni bir masaüstü pencere uygulaması başlatır.
    Örnek: program.olustur("Hesap Makinesi", 420, 520, "karanlik")
    """
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
    """
    Pencerenin en üstüne profesyonel masaüstü menü çubuğu ekler.
    Örnek: program.menu_cubugu(["Dosya", "Düzenle", "Görünüm", "Araçlar", "Yardım"])
    """
    if isinstance(menuler, str):
        menuler = [menuler]
    elem = {
        "type": "menu_cubugu",
        "items": [str(m) for m in menuler]
    }
    _append_element(elem)
    return True

def arac_cubugu(araclar):
    """
    Hızlı eylem araç çubuğu ekler.
    Örnek: program.arac_cubugu(["Yeni", "Kaydet", "Çalıştır", "Ayarlar"])
    """
    if isinstance(araclar, str):
        araclar = [araclar]
    elem = {
        "type": "arac_cubugu",
        "items": [str(a) for a in araclar]
    }
    _append_element(elem)
    return True

def sekme(sekmeler, aktif=0):
    """
    Çok sayfalı / görünümlü programlar için sekme grubu ekler.
    Örnek: program.sekme(["Genel Bakış", "Veri Listesi", "Ayarlar"], 0)
    """
    if isinstance(sekmeler, str):
        sekmeler = [sekmeler]
    elem = {
        "type": "sekme_grubu",
        "items": [str(s) for s in sekmeler],
        "active": int(aktif)
    }
    _append_element(elem)
    return True

def baslik(metin, alt_yazi="", seviye=1):
    """
    Program paneline başlık ve opsiyonel alt açıklama ekler.
    """
    elem = {
        "type": "program_baslik",
        "title": str(metin),
        "subtitle": str(alt_yazi) if alt_yazi else "",
        "level": int(seviye)
    }
    _append_element(elem)
    return True

def yazi(metin, stil="normal", hizalama="sol"):
    """
    Program içerisine biçimlendirilmiş metin ekler.
    Stiller: "normal", "vurgulu", "bilgi", "basarili", "uyari", "hata", "kod"
    """
    elem = {
        "type": "program_yazi",
        "text": str(metin),
        "style": str(stil),
        "align": str(hizalama)
    }
    _append_element(elem)
    return True

def metin_kutusu(etiket, varsayilan="", ipucu=""):
    """
    Kullanıcıdan metin girdisi almak için form giriş alanı ekler.
    """
    elem = {
        "type": "metin_kutusu",
        "label": str(etiket),
        "value": str(varsayilan),
        "placeholder": str(ipucu) if ipucu else f"{etiket} giriniz..."
    }
    _append_element(elem)
    return True

def sayi_kutusu(etiket, min_deger=0, max_deger=100, varsayilan=0):
    """
    Sayısal giriş kutusu ekler.
    """
    elem = {
        "type": "sayi_kutusu",
        "label": str(etiket),
        "min": float(min_deger),
        "max": float(max_deger),
        "value": float(varsayilan)
    }
    _append_element(elem)
    return True

def buton(yazi, eylem="", stil="birincil", ikon=""):
    """
    Etkileşimli masaüstü butonu ekler.
    Stiller: 'birincil' (mavi), 'basari' (yeşil), 'tehlike' (kırmızı), 'uyari' (turuncu), 'ikincil' (gri)
    """
    elem = {
        "type": "program_buton",
        "label": str(yazi),
        "action": str(eylem) if eylem else str(yazi),
        "style": str(stil),
        "icon": str(ikon) if ikon else ""
    }
    _append_element(elem)
    return True

def onay_kutusu(etiket, secili_mi=False):
    """
    Onay kutusu (Checkbox) ekler.
    """
    elem = {
        "type": "onay_kutusu",
        "label": str(etiket),
        "checked": bool(secili_mi)
    }
    _append_element(elem)
    return True

def secim_kutusu(etiket, secenekler=None, varsayilan=None):
    """
    Açılır seçim kutusu (Dropdown / Combobox) ekler.
    """
    if secenekler is None:
        secenekler = []
    elem = {
        "type": "secim_kutusu",
        "label": str(etiket),
        "options": [str(s) for s in secenekler],
        "selected": str(varsayilan) if varsayilan else (str(secenekler[0]) if secenekler else "")
    }
    _append_element(elem)
    return True

def kaydirici(etiket, min_deger=0, max_deger=100, deger=50):
    """
    Değer aralığı kaydırıcısı (Slider) ekler.
    """
    elem = {
        "type": "program_kaydirici",
        "label": str(etiket),
        "min": float(min_deger),
        "max": float(max_deger),
        "value": float(deger)
    }
    _append_element(elem)
    return True

def kart(baslik, icerik="", rozet="", ikon=""):
    """
    Şık bir bilgi veya istatistik kartı ekler.
    """
    elem = {
        "type": "program_kart",
        "title": str(baslik),
        "content": str(icerik),
        "badge": str(rozet) if rozet else "",
        "icon": str(ikon) if ikon else ""
    }
    _append_element(elem)
    return True

def tablo(kolonlar, satirlar):
    """
    Veri tablosu / grid bileşeni ekler.
    Örnek: program.tablo(["ID", "Ürün", "Fiyat"], [["1", "Laptop", "25.000 TL"], ["2", "Fare", "350 TL"]])
    """
    elem = {
        "type": "program_tablo",
        "headers": [str(k) for k in kolonlar],
        "rows": [[str(cell) for cell in row] for row in satirlar]
    }
    _append_element(elem)
    return True

def kod_kutusu(kod, dil="varyn"):
    """
    Program içinde kod düzenleme veya görüntüleme alanı ekler.
    """
    elem = {
        "type": "kod_kutusu",
        "code": str(kod),
        "lang": str(dil)
    }
    _append_element(elem)
    return True

def terminal_kutusu(ciktilar=None):
    """
    Program penceresi içerisine gömülü konsol / log paneli ekler.
    """
    if ciktilar is None:
        ciktilar = ["[Sistem] Uygulama çekirdeği başlatıldı.", "[Sistem] Hazır ve dinlemede..."]
    elif isinstance(ciktilar, str):
        ciktilar = [ciktilar]
    elem = {
        "type": "terminal_kutusu",
        "logs": [str(log) for log in ciktilar]
    }
    _append_element(elem)
    return True

def ilerleme(yuzde, durum=""):
    """
    Yüzdelik ilerleme çubuğu ekler.
    """
    elem = {
        "type": "program_ilerleme",
        "percent": max(0, min(100, float(yuzde))),
        "status": str(durum)
    }
    _append_element(elem)
    return True

def durum_cubugu(sol_mesaj="Hazır", sag_bilgi="v1.0.0 | UTF-8", durum="tamam"):
    """
    Pencerenin altına durum çubuğu ekler.
    """
    elem = {
        "type": "durum_cubugu",
        "left": str(sol_mesaj),
        "right": str(sag_bilgi),
        "status": str(durum)
    }
    _append_element(elem)
    return True

def bildirim(baslik, mesaj, tip="bilgi"):
    """
    Program içi bildirim bildirisi gösterir.
    Tipler: 'bilgi', 'basari', 'uyari', 'hata'
    """
    elem = {
        "type": "program_bildirim",
        "title": str(baslik),
        "message": str(mesaj),
        "alert_type": str(tip)
    }
    _append_element(elem)
    return True

def mesaj_kutusu(baslik, mesaj):
    """Açılır bilgi diyalog kutusu ekler."""
    return bildirim(baslik, mesaj, "bilgi")

def ornek_program(program_turu):
    """
    Kullanıcının tek satırda hazır masaüstü program şablonları çalıştırmasını sağlar.
    Türler: 'hesap_makinesi', 'not_defteri', 'gorev_yoneticisi', 'sistem_paneli', 'veri_tablosu'
    """
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
    """Program içi olay dinleyicisi kaydeder."""
    plugin_api.plugin.event_ekle(str(olay_adi), fonksiyon)
    return True

def olay_tetikle(olay_adi, veri=None):
    """Kayıtlı bir olayı program içinde tetikler."""
    plugin_api.plugin.trigger_event(str(olay_adi), veri)
    return True

def plugin():
    """Varyn plugin giriş noktası."""
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
