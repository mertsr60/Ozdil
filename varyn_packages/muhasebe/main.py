# Finansal Muhasebe ve Vergi Hesaplama Kütüphanesi

def kdv_hesapla(tutar, oran=20):
    kdv_tutari = (float(tutar) * float(oran)) / 100.0
    toplam = float(tutar) + kdv_tutari
    return {
        "ham_tutar": float(tutar),
        "kdv_orani": float(oran),
        "kdv_tutari": round(kdv_tutari, 2),
        "toplam_tutar": round(toplam, 2)
    }

def brutten_nete_maas(brut_maas, sgk_orani=14, issizlik_orani=1, gelir_vergisi_orani=15):
    brut = float(brut_maas)
    sgk = (brut * sgk_orani) / 100.0
    issizlik = (brut * issizlik_orani) / 100.0
    matrah = brut - (sgk + issizlik)
    gelir_vergisi = (matrah * gelir_vergisi_orani) / 100.0
    damga_vergisi = (brut * 0.759) / 100.0
    kesintiler_toplami = sgk + issizlik + gelir_vergisi + damga_vergisi
    net_maas = brut - kesintiler_toplami
    return {
        "brut_maas": round(brut, 2),
        "kesintiler_toplami": round(kesintiler_toplami, 2),
        "net_maas": round(net_maas, 2)
    }

def zam_hesapla(mevcut_tutar, zam_orani):
    arti = (float(mevcut_tutar) * float(zam_orani)) / 100.0
    yeni_tutar = float(mevcut_tutar) + arti
    return {
        "eski_tutar": float(mevcut_tutar),
        "zam_miktari": round(arti, 2),
        "yeni_tutar": round(yeni_tutar, 2)
    }

def plugin():
    return {
        "kdv_hesapla": kdv_hesapla,
        "brutten_nete_maas": brutten_nete_maas,
        "zam_hesapla": zam_hesapla
    }
