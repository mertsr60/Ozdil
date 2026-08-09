# -*- coding: utf-8 -*-
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ozdil.sandbox import verify_python_code

class TestSandbox(unittest.TestCase):
    def test_safe_code(self):
        code = (
            "def topla(a, b):\n"
            "    return a + b\n"
        )
        ok, errors = verify_python_code(code, "test_safe")
        self.assertTrue(ok)
        self.assertEqual(len(errors), 0)

    def test_forbidden_module(self):
        code = (
            "import os\n"
            "os.system('ls')\n"
        )
        ok, errors = verify_python_code(code, "test_os")
        self.assertFalse(ok)
        self.assertTrue(any("os" in err for err in errors))

    def test_eval_exec_blocking(self):
        code = "eval('2+2')"
        ok, errors = verify_python_code(code, "test_eval")
        self.assertFalse(ok)
        self.assertTrue(any("eval" in err for err in errors))

if __name__ == "__main__":
    unittest.main()
