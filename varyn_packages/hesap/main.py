# Hesaplama ve Sunum Eklentisi
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
