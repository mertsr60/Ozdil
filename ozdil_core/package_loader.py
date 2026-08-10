# -*- coding: utf-8 -*-
import os
import sys
import json
import re
import socket
import ipaddress
import math
import random
import time
import urllib.parse
import urllib.request
from .errors import OzdilError

# Absolute path resolution for packages
_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_CURRENT_DIR, ".."))
LOCAL_PACKAGES_DIR = os.path.join(_PROJECT_ROOT, "oz_packages")

_PACKAGE_CACHE = {}

_BUILTIN_NAME_MAP = {
    'math': 'matematik', 'matematik': 'matematik',
    'random': 'rastgele', 'rastgele': 'rastgele',
    'time': 'zaman', 'zaman': 'zaman',
    'web': 'web', 'internet': 'web',
    'sistem': 'sistem', 'system': 'sistem',
    'json': 'json',
    'dosya': 'dosya', 'file': 'dosya'
}

_BUILTIN_MODULE_CACHE = {}

def validate_url_for_ssrf(url):
    try:
        parsed = urllib.parse.urlparse(url)
        host = parsed.hostname
        if not host:
            raise ValueError("Geçersiz URL veya sunucu adı bulunamadı.")
        
        host_lower = host.lower()
        if host_lower in ("localhost", "0.0.0.0", "::1"):
            raise ValueError("Yerel adreslere erişim engellendi.")
            
        # Quick syntax checks
        if "localhost" in host_lower or "127.0.0.1" in host_lower:
            raise ValueError("Yerel adreslere erişim engellendi.")
            
        # DNS Rebinding & SSRF Koruması: Hostname IP adreslerini çözümleyip kontrol et
        try:
            # Resolve all IPs (handles both IPv4 and IPv6)
            addr_info = socket.getaddrinfo(host, None)
            for item in addr_info:
                ip_str = item[4][0]
                ip_obj = ipaddress.ip_address(ip_str)
                if (ip_obj.is_loopback or 
                    ip_obj.is_private or 
                    ip_obj.is_link_local or 
                    ip_obj.is_multicast or 
                    ip_obj.is_reserved or 
                    ip_obj.is_unspecified):
                    raise ValueError(f"Erişim engellendi: IP {ip_str} özel, yerel veya geçersiz bir ağ adresidir.")
        except Exception as dns_err:
            if "engellendi" in str(dns_err) or "Erişim engellendi" in str(dns_err):
                raise dns_err
            raise ValueError(f"DNS çözümleme hatası: {str(dns_err)}")
    except Exception as e:
        if "engellendi" in str(e):
            raise RuntimeError(f"Güvenlik Hatası (SSRF): {str(e)}")
        raise RuntimeError(f"URL doğrulama hatası: {str(e)}")

def validate_filepath_for_sandbox(filepath):
    abs_path = os.path.abspath(filepath)
    allowed_root = os.path.abspath(_PROJECT_ROOT)
    if not abs_path.startswith(allowed_root):
        raise PermissionError("Hata: Dosya sisteminde bu dizine erişim güvenlik nedeniyle engellenmiştir!")
    # Block access to sensitive system paths or critical code files
    base_name = os.path.basename(abs_path)
    if base_name in (".env", "config.json", "repository.py", "server.ts", "package.json"):
        raise PermissionError("Hata: Hassas dosyalara erişim güvenlik nedeniyle engellenmiştir!")

def make_restricted_builtins(permissions, stdout_ref):
    import builtins
    
    safe_builtins = {}
    
    # Allowed safe builtin function and class names
    safe_names = [
        'abs', 'all', 'any', 'bin', 'chr', 'divmod', 'enumerate', 'filter', 'hex',
        'id', 'len', 'map', 'max', 'min', 'next', 'oct', 'ord', 'pow', 'repr',
        'reversed', 'round', 'sorted', 'sum', 'zip', 'int', 'float', 'str', 'bool',
        'list', 'dict', 'tuple', 'set', 'frozenset', 'bytes', 'bytearray', 'range',
        'slice', 'object', 'type', 'isinstance', 'issubclass', 'callable'
    ]
    
    # Auto-allow exception classes
    for name in dir(builtins):
        obj = getattr(builtins, name)
        if isinstance(obj, type) and issubclass(obj, BaseException):
            safe_builtins[name] = obj
            
    for name in safe_names:
        if hasattr(builtins, name):
            safe_builtins[name] = getattr(builtins, name)
            
    # Custom print
    safe_builtins['print'] = lambda *args: stdout_ref.append(" ".join(str(x) for x in args) + "\n")
    
    # Sandboxed open()
    if "dosya_sistemi" in permissions:
        def sandboxed_open(file, mode='r', *args, **kwargs):
            validate_filepath_for_sandbox(file)
            if mode not in ('r', 'w', 'a', 'rb', 'wb', 'ab', 'rt', 'wt', 'at'):
                raise ValueError("Geçersiz veya güvensiz dosya açma modu.")
            return builtins.open(file, mode, *args, **kwargs)
        safe_builtins['open'] = sandboxed_open
    else:
        def disabled_open(*args, **kwargs):
            raise PermissionError("Hata: Dosya sistemine erişim izniniz yok. Lütfen 'dosya_sistemi' izni talep edin.")
        safe_builtins['open'] = disabled_open
        
    # Guarded getattr/setattr/hasattr
    def sandboxed_getattr(obj, name, *args):
        if isinstance(name, str) and (name.startswith('_') or '__' in name):
            raise PermissionError(f"Güvenlik İhlali: Gizli veya sistem özniteliklerine erişim yasaktır ('{name}').")
        return getattr(obj, name, *args)
        
    def sandboxed_setattr(obj, name, value):
        if isinstance(name, str) and (name.startswith('_') or '__' in name):
            raise PermissionError(f"Güvenlik İhlali: Gizli veya sistem özniteliklerine müdahale yasaktır ('{name}').")
        setattr(obj, name, value)
        
    def sandboxed_hasattr(obj, name):
        if isinstance(name, str) and (name.startswith('_') or '__' in name):
            return False
        return hasattr(obj, name)
        
    safe_builtins['getattr'] = sandboxed_getattr
    safe_builtins['setattr'] = sandboxed_setattr
    safe_builtins['hasattr'] = sandboxed_hasattr
    
    return safe_builtins

def load_external_package(name, lineno, stdout_ref):
    if name in _PACKAGE_CACHE:
        return _PACKAGE_CACHE[name]
        
    from ozdil.package_manager import verify_package_signature
    from ozdil.sandbox import verify_python_code
    import ozdil.plugin_api
    sys.modules['plugin_api'] = ozdil.plugin_api
    
    package_dirs = [
        os.path.abspath(os.path.expanduser("~/.ozdil/packages")),
        LOCAL_PACKAGES_DIR,
    ]
    
    found_pkg_dir = None
    for pdir in package_dirs:
        potential_dir = os.path.join(pdir, name)
        if os.path.isdir(potential_dir):
            found_pkg_dir = potential_dir
            break
            
    if not found_pkg_dir:
        raise OzdilError(
            "Kütüphane Hatası (ImportError)",
            f"'{name}' kütüphanesi bulunamadı. Lütfen 'ozpip' ile yüklendiğinden veya yerel olarak mevcut olduğundan emin olun.",
            lineno
        )
        
    config_file = os.path.join(found_pkg_dir, "ozpaket.json")
    if not os.path.isfile(config_file):
        raise OzdilError(
            "Kütüphane Hatası (ImportError)",
            f"'{name}' kütüphanesinde 'ozpaket.json' yapılandırma dosyası eksik.",
            lineno
        )
        
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            meta = json.load(f)
    except Exception as e:
        raise OzdilError(
            "Kütüphane Hatası (ImportError)",
            f"'{name}' kütüphanesinin 'ozpaket.json' dosyası okunamadı veya geçersiz JSON: {str(e)}",
            lineno
        )
        
    # 1. Sürüm imza doğrulaması (SHA256)
    sig_ok, sig_msg = verify_package_signature(name)
    if not sig_ok:
        raise OzdilError(
            "Güvenlik Hatası (SignatureError)",
            f"'{name}' kütüphanesi güvenlik/imza testini geçemedi: {sig_msg}",
            lineno
        )
        
    # 1.5. Bağımlılıkları otomatik yükle
    bagimliliklar = meta.get("bagimliliklar", [])
    for dep in bagimliliklar:
        m = re.match(r'^([a-zA-Z0-9_]+)', dep.strip())
        if m:
            dep_name = m.group(1)
            if dep_name not in sys.modules:
                try:
                    load_external_package(dep_name, lineno, stdout_ref)
                except Exception as e:
                    if isinstance(e, OzdilError):
                        raise e
                    raise OzdilError(
                        "Kütüphane Hatası (ImportError)",
                        f"'{name}' kütüphanesinin bağımlılığı olan '{dep_name}' yüklenemedi: {str(e)}",
                        lineno
                    )
        
    pkg_type = meta.get("tur", "ozdil")
    permissions = meta.get("izinler", [])
    
    # Tetikle: paket_yuklendi
    if hasattr(ozdil.plugin_api, "plugin") and hasattr(ozdil.plugin_api.plugin, "trigger_event"):
        ozdil.plugin_api.plugin.trigger_event("paket_yuklendi", name)
    
    if pkg_type == "ozdil":
        entry_file = os.path.join(found_pkg_dir, f"{name}.oz")
        if not os.path.isfile(entry_file):
            entry_file = os.path.join(found_pkg_dir, "main.oz")
            
        if not os.path.isfile(entry_file):
            raise OzdilError(
                "Kütüphane Hatası (ImportError)",
                f"'{name}' kütüphanesinde bir giriş dosyası ('{name}.oz' veya 'main.oz') bulunamadı.",
                lineno
            )
            
        try:
            with open(entry_file, "r", encoding="utf-8") as f:
                code_content = f.read()
        except Exception as e:
            raise OzdilError(
                "Kütüphane Hatası (ImportError)",
                f"'{name}' kütüphanesinin giriş dosyası okunamadı: {str(e)}",
                lineno
            )
            
        try:
            from .lexer import lex_ozdil
            from .parser import Parser
            pkg_tokens = lex_ozdil(code_content)
            pkg_parser = Parser(pkg_tokens)
            pkg_ast = pkg_parser.parse_program()
            
            use_legacy = os.environ.get("OZDIL_USE_LEGACY_INTERPRETER") == "1"
            if use_legacy:
                from .interpreter import Interpreter
                pkg_interpreter = Interpreter()
                pkg_interpreter.stdout = stdout_ref
                pkg_interpreter.eval(pkg_ast, pkg_interpreter.global_env)
                res = pkg_interpreter.global_env.values
            else:
                from .vm import VirtualMachine
                pkg_vm = VirtualMachine(inputs_list=None)
                pkg_vm.stdout = stdout_ref
                pkg_vm.eval(pkg_ast, pkg_vm.global_env)
                res = pkg_vm.global_env.values
                
            _PACKAGE_CACHE[name] = res
            return res
        except Exception as e:
            if isinstance(e, OzdilError):
                raise OzdilError(
                    f"Kütüphane Hatası ({e.friendly_type})",
                    f"'{name}' kütüphanesi yüklenirken hata oluştu (Satır {e.lineno}): {e.message}",
                    lineno
                )
            raise OzdilError(
                "Kütüphane Hatası (ImportError)",
                f"'{name}' kütüphanesi yürütülürken hata: {str(e)}",
                lineno
            )
            
    elif pkg_type == "python":
        entry_file = os.path.join(found_pkg_dir, f"{name}.py")
        if not os.path.isfile(entry_file):
            entry_file = os.path.join(found_pkg_dir, "main.py")
            
        if not os.path.isfile(entry_file):
            raise OzdilError(
                "Kütüphane Hatası (ImportError)",
                f"'{name}' kütüphanesinde Python giriş dosyası ('{name}.py' veya 'main.py') bulunamadı.",
                lineno
            )
            
        try:
            with open(entry_file, "r", encoding="utf-8") as f:
                code_content = f.read()
        except Exception as e:
            raise OzdilError(
                "Kütüphane Hatası (ImportError)",
                f"'{name}' kütüphanesinin Python dosyası okunamadı: {str(e)}",
                lineno
            )
            
        # 2. Gelişmiş AST-tabanlı Python Sandbox Güvenlik Kontrolü
        sandbox_ok, sandbox_errors = verify_python_code(code_content, name, permissions)
        if not sandbox_ok:
            raise OzdilError(
                "Güvenlik Hatası (SecurityError)",
                f"'{name}' Python eklentisi güvenlik süzgecini geçemedi:\n" + "\n".join(sandbox_errors),
                lineno
            )
            
        try:
            # Build heavily restricted and sandboxed __builtins__
            restricted_builtins = make_restricted_builtins(permissions, stdout_ref)
            exec_globals = {
                "__builtins__": restricted_builtins,
                "math": math,
                "random": random,
                "time": time,
                "plugin_api": ozdil.plugin_api
            }
            exec(code_content, exec_globals, exec_globals)
            local_scope = exec_globals
            
            if "plugin" not in local_scope:
                raise OzdilError(
                    "Güvenlik Hatası (PluginError)",
                    f"'{name}' kütüphanesinde 'plugin()' fonksiyonu tanımlanmamış.",
                    lineno
                )
                
            plugin_func = local_scope["plugin"]
            if not callable(plugin_func):
                raise OzdilError(
                    "Güvenlik Hatası (PluginError)",
                    f"'{name}' kütüphanesindeki 'plugin' bir fonksiyon değil.",
                    lineno
                )
                
            plugin_apis = plugin_func()
            if not isinstance(plugin_apis, dict):
                raise OzdilError(
                    "Güvenlik Hatası (PluginError)",
                    f"'{name}' kütüphanesinin 'plugin()' fonksiyonu bir sözlük döndürmeli.",
                    lineno
                )
                
            # Dinamik modül kaydı (diğer modüllerin import edebilmesi için)
            import types
            mod = types.ModuleType(name)
            for k, v in local_scope.items():
                setattr(mod, k, v)
            mod.plugin = plugin_func
            sys.modules[name] = mod
                
            _PACKAGE_CACHE[name] = plugin_apis
            return plugin_apis
        except Exception as e:
            if isinstance(e, OzdilError):
                raise e
            raise OzdilError(
                "Kütüphane Hatası (ImportError)",
                f"'{name}' Python eklentisi yüklenirken hata oluştu: {str(e)}",
                lineno
            )
    else:
        raise OzdilError(
            "Kütüphane Hatası (ImportError)",
            f"'{name}' kütüphanesinin türü ('{pkg_type}') desteklenmiyor. Geçerli türler: 'ozdil', 'python'",
            lineno
        )
