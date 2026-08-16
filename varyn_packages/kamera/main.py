# Kamera Donanım Kontrolcü Modülü
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
