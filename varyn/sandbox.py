# -*- coding: utf-8 -*-
"""
Varyn Python Sandbox Güvenlik Denetleyicisi (sandbox.py)
Bu modül, Python eklentilerinin kaynak kodlarını AST (Soyut Sözdizimi Ağacı) seviyesinde analiz eder,
yasaklı kütüphane içe aktarmalarını, dinamik import'ları, eval/exec çağrılarını ve izinsiz dosya/sistem erişimlerini engeller.
"""

import ast

class SandboxChecker(ast.NodeVisitor):
    def __init__(self, name="bilinmeyen", allowed_permissions=None):
        self.name = name
        self.allowed_permissions = allowed_permissions or []
        self.errors = []
        
        # Yasaklı modüller ve gerekli izinleri
        self.forbidden_modules = {
            "os": "dosya_sistemi",
            "subprocess": "sistem",
            "sys": "sistem",
            "socket": "ag",
            "urllib": "ag",
            "requests": "ag",
            "shutil": "dosya_sistemi",
            "pathlib": "dosya_sistemi",
            "ctypes": "sistem",
            "platform": "sistem",
            "builtins": "sistem",
            "importlib": "sistem",
            "pickle": "sistem",
            "marshal": "sistem",
            "shelve": "sistem",
            "runpy": "sistem",
            "gc": "sistem"
        }

    def check_code(self, code_content):
        """
        Verilen Python kodunu AST ile parse edip ziyaret eder.
        Varsa güvenlik açıklarını hata listesi olarak döndürür.
        """
        try:
            tree = ast.parse(code_content)
            self.visit(tree)
        except SyntaxError as se:
            self.errors.append(f"Yazım Hatası (SyntaxError): {str(se)}")
        return self.errors

    def visit_Import(self, node):
        for alias in node.names:
            base_module = alias.name.split('.')[0]
            if base_module in self.forbidden_modules:
                req_perm = self.forbidden_modules[base_module]
                if req_perm not in self.allowed_permissions:
                    self.errors.append(
                        f"Güvenlik İhlali: '{self.name}' kütüphanesi '{alias.name}' modülünü içe aktarıyor. "
                        f"Bunun için '{req_perm}' izni gereklidir."
                    )
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            base_module = node.module.split('.')[0]
            if base_module in self.forbidden_modules:
                req_perm = self.forbidden_modules[base_module]
                if req_perm not in self.allowed_permissions:
                    self.errors.append(
                        f"Güvenlik İhlali: '{self.name}' kütüphanesi '{node.module}' modülünden içe aktarım yapıyor. "
                        f"Bunun için '{req_perm}' izni gereklidir."
                    )
        self.generic_visit(node)

    def visit_Call(self, node):
        # Fonksiyon çağrılarının analizi
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            
            # eval ve exec engellemesi
            if func_name in ("eval", "exec"):
                self.errors.append(
                    f"Güvenlik İhlali: '{func_name}' fonksiyonunun kullanılması kesinlikle yasaktır."
                )
                
            # Dinamik __import__ engellemesi/izin kontrolü
            elif func_name == "__import__":
                if node.args and isinstance(node.args[0], ast.Constant):
                    imp_val = str(node.args[0].value)
                    base_module = imp_val.split('.')[0]
                    if base_module in self.forbidden_modules:
                        req_perm = self.forbidden_modules[base_module]
                        if req_perm not in self.allowed_permissions:
                            self.errors.append(
                                f"Güvenlik İhlali: Dinamik '__import__' ile '{imp_val}' modülü çağrıldı. "
                                f"Bunun için '{req_perm}' izni gereklidir."
                            )
                else:
                    self.errors.append(
                        "Güvenlik İhlali: Değişken içeren dinamik '__import__' çağrısı engellendi."
                    )
                    
            # open() fonksiyonu dosya sistemi erişimi ister
            elif func_name == "open":
                if "dosya_sistemi" not in self.allowed_permissions:
                    self.errors.append(
                        f"Güvenlik İhlali: Dosya açma/yazma işlemi ('open') için 'dosya_sistemi' izni gereklidir."
                    )

        # Attribute çağrıları: örn. importlib.import_module veya os.system
        elif isinstance(node.func, ast.Attribute):
            full_attr_path = self._get_attribute_path(node.func)
            
            # import_module tespiti
            if "import_module" in full_attr_path:
                if node.args and isinstance(node.args[0], ast.Constant):
                    imp_val = str(node.args[0].value)
                    base_module = imp_val.split('.')[0]
                    if base_module in self.forbidden_modules:
                        req_perm = self.forbidden_modules[base_module]
                        if req_perm not in self.allowed_permissions:
                            self.errors.append(
                                f"Güvenlik İhlali: import_module ile '{imp_val}' modülü çağrıldı. "
                                f"Bunun için '{req_perm}' izni gereklidir."
                            )
                else:
                    self.errors.append(
                        "Güvenlik İhlali: Değişken içeren dinamik 'import_module' çağrısı engellendi."
                    )
            
            # os.system, subprocess.run vb. öznitelik erişimleri
            for forbidden_mod, req_perm in self.forbidden_modules.items():
                if f"{forbidden_mod}." in full_attr_path or full_attr_path.startswith(forbidden_mod):
                    if req_perm not in self.allowed_permissions:
                        self.errors.append(
                            f"Güvenlik İhlali: Yasaklı '{full_attr_path}' çağrısı yapıldı. "
                            f"Bunun için '{req_perm}' izni gereklidir."
                        )

        self.generic_visit(node)

    def visit_Name(self, node):
        if node.id.startswith("__") and node.id != "__init__":
            self.errors.append(f"Güvenlik İhlali: Gizli veya sistem seviyesi nesnelere erişim yasaktır ('{node.id}').")
        elif node.id in ("eval", "exec", "compile", "globals", "locals", "vars", "dir", "getattr", "setattr", "delattr", "hasattr"):
            self.errors.append(f"Güvenlik İhlali: Güvensiz '{node.id}' kelimesinin kullanımı yasaktır.")
        self.generic_visit(node)

    def visit_Attribute(self, node):
        if node.attr.startswith("_") and node.attr != "__init__":
            self.errors.append(f"Güvenlik İhlali: Gizli veya sistem seviyesi özniteliklere erişim yasaktır ('{node.attr}').")
        elif node.attr in ("eval", "exec", "compile", "globals", "locals", "vars", "dir", "getattr", "setattr", "delattr", "hasattr"):
            self.errors.append(f"Güvenlik İhlali: Güvensiz '{node.attr}' özniteliğine erişim yasaktır.")
        self.generic_visit(node)

    def visit_Constant(self, node):
        if isinstance(node.value, str):
            val_lower = node.value.lower()
            for forbidden in ("__builtins__", "__globals__", "__subclasses__", "__code__"):
                if forbidden in val_lower:
                    self.errors.append(f"Güvenlik İhlali: Gizli öznitelik veya sistem kelimesi kullanımı yasaktır ('{forbidden}').")
        self.generic_visit(node)

    def _get_attribute_path(self, node):
        parts = []
        curr = node
        while isinstance(curr, ast.Attribute):
            parts.append(curr.attr)
            curr = curr.value
        if isinstance(curr, ast.Name):
            parts.append(curr.id)
        return ".".join(reversed(parts))


def verify_python_code(code_content, package_name="bilinmeyen", allowed_permissions=None):
    """
    Python kodunu tamamen güvenli sandbox süzgecinden geçirir.
    Hata yoksa True ve boş liste döner, varsa False ve hata listesini döner.
    """
    checker = SandboxChecker(package_name, allowed_permissions)
    errors = checker.check_code(code_content)
    if errors:
        return False, errors
    return True, []

def run_in_subprocess_sandbox(code_content, timeout_sec=2, max_mem_mb=128, allowed_permissions=None):
    """
    Python kodunu tamamen izole edilmiş bir alt süreçte (subprocess) çalıştırır.
    Süreç seviyesinde CPU, bellek, dosya tanımlayıcı (FD) ve süreç oluşturma sınırları koyar.
    """
    import subprocess
    import sys
    import json
    
    # Python code wrapper to run the target code under restricted globals/builtins
    # We serialize the execution and retrieve stdout/stderr
    wrapper_code = f"""
import sys
import json
import resource

def set_limits():
    # CPU Sınırı (saniye)
    resource.setrlimit(resource.RLIMIT_CPU, ({timeout_sec}, {timeout_sec} + 1))
    # Bellek Sınırı (Byte)
    mem_bytes = {max_mem_mb} * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (mem_bytes, mem_bytes))
    # Süreç oluşturma sınırı (0 -> yeni process oluşturamaz, fork/exec engellenir)
    if "sistem" not in {allowed_permissions or []}:
        try:
            resource.setrlimit(resource.RLIMIT_NPROC, (0, 0))
        except Exception:
            pass
    # Açık dosya sayısı sınırı (örn: 20)
    if "dosya_sistemi" not in {allowed_permissions or []}:
        try:
            resource.setrlimit(resource.RLIMIT_NOFILE, (20, 20))
        except Exception:
            pass

try:
    set_limits()
except Exception as e:
    # Bazı ortamlarda bazı limitler kısıtlanamayabilir, hata vermeden devam et
    pass

# Hedef kodu güvenli şekilde çalıştır
try:
    # AST kontrolü
    from varyn.sandbox import verify_python_code
    code_to_run = {repr(code_content)}
    ok, errors = verify_python_code(code_to_run, "subprocess_sandbox", {allowed_permissions})
    if not ok:
        print(json.dumps({{"success": False, "error": "AST Süzgeç Hatası: " + ", ".join(errors)}}))
        sys.exit(0)
        
    # Restricted builtins ve global alan oluştur
    from varyn_core.package_loader import make_restricted_builtins
    import math, random, time
    stdout_ref = []
    restricted_builtins = make_restricted_builtins({allowed_permissions or []}, stdout_ref)
    
    exec_globals = {{
        "__builtins__": restricted_builtins,
        "math": math,
        "random": random,
        "time": time
    }}
    
    exec(code_to_run, exec_globals, exec_globals)
    print(json.dumps({{"success": True, "output": "".join(stdout_ref), "error": None}}))
except Exception as e:
    print(json.dumps({{"success": False, "error": str(e)}}))
"""

    try:
        proc = subprocess.Popen(
            [sys.executable, "-c", wrapper_code],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        try:
            stdout, stderr = proc.communicate(timeout=timeout_sec + 1)
        except subprocess.TimeoutExpired:
            proc.kill()
            stdout, stderr = proc.communicate()
            return False, "Süre Aşımı: Kod çalışması belirlenen süreyi aştı."
            
        if proc.returncode != 0:
            # Process crashed (e.g. killed by SIGSEGV or RLIMIT_AS exceeded)
            if proc.returncode == -9 or proc.returncode == -15:
                return False, "Süreç Aşımı veya Bellek Sınırı: Kod işletilirken sistem tarafından sonlandırıldı."
            return False, f"Alt Süreç Hatası (Exit Code: {proc.returncode}): {stderr.strip() or 'Bellek veya kaynak sınırları aşıldı.'}"
            
        try:
            res = json.loads(stdout.strip())
            if res.get("success"):
                return True, res.get("output")
            else:
                return False, res.get("error")
        except Exception:
            return False, f"Çıktı çözümlenemedi. StdOut: {stdout.strip()} StdErr: {stderr.strip()}"
    except Exception as e:
        return False, f"Sandbox başlatılamadı: {str(e)}"

