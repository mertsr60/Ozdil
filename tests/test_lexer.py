# -*- coding: utf-8 -*-
import unittest
import sys
import os

# Add root folder to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ozdil_core.lexer import tokenize_line, lex_ozdil
from ozdil_core.tokens import Token

class TestLexer(unittest.TestCase):
    def test_keywords_and_ids(self):
        # test keyword vs identifier
        tokens = tokenize_line("yazdır eger degilse x", 1)
        self.assertEqual(len(tokens), 4)
        self.assertEqual(tokens[0].type, 'ID')
        self.assertEqual(tokens[0].value, 'yazdır')
        self.assertEqual(tokens[1].type, 'KEYWORD')
        self.assertEqual(tokens[1].value, 'eger')
        self.assertEqual(tokens[2].type, 'KEYWORD')
        self.assertEqual(tokens[2].value, 'degilse')
        self.assertEqual(tokens[3].type, 'ID')
        self.assertEqual(tokens[3].value, 'x')

    def test_numbers(self):
        tokens = tokenize_line("123 45.67", 1)
        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].type, 'NUM_INT')
        self.assertEqual(tokens[0].value, '123')
        self.assertEqual(tokens[1].type, 'NUM_FLOAT')
        self.assertEqual(tokens[1].value, '45.67')

    def test_strings(self):
        tokens = tokenize_line('"merhaba" \'dunya\'', 1)
        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].type, 'STRING')
        self.assertEqual(tokens[0].value, '"merhaba"')
        self.assertEqual(tokens[1].type, 'STRING')
        self.assertEqual(tokens[1].value, "'dunya'")

    def test_operators(self):
        tokens = tokenize_line("== != <= >= + - * /", 1)
        ops = [t.value for t in tokens]
        self.assertEqual(ops, ["==", "!=", "<=", ">=", "+", "-", "*", "/"])

if __name__ == "__main__":
    unittest.main()
