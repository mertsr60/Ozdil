# -*- coding: utf-8 -*-
import unittest
import os
import sys

# Ensure root directory in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from compiler import run_code
from varyn_core.capabilities import Capability, ResourceLimits
from varyn_core.errors import VarynError
from varyn_core.vm import VirtualMachine
from varyn_core.runtime_types import (
    OzString, OzList, OzMap, OzInstance, OzClass, wrap_value
)
from varyn_core.object_model import is_dangerous_attribute, get_attribute

class TestAdversarialSecurity(unittest.TestCase):
    """
    Kapsamlı Güvenlik ve Karşıt (Adversarial) Test Paketi:
    - Host/Python Kaçış (Escape) Vektörleri
    - Nesne / Yansıma (Reflection & Introspection) Engelleme
    - Dosya Sistemi Sandbox & Yol Aşımı (Path Traversal)
    - SSRF & Ağ Güvenliği
    - Kaynak Tükenmesi / DoS (Hafıza, Sonsuz Döngü, Rekürsiyon)
    - Ortam Değişkenleri & Host Gizliliği
    - Normal ÖzDil İşlevselliğinin Korunması (Regresyon)
    """

    # -------------------------------------------------------------
    # 1. PYTHON / HOST ESCAPE & REFLECTION TESTS
    # -------------------------------------------------------------
    def test_escape_via_dunder_class_on_string(self):
        """Metin nesnesi üzerinden __class__.__bases__[0].__subclasses__() kaçış denemesi engellenmelidir."""
        code = """
s = "test"
x = s.__class__
"""
        res = run_code(code)
        self.assertIsNotNone(res["error"])
        self.assertTrue("Öznitelik" in res["error"] or "Güvenlik" in res["error"] or "AttributeError" in res["error"])

    def test_escape_via_dunder_globals_on_function(self):
        """Fonksiyon nesneleri üzerinden __globals__ erişimi engellenmelidir."""
        code = """
islem gizli():
    dondur 42

g = gizli.__globals__
"""
        res = run_code(code)
        self.assertIsNotNone(res["error"])
        self.assertTrue("Öznitelik" in res["error"] or "Güvenlik" in res["error"])

    def test_escape_via_dunder_subclasses_on_instance(self):
        """Sınıf örneği üzerinden __subclasses__ ve __bases__ çağrısı engellenmelidir."""
        code = """
sinif Saldirgan:
    islem baslat():
        dondur 1

a = Saldirgan()
sub = a.__class__.__subclasses__()
"""
        res = run_code(code)
        self.assertIsNotNone(res["error"])

    def test_escape_via_attribute_assignment_to_native(self):
        """Dahili veya yerel Python nesnelerinin özniteliklerinin ezilmeye çalışılması engellenmelidir."""
        code = """
s = "merhaba"
s.__class__ = 123
"""
        res = run_code(code)
        self.assertIsNotNone(res["error"])

    def test_escape_via_dangerous_attributes_blocklist(self):
        """is_dangerous_attribute fonksiyonunun bilinen tüm tehlikeli dunder ve frame alanlarını engellediği doğrulanmalıdır."""
        dangerous_names = [
            "__class__", "__bases__", "__subclasses__", "__mro__", "__globals__",
            "__code__", "__dict__", "__closure__", "__func__", "__self__",
            "__module__", "__builtins__", "__import__", "gi_frame", "f_globals",
            "f_locals", "cr_frame", "ag_frame", "__del__", "__reduce__"
        ]
        for name in dangerous_names:
            self.assertTrue(is_dangerous_attribute(name), f"Tehlikeli öznitelik engellenmedi: {name}")

    def test_escape_via_wrapper_to_native_isolation(self):
        """to_native() fonksiyonunun güvenli yerel tiplere indirgediği ve sızıntı yapmadığı doğrulanmalıdır."""
        s = OzString("test")
        self.assertEqual(s.to_native(), "test")
        
        # OzString'den __dict__ veya __globals__ erişiminin AttributeError fırlattığı
        with self.assertRaises(Exception):
            s.get_attr("__globals__")
            
        l = OzList([1, 2, 3])
        with self.assertRaises(Exception):
            l.get_attr("__class__")

    # -------------------------------------------------------------
    # 2. FILESYSTEM & PATH TRAVERSAL SANDBOX TESTS
    # -------------------------------------------------------------
    def test_filesystem_default_no_capability(self):
        """Varsayılan olarak 'dosya_sistemi' yetkisi yokken dosya modülü kullanımı engellenmelidir."""
        code = """
getir dosya
icerik = dosya.oku("test.txt")
"""
        res = run_code(code)
        self.assertIsNotNone(res["error"])
        self.assertTrue("Yetki" in res["error"] or "PermissionError" in res["error"] or "dosya_sistemi" in res["error"])

    def test_filesystem_path_traversal_blocking(self):
        """'dosya_sistemi' yetkisi verilse dahi proje kök dizini dışına çıkış (../ traversal) engellenmelidir."""
        code = """
getir dosya
icerik = dosya.oku("../../../etc/passwd")
"""
        res = run_code(code, capabilities=[Capability.FILESYSTEM])
        self.assertIsNotNone(res["error"])
        self.assertTrue("engellenmiştir" in res["error"] or "Hata" in res["error"])

    def test_filesystem_sensitive_files_blocking(self):
        """Hassas yapılandırma dosyalarına (.env, package.json, server.ts) erişim engellenmelidir."""
        code = """
getir dosya
icerik = dosya.oku(".env")
"""
        res = run_code(code, capabilities=[Capability.FILESYSTEM])
        self.assertIsNotNone(res["error"])
        self.assertTrue("Hassas" in res["error"] or "engellenmiştir" in res["error"])

    def test_filesystem_null_byte_injection(self):
        """Null byte (\0) içeren dosya yolları tespit edilip engellenmelidir."""
        code = """
getir dosya
icerik = dosya.oku("guvenli.txt\\0/etc/passwd")
"""
        res = run_code(code, capabilities=[Capability.FILESYSTEM])
        self.assertIsNotNone(res["error"])
        self.assertTrue("Güvenlik İhlali" in res["error"] or "geçersiz karakter" in res["error"])

    # -------------------------------------------------------------
    # 3. NETWORK & SSRF SANDBOX TESTS
    # -------------------------------------------------------------
    def test_network_default_no_capability(self):
        """Varsayılan olarak 'ag' yetkisi yokken web modülü kullanımı engellenmelidir."""
        code = """
getir web
sonuc = web.getir("https://example.com")
"""
        res = run_code(code)
        self.assertIsNotNone(res["error"])
        self.assertTrue("Yetki" in res["error"] or "PermissionError" in res["error"] or "ag" in res["error"])

    def test_network_ssrf_localhost_blocking(self):
        """'ag' yetkisi olsa dahi localhost / 127.0.0.1 / dahili bulut adresleri engellenmelidir."""
        code = """
getir web
sonuc = web.getir("http://127.0.0.1:8080/admin")
"""
        res = run_code(code, capabilities=[Capability.NETWORK])
        self.assertIsNotNone(res["error"])
        self.assertTrue("engellendi" in res["error"] or "SSRF" in res["error"] or "Güvenlik" in res["error"])

    def test_network_ssrf_metadata_blocking(self):
        """Bulut metadata IP adresine (169.254.169.254) erişim engellenmelidir."""
        code = """
getir web
sonuc = web.getir("http://169.254.169.254/latest/meta-data/")
"""
        res = run_code(code, capabilities=[Capability.NETWORK])
        self.assertIsNotNone(res["error"])
        self.assertTrue("engellendi" in res["error"] or "SSRF" in res["error"])

    # -------------------------------------------------------------
    # 4. RESOURCE EXHAUSTION & DoS (DENIAL OF SERVICE) TESTS
    # -------------------------------------------------------------
    def test_dos_infinite_loop_instruction_limit(self):
        """Sonsuz döngüler maksimum işlem adımı sınırına (max_instructions) ulaştığında durdurulmalıdır."""
        code = """
sayac = 0
iken doğru:
    sayac = sayac + 1
"""
        # 5000 instruction limit ile test edelim
        limits = ResourceLimits(max_instructions=5000, max_execution_time_sec=2.0)
        res = run_code(code, limits=limits)
        self.assertIsNotNone(res["error"])
        self.assertTrue("Kaynak Aşımı" in res["error"] or "Maksimum işlem adımı" in res["error"])

    def test_dos_deep_recursion_call_depth(self):
        """Aşırı derin özyineleme (recursion) çağrı derinliği sınırını aşınca yakalanmalıdır."""
        code = """
islem sonsuz_cagri(n):
    dondur sonsuz_cagri(n + 1)

sonsuz_cagri(1)
"""
        limits = ResourceLimits(max_call_depth=50)
        res = run_code(code, limits=limits)
        self.assertIsNotNone(res["error"])
        self.assertTrue("Özyineleme Hatası" in res["error"] or "Maksimum çağrı derinliği" in res["error"])

    def test_dos_memory_exhaustion_string_multiplication(self):
        """Büyük metin çoğaltma saldırısı bellek sınırı kontrolü ile engellenmelidir."""
        code = """
bomba = "A" * 20000000
"""
        res = run_code(code)
        self.assertIsNotNone(res["error"])
        self.assertTrue("Kaynak Aşımı" in res["error"] or "Maksimum metin boyutu" in res["error"])

    def test_dos_memory_exhaustion_list_range(self):
        """Devasa liste veya aralık oluşturma saldırısı engellenmelidir."""
        code = """
dizi = aralık(10000000)
"""
        res = run_code(code)
        self.assertIsNotNone(res["error"])
        self.assertTrue("Kaynak Aşımı" in res["error"] or "Maksimum" in res["error"])

    # -------------------------------------------------------------
    # 5. ENVIRONMENT & HOST PRIVACY
    # -------------------------------------------------------------
    def test_environment_variables_host_isolation(self):
        """Host işletim sistemi ortam değişkenleri (os.environ) misafir ÖzDil koduna sızmamalıdır."""
        code = """
getir sistem
yazdır(sistem.çevre)
"""
        res = run_code(code)
        self.assertIsNone(res["error"])
        # Host environment keys should NOT be exposed
        output = res["output"]
        self.assertNotIn("PATH", output)
        self.assertNotIn("HOME", output)
        self.assertNotIn("GEMINI_API_KEY", output)

    # -------------------------------------------------------------
    # 6. NORMAL FUNCTIONALITY & REGRESSION TESTS
    # -------------------------------------------------------------
    def test_normal_math_and_logic(self):
        """Normal matematiksel işlemler ve mantıksal akış sorunsuz çalışmalıdır."""
        code = """
a = 15
b = 25
toplam = a + b
yazdır(toplam)
"""
        res = run_code(code)
        self.assertIsNone(res["error"])
        self.assertIn("40", res["output"])

    def test_normal_string_and_list_operations(self):
        """Metin ve liste fonksiyonları, döngüler ve koşullar standart şekilde çalışmalıdır."""
        code = """
meyveler = ["elma", "armut", "muz"]
meyveler.ekle("çilek")
yazdır(meyveler.uzunluk())
yazdır(meyveler[0])
"""
        res = run_code(code)
        self.assertIsNone(res["error"])
        self.assertIn("4", res["output"])
        self.assertIn("elma", res["output"])

    def test_normal_classes_and_oop(self):
        """ÖzDil nesne yönelimli programlama (OOP), sınıflar ve metotlar sorunsuz çalışmalıdır."""
        code = """
sinif Araba:
    islem __init__(self, marka, hiz):
        self.marka = marka
        self.hiz = hiz
        
    islem hizlan(self, miktar):
        self.hiz = self.hiz + miktar
        dondur self.hiz

oto = Araba("Anadol", 50)
yazdır(oto.hizlan(20))
"""
        res = run_code(code)
        self.assertIsNone(res["error"])
        self.assertIn("70", res["output"])

    def test_normal_exception_handling(self):
        """Dene/Yakala blokları beklenen hataları yakalayabilmelidir."""
        code = """
sonuc = "varsayilan"
dene:
    x = 10 / 0
yakala SıfıraBölmeHatası:
    sonuc = "yakalandi"
yazdır(sonuc)
"""
        res = run_code(code)
        self.assertIsNone(res["error"])
        self.assertIn("yakalandi", res["output"])

if __name__ == '__main__':
    unittest.main()
