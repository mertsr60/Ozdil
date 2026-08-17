# -*- coding: utf-8 -*-
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from compiler import run_code

class TestYeniKutuphaneler(unittest.TestCase):
    """
    Eklenen 10 Yeni Kütüphaneye Özel Birim ve Entegrasyon Testleri
    """

    def test_01_veritabani(self):
        code = (
            'getir veritabani\n'
            'veritabani.veritabani_baglan("test_db")\n'
            'veritabani.veritabani_koy("kullanici", "ahmet", "test_db")\n'
            'değişken val = veritabani.veritabani_al("kullanici", "yok", "test_db")\n'
            'yazdır(val)\n'
            'değişken hepsi = veritabani.veritabani_tumunu_getir("test_db")\n'
            'yazdır(hepsi["kullanici"])\n'
            'veritabani.veritabani_sil("kullanici", "test_db")\n'
            'yazdır(veritabani.veritabani_al("kullanici", "silindi", "test_db"))\n'
        )
        res = run_code(code)
        self.assertIsNone(res.get("error"), f"veritabani hatası: {res.get('error')}")
        output = res.get("output", "").strip().splitlines()
        self.assertEqual(output, ["ahmet", "ahmet", "silindi"])

    def test_02_ag_istemci(self):
        code = (
            'getir ag_istemci\n'
            'değişken json_metin = "{\\"durum\\": \\"aktif\\", \\"kod\\": 200}"\n'
            'değişken obj = ag_istemci.ag_json_coz(json_metin)\n'
            'yazdır(obj["durum"])\n'
            'yazdır(obj["kod"])\n'
        )
        res = run_code(code)
        self.assertIsNone(res.get("error"), f"ag_istemci hatası: {res.get('error')}")
        output = res.get("output", "").strip().splitlines()
        self.assertEqual(output, ["aktif", "200"])

    def test_03_sifreleme_araclari(self):
        code = (
            'getir sifreleme_araclari\n'
            'değişken sha = sifreleme_araclari.sha256_hesapla("varyn")\n'
            'değişken md5 = sifreleme_araclari.md5_hesapla("varyn")\n'
            'değişken b64 = sifreleme_araclari.base64_kodla("ozdil")\n'
            'değişken b64_coz = sifreleme_araclari.base64_coz(b64)\n'
            'değişken sezar = sifreleme_araclari.sezar_sifrele("abc", 3)\n'
            'değişken sezar_coz = sifreleme_araclari.sezar_coz(sezar, 3)\n'
            'yazdır(b64_coz)\n'
            'yazdır(sezar)\n'
            'yazdır(sezar_coz)\n'
        )
        res = run_code(code)
        self.assertIsNone(res.get("error"), f"sifreleme_araclari hatası: {res.get('error')}")
        output = res.get("output", "").strip().splitlines()
        self.assertEqual(output, ["ozdil", "def", "abc"])

    def test_04_ses_muzik(self):
        code = (
            'getir ses_muzik\n'
            'değişken f = ses_muzik.nota_frekansi("LA")\n'
            'değişken oktav = ses_muzik.oktav_hesapla(f, 1)\n'
            'değişken bpm_saniye = ses_muzik.bpm_vurus_suresi(120)\n'
            'değişken ornekler = ses_muzik.sinus_dalgasi_ornekle(440, 1, 8000)\n'
            'yazdır(f)\n'
            'yazdır(oktav)\n'
            'yazdır(bpm_saniye)\n'
            'yazdır(uzunluk(ornekler))\n'
        )
        res = run_code(code)
        self.assertIsNone(res.get("error"), f"ses_muzik hatası: {res.get('error')}")
        output = res.get("output", "").strip().splitlines()
        self.assertEqual(output, ["440.0", "880.0", "0.5", "1000"])

    def test_05_muhasebe(self):
        code = (
            'getir muhasebe\n'
            'değişken kdv = muhasebe.kdv_hesapla(100, 20)\n'
            'değişken maas = muhasebe.brutten_nete_maas(50000)\n'
            'değişken zam = muhasebe.zam_hesapla(10000, 10)\n'
            'yazdır(kdv["toplam_tutar"])\n'
            'yazdır(zam["yeni_tutar"])\n'
        )
        res = run_code(code)
        self.assertIsNone(res.get("error"), f"muhasebe hatası: {res.get('error')}")
        output = res.get("output", "").strip().splitlines()
        self.assertEqual(output, ["120.0", "11000.0"])

    def test_06_fizik(self):
        code = (
            'getir fizik\n'
            'değişken ke = fizik.kinetik_enerji(10, 5)\n'
            'değişken pe = fizik.potansiyel_enerji(10, 5)\n'
            'değişken dusme = fizik.serbest_dusme(2)\n'
            'yazdır(ke)\n'
            'yazdır(pe)\n'
            'yazdır(dusme["hiz"])\n'
        )
        res = run_code(code)
        self.assertIsNone(res.get("error"), f"fizik hatası: {res.get('error')}")
        output = res.get("output", "").strip().splitlines()
        self.assertEqual(output, ["125.0", "490.33", "19.61"])

    def test_07_geometri(self):
        code = (
            'getir geometri\n'
            'değişken u_alan = geometri.ucgen_alani(10, 6)\n'
            'değişken d_alan = geometri.daire_alani(10)\n'
            'değişken hip = geometri.hipotenus(3, 4)\n'
            'değişken kure = geometri.kure_hacmi(3)\n'
            'yazdır(u_alan)\n'
            'yazdır(hip)\n'
            'yazdır(d_alan)\n'
            'yazdır(kure)\n'
        )
        res = run_code(code)
        self.assertIsNone(res.get("error"), f"geometri hatası: {res.get('error')}")
        output = res.get("output", "").strip().splitlines()
        self.assertEqual(output, ["30.0", "5.0", "314.16", "113.1"])

    def test_08_otomasyon(self):
        code = (
            'getir otomasyon\n'
            'otomasyon.gunluk_temizle()\n'
            'otomasyon.gunluk_ekle("Sistem Baslatildi", "BILGI")\n'
            'değişken d = otomasyon.gunluk_dokum()\n'
            'değişken sure = otomasyon.zamanlayici_suresi(3665)\n'
            'yazdır(uzunluk(d))\n'
            'yazdır(sure)\n'
        )
        res = run_code(code)
        self.assertIsNone(res.get("error"), f"otomasyon hatası: {res.get('error')}")
        output = res.get("output", "").strip().splitlines()
        self.assertEqual(output, ["1", "01:01:05"])

    def test_09_lokasyon(self):
        code = (
            'getir lokasyon\n'
            'değişken ank = lokasyon.sehir_koordinati("ANKARA")\n'
            'değişken mesafe = lokasyon.sehirler_arasi_mesafe("ANKARA", "ISTANBUL")\n'
            'yazdır(ank[0])\n'
            'yazdır(mesafe > 300.0)\n'
        )
        res = run_code(code)
        self.assertIsNone(res.get("error"), f"lokasyon hatası: {res.get('error')}")
        output = res.get("output", "").strip().splitlines()
        self.assertEqual(output, ["39.9334", "doğru"])

    def test_10_donusturucu(self):
        code = (
            'getir donusturucu\n'
            'değişken c2f = donusturucu.celcius_fahrenheit(0)\n'
            'değişken f2c = donusturucu.fahrenheit_celcius(32)\n'
            'değişken km2mil = donusturucu.km_mil(100)\n'
            'değişken mb = donusturucu.bayt_donustur(1048576, "MB")\n'
            'yazdır(c2f)\n'
            'yazdır(f2c)\n'
            'yazdır(km2mil)\n'
            'yazdır(mb)\n'
        )
        res = run_code(code)
        self.assertIsNone(res.get("error"), f"donusturucu hatası: {res.get('error')}")
        output = res.get("output", "").strip().splitlines()
        self.assertEqual(output, ["32.0", "0.0", "62.14", "1.0"])

if __name__ == "__main__":
    unittest.main()
