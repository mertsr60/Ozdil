# -*- coding: utf-8 -*-
"""
ÖzDil Python Sandbox Güvenlik Denetleyicisi (sandbox.py)
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
            "platform": "sistem"
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
