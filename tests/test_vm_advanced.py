# -*- coding: utf-8 -*-
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from varyn_core.lexer import lex_varyn
from varyn_core.parser import Parser
from varyn_core.vm import VirtualMachine

class TestVMAdvanced(unittest.TestCase):
    def run_vm(self, code):
        tokens = lex_varyn(code)
        parser = Parser(tokens)
        ast_tree = parser.parse_program()
        vm = VirtualMachine()
        vm.eval(ast_tree, vm.global_env)
        return vm.stdout

    def test_recursive_fibonacci(self):
        code = (
            "islem fib(n):\n"
            "    eger n <= 1:\n"
            "        döndür n\n"
            "    döndür fib(n - 1) + fib(n - 2)\n"
            "yazdır(fib(6))\n"
        )
        outputs = self.run_vm(code)
        self.assertEqual(outputs, ["8\n"])

    def test_nested_loops(self):
        code = (
            "değişken toplam = 0\n"
            "değişken i = 1\n"
            "iken i <= 3:\n"
            "    değişken j = 1\n"
            "    iken j <= 3:\n"
            "        toplam = toplam + i * j\n"
            "        j = j + 1\n"
            "    i = i + 1\n"
            "yazdır(toplam)\n"
        )
        outputs = self.run_vm(code)
        self.assertEqual(outputs, ["36\n"])

    def test_class_inheritance_and_methods(self):
        code = (
            "sınıf Kopek:\n"
            "    islem ses_ver():\n"
            "        yazdır(\"Hav!\")\n"
            "\n"
            "değişken k = Kopek()\n"
            "k.ses_ver()\n"
        )
        outputs = self.run_vm(code)
        self.assertEqual(outputs, ["Hav!\n"])

    def test_native_exception_handling_matching(self):
        code = (
            "dene:\n"
            "    değişken sıfır = 0\n"
            "    değişken x = 10 / sıfır\n"
            "except SıfıraBölmeHatası as e:\n"
            "    yazdır(\"Sıfıra bölme yakalandı!\")\n"
        )
        outputs = self.run_vm(code)
        self.assertEqual(outputs, ["Sıfıra bölme yakalandı!\n"])

    def test_list_map_string_operators_and_methods(self):
        code = (
            "değişken lst = [1, 2]\n"
            "lst.ekle(3)\n"
            "yazdır(lst)\n"
            "yazdır(lst[0] + lst[2])\n"
            "\n"
            "değişken sozluk = {\"anahtar\": \"deger\"}\n"
            "yazdır(sozluk[\"anahtar\"])\n"
            "\n"
            "değişken metin = \"özdil\"\n"
            "yazdır(metin.büyük_harf())\n"
        )
        outputs = self.run_vm(code)
        self.assertEqual(outputs, ["[1, 2, 3]\n", "4\n", "deger\n", "ÖZDİL\n"])

    def test_unicode_nfd_normalization(self):
        import unicodedata
        # de-normalized turkish chars (NFD)
        nfd_code = unicodedata.normalize('NFD', "değişken x = \"test\"\nyazdır(x)\n")
        outputs = self.run_vm(nfd_code)
        self.assertEqual(outputs, ["test\n"])

    def test_path_traversal_prefix_bypass(self):
        from varyn_core.package_loader import validate_filepath_for_sandbox
        # Ensure that prefix-matching fails to access outer folders (e.g. varyn_secret)
        # Assuming project root is at /home/user/workspace
        import os
        from varyn_core.package_loader import _PROJECT_ROOT
        fake_traversal_path = os.path.abspath(_PROJECT_ROOT) + "_secret"
        with self.assertRaises(PermissionError):
            validate_filepath_for_sandbox(fake_traversal_path)

    def test_bool_none_printing(self):
        code = (
            "yazdır(doğru)\n"
            "yazdır(yanlış)\n"
            "yazdır(boş)\n"
        )
        outputs = self.run_vm(code)
        self.assertEqual(outputs, ["doğru\n", "yanlış\n", "boş\n"])

    def test_for_loop_and_break(self):
        code = (
            "değişken toplam = 0\n"
            "dongu x in aralık(1, 10):\n"
            "    eger x == 5:\n"
            "        dur\n"
            "    toplam = toplam + x\n"
            "yazdır(toplam)\n"
        )
        outputs = self.run_vm(code)
        self.assertEqual(outputs, ["10\n"])

    def test_multiple_except_clauses(self):
        code = (
            "islem test_hata(secim):\n"
            "    dene:\n"
            "        eger secim == 1:\n"
            "            değişken x = 1 / 0\n"
            "        eger secim == 2:\n"
            "            değişken lst = [1]\n"
            "            değişken y = lst[5]\n"
            "    except SıfıraBölmeHatası:\n"
            "        yazdır(\"sifir\")\n"
            "    except DizinHatası:\n"
            "        yazdır(\"dizin\")\n"
            "    except Hata:\n"
            "        yazdır(\"diger\")\n"
            "test_hata(1)\n"
            "test_hata(2)\n"
        )
        outputs = self.run_vm(code)
        self.assertEqual(outputs, ["sifir\n", "dizin\n"])

    def test_nested_reentrant_vm_call(self):
        from varyn_core.runtime_types import wrap_value
        tokens = lex_varyn("islem carp(a, b):\n    döndür a * b\n")
        parser = Parser(tokens)
        ast_tree = parser.parse_program()
        vm = VirtualMachine()
        vm.eval(ast_tree, vm.global_env)
        
        carp_fn = vm.global_env.lookup("carp", 1)
        native_carp = carp_fn.to_native()
        
        def callback(x):
            return native_carp(x, 10)
            
        vm.global_env.define("islem_yap", wrap_value(callback))
        
        tokens_call = lex_varyn("yazdır(islem_yap(7))\n")
        parser_call = Parser(tokens_call)
        ast_call = parser_call.parse_program()
        vm.eval(ast_call, vm.global_env)
        self.assertEqual(vm.stdout, ["70\n"])

    def test_multiline_implicit_continuation(self):
        code = (
            "değişken veri_noktalari = [\n"
            "    [1.0, 1.0], [1.5, 1.2],\n"
            "    [5.0, 5.0]\n"
            "]\n"
            "yazdır(veri_noktalari[1][0])\n"
        )
        outputs = self.run_vm(code)
        self.assertEqual(outputs, ["1.5\n"])

if __name__ == "__main__":
    unittest.main()
