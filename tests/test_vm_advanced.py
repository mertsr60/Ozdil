# -*- coding: utf-8 -*-
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ozdil_core.lexer import lex_ozdil
from ozdil_core.parser import Parser
from ozdil_core.vm import VirtualMachine

class TestVMAdvanced(unittest.TestCase):
    def run_vm(self, code):
        tokens = lex_ozdil(code)
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

if __name__ == "__main__":
    unittest.main()
