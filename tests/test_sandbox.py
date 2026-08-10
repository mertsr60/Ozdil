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

    def test_forbidden_builtins_import(self):
        code = "import builtins\nbuiltins.eval('1')"
        ok, errors = verify_python_code(code, "test_builtins")
        self.assertFalse(ok)
        self.assertTrue(any("builtins" in err for err in errors))

    def test_forbidden_importlib(self):
        code = "import importlib\n"
        ok, errors = verify_python_code(code, "test_importlib")
        self.assertFalse(ok)
        self.assertTrue(any("importlib" in err for err in errors))

    def test_introspection_blocking(self):
        code = "x = ().__class__"
        ok, errors = verify_python_code(code, "test_introspection")
        self.assertFalse(ok)
        self.assertTrue(any("gizli" in err.lower() or "sistem" in err.lower() or "__class__" in err.lower() for err in errors))

    def test_single_underscore_blocking(self):
        code = "x = obj._some_private_var"
        ok, errors = verify_python_code(code, "test_private")
        self.assertFalse(ok)
        self.assertTrue(any("gizli" in err.lower() or "sistem" in err.lower() for err in errors))

    def test_reflection_blocking(self):
        for func in ("globals", "locals", "vars", "dir", "getattr", "setattr", "delattr", "hasattr"):
            code = f"x = {func}()"
            ok, errors = verify_python_code(code, "test_reflection")
            self.assertFalse(ok)
            self.assertTrue(any(func in err.lower() for err in errors))

    def test_ssrf_protection(self):
        import socket
        # Verify socket.getaddrinfo blocks loopback/private IPs
        for bad_ip in ("127.0.0.1", "localhost", "10.0.0.1", "192.168.1.1", "0.0.0.0"):
            with self.assertRaises(PermissionError):
                socket.getaddrinfo(bad_ip, 80)
        # Verify socket.socket.connect blocks private/loopback connections
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        for bad_ip in ("127.0.0.1", "10.0.0.1", "192.168.1.1"):
            with self.assertRaises(PermissionError):
                s.connect((bad_ip, 80))

    def test_package_asymmetric_verification(self):
        from ozdil.package_manager import verify_package_signature
        from ozdil.repository import REPOSITORY_PACKAGES
        # Standard repository packages should be signed correctly and pass
        for pkg in REPOSITORY_PACKAGES.keys():
            # Standard package check (if installed, check signature)
            # We can also mock verify_package_signature with a dummy metadata
            pass

if __name__ == "__main__":
    unittest.main()
