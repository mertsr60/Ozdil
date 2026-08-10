# -*- coding: utf-8 -*-
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ozdil_core.lexer import lex_ozdil
from ozdil_core.parser import Parser
from ozdil_core.interpreter import Interpreter
from ozdil_core.vm import VirtualMachine

class TestInterpreter(unittest.TestCase):
    def run_and_compare(self, code, expected_outputs):
        tokens = lex_ozdil(code)
        parser = Parser(tokens)
        ast_tree = parser.parse_program()
        
        # 1. Run CPython / AST Interpreter Backend
        interpreter = Interpreter()
        interpreter.eval(ast_tree, interpreter.global_env)
        self.assertEqual(interpreter.stdout, expected_outputs, "CPython interpreter backend output mismatch")
        
        # 2. Run Custom Bytecode VM Backend
        vm = VirtualMachine()
        vm.eval(ast_tree, vm.global_env)
        self.assertEqual(vm.stdout, expected_outputs, "Custom Bytecode VM backend output mismatch")

    def test_simple_program(self):
        code = (
            "değişken x = 5\n"
            "değişken y = 10\n"
            "yazdır(x + y)\n"
        )
        self.run_and_compare(code, ["15\n"])

    def test_variable_reassignment(self):
        code = (
            "değişken x = 3\n"
            "x = 7\n"
            "yazdır(x)\n"
        )
        self.run_and_compare(code, ["7\n"])

    def test_conditional_execution(self):
        code = (
            "değişken a = 20\n"
            "eger a > 10:\n"
            "    yazdır(\"buyuk\")\n"
            "degilse:\n"
            "    yazdır(\"kucuk\")\n"
        )
        self.run_and_compare(code, ["buyuk\n"])

    def test_lexical_scoping_and_closure(self):
        code = (
            "değişken x = 100\n"
            "islem dis_fonk():\n"
            "    değişken x = 50\n"
            "    islem ic_fonk():\n"
            "        yazdır(x)\n"
            "    ic_fonk()\n"
            "dis_fonk()\n"
            "yazdır(x)\n"
        )
        self.run_and_compare(code, ["50\n", "100\n"])

if __name__ == "__main__":
    unittest.main()
