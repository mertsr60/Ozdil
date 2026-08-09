# Gelişmiş Finans ve Yatırım Eklentisi
import plugin_api

def faiz_hesapla(ana_para, oran, sure):
    try:
        ana_para = float(ana_para)
        oran = float(oran)
        sure = float(sure)
        if sure < 0 or ana_para < 0:
            return "Hata: Süre veya ana para negatif olamaz."
        toplam = ana_para * ((1 + (oran / 100)) ** sure)
        return round(toplam, 2)
    except Exception as e:
        return f"Hata: {str(e)}"

def doviz_cevir(tutar, kur):
    try:
        tutar = float(tutar)
        kur = float(kur)
        if tutar < 0 or kur < 0:
            return "Hata: Tutar veya kur negatif olamaz."
        return round(tutar * kur, 2)
    except Exception as e:
        return f"Hata: {str(e)}"

def enflasyon_etkisi(tutar, oran, yil):
    try:
        tutar = float(tutar)
        oran = float(oran)
        yil = float(yil)
        if yil < 0 or tutar < 0:
            return "Hata: Yıl veya tutar negatif olamaz."
        alim_gucu = tutar / ((1 + (oran / 100)) ** yil)
        return round(alim_gucu, 2)
    except Exception as e:
        return f"Hata: {str(e)}"

def kredi_taksit(tutar, oran, vade):
    try:
        tutar = float(tutar)
        yillik_oran = float(oran)
        vade = int(vade)
        if vade <= 0 or tutar < 0 or yillik_oran < 0:
            return "Hata: Vade, tutar ve oran pozitif olmalıdır."
        aylik_oran = (yillik_oran / 12) / 100
        if aylik_oran == 0:
            return round(tutar / vade, 2)
        faktor = (1 + aylik_oran) ** vade
        if (faktor - 1) == 0:
            return round(tutar / vade, 2)
        taksit = tutar * (aylik_oran * faktor) / (faktor - 1)
        return round(taksit, 2)
    except Exception as e:
        return f"Hata: {str(e)}"

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
