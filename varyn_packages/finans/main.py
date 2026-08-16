# Gelişmiş Finans ve Yatırım Eklentisi
import plugin_api

def faiz_hesapla(ana_para, oran, sure):
    ana_para = float(ana_para)
    oran = float(oran)
    sure = float(sure)
    toplam = ana_para * ((1 + (oran / 100)) ** sure)
    return round(toplam, 2)

def doviz_cevir(tutar, kur):
    tutar = float(tutar)
    kur = float(kur)
    return round(tutar * kur, 2)

def enflasyon_etkisi(tutar, oran, yil):
    tutar = float(tutar)
    oran = float(oran)
    yil = float(yil)
    alim_gucu = tutar / ((1 + (oran / 100)) ** yil)
    return round(alim_gucu, 2)

def kredi_taksit(tutar, oran, vade):
    tutar = float(tutar)
    yillik_oran = float(oran)
    vade = int(vade)
    aylik_oran = (yillik_oran / 12) / 100
    if aylik_oran == 0:
        return round(tutar / vade, 2)
    faktor = (1 + aylik_oran) ** vade
    taksit = tutar * (aylik_oran * faktor) / (faktor - 1)
    return round(taksit, 2)

def plugin():
    plugin_api.plugin.fonksiyon_ekle("faiz_hesapla", faiz_hesapla)
    plugin_api.plugin.fonksiyon_ekle("doviz_cevir", doviz_cevir)
    plugin_api.plugin.fonksiyon_ekle("enflasyon_etkisi", enflasyon_etkisi)
    plugin_api.plugin.fonksiyon_ekle("kredi_taksit", kredi_taksit)
    return {
        "faiz_hesapla": faiz_hesapla,
        "doviz_cevir": doviz_cevir,
        "enflasyon_etkisi": enflasyon_etkisi,
        "kredi_taksit": kredi_taksit
    }
