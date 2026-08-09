# -*- coding: utf-8 -*-
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ozdil_core.lexer import lex_ozdil
from ozdil_core.parser import Parser
from ozdil_core.ast_nodes import Program, Atama, Degisken, Deger, IkiliIslem, Eger, Iken

class TestParser(unittest.TestCase):
    def test_simple_assignment(self):
        tokens = lex_ozdil("değişken x = 5")
        parser = Parser(tokens)
        ast_tree = parser.parse_program()
        self.assertIsInstance(ast_tree, Program)
        self.assertEqual(len(ast_tree.body), 1)
        
        stmt = ast_tree.body[0]
        self.assertIsInstance(stmt, Atama)
        self.assertEqual(stmt.target.name, "x")
        self.assertIsInstance(stmt.value, Deger)
        self.assertEqual(stmt.value.value, 5)

    def test_binary_operation(self):
        tokens = lex_ozdil("değişken y = 10 + 20")
        parser = Parser(tokens)
        ast_tree = parser.parse_program()
        stmt = ast_tree.body[0]
        self.assertIsInstance(stmt.value, IkiliIslem)
        self.assertEqual(stmt.value.op, "+")
        self.assertEqual(stmt.value.left.value, 10)
        self.assertEqual(stmt.value.right.value, 20)

    def test_if_statement_parsing(self):
        code = (
            "eger x > 2:\n"
            "    yazdır(10)\n"
        )
        tokens = lex_ozdil(code)
        parser = Parser(tokens)
        ast_tree = parser.parse_program()
        self.assertEqual(len(ast_tree.body), 1)
        stmt = ast_tree.body[0]
        self.assertIsInstance(stmt, Eger)
        self.assertIsInstance(stmt.test, IkiliIslem)
        self.assertEqual(len(stmt.body), 1)

if __name__ == "__main__":
    unittest.main()
