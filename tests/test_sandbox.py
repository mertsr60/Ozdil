# -*- coding: utf-8 -*-
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from varyn.sandbox import verify_python_code

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
        from varyn.package_manager import verify_package_signature
        from varyn.repository import REPOSITORY_PACKAGES, generate_sha256
        import tempfile
        import json
        import shutil

        # Create a temporary directory structure for testing package signature
        with tempfile.TemporaryDirectory() as tmpdir:
            pkg_dir = os.path.join(tmpdir, "testpaket")
            os.makedirs(pkg_dir)
            
            # 1. Create files in the package (hashing skips varynpaket.json)
            content = {
                "testpaket.py": "def plugin(): return {}"
            }
            for filename, filecontent in content.items():
                with open(os.path.join(pkg_dir, filename), "w", encoding="utf-8") as f:
                    f.write(filecontent)
                    
            # 2. Sign the package
            expected_imza = generate_sha256(content)
            
            # Let's save the metadata with the signature
            meta_content = {
                "isim": "testpaket",
                "versiyon": "1.0.0",
                "imza": expected_imza
            }
            with open(os.path.join(pkg_dir, "varynpaket.json"), "w", encoding="utf-8") as f:
                json.dump(meta_content, f)
                
            # Now let's mock verify_package_signature's directory lookup to search in our temp directory
            import varyn.package_manager
            original_dirs = varyn.package_manager.LOCAL_PACKAGES_DIR
            
            try:
                # Point package manager's local directory to our temp directory
                varyn.package_manager.LOCAL_PACKAGES_DIR = tmpdir
                
                # Check signature passes
                ok, msg = verify_package_signature("testpaket")
                self.assertTrue(ok, f"Verification failed: {msg}")
                
                # 3. Modify testpaket.py to simulate tampering
                with open(os.path.join(pkg_dir, "testpaket.py"), "w", encoding="utf-8") as f:
                    f.write("def plugin(): return {'tampered': True}")
                    
                # Check signature fails!
                ok, msg = verify_package_signature("testpaket")
                self.assertFalse(ok)
                self.assertIn("Asimetrik imza doğrulaması başarısız oldu", msg)
                
            finally:
                varyn.package_manager.LOCAL_PACKAGES_DIR = original_dirs

    def test_subprocess_sandbox_success(self):
        from varyn.sandbox import run_in_subprocess_sandbox
        code = "print('Hello from isolated subprocess!')"
        ok, out = run_in_subprocess_sandbox(code)
        self.assertTrue(ok)
        self.assertIn("Hello", out)

    def test_subprocess_sandbox_security_blocking(self):
        from varyn.sandbox import run_in_subprocess_sandbox
        # AST blocks import of os
        code = "import os\nos.system('echo test')"
        ok, err = run_in_subprocess_sandbox(code)
        self.assertFalse(ok)
        self.assertIn("AST Süzgeç Hatası", err)

if __name__ == "__main__":
    unittest.main()
