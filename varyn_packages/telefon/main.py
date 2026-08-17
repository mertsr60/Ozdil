# Mobil GUI Telefon Eklentisi
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
