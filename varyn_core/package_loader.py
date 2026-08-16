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
import unicodedata
import urllib.parse
import urllib.request
from .errors import VarynError
from .capabilities import Capability, DEFAULT_GUEST_ENV

# Absolute path resolution for packages
_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.realpath(os.path.join(_CURRENT_DIR, ".."))
LOCAL_PACKAGES_DIR = os.path.realpath(os.path.join(_PROJECT_ROOT, "varyn_packages"))

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

# Blocked sensitive files and directories
_SENSITIVE_FILES = {
    '.env', '.env.local', '.env.production', '.env.development',
    'config.json', 'repository.py', 'server.ts', 'package.json',
    'compiler.py', 'tsconfig.json', 'metadata.json', 'bun.lock',
    'vite.config.ts', 'firestore.rules', 'firebase-blueprint.json'
}

_SENSITIVE_EXTENSIONS = ('.key', '.pem', '.secret', '.token', '.env')

def validate_url_for_ssrf(url):
    """
    SSRF and DNS Rebinding protection.
    Blocks localhost, private subnets, loopback, link-local, multicast, metadata endpoints.
    """
    try:
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme not in ('http', 'https'):
            raise ValueError("Sadece HTTP ve HTTPS protokollerine izin verilmektedir.")
            
        host = parsed.hostname
        if not host:
            raise ValueError("Geçersiz URL veya sunucu adı bulunamadı.")
        
        host_lower = host.lower()
        if host_lower in ("localhost", "0.0.0.0", "::1", "127.0.0.1", "169.254.169.254", "metadata.google.internal"):
            raise ValueError("Yerel veya bulut yönetim adreslerine erişim engellendi.")
            
        if "localhost" in host_lower or "127.0.0.1" in host_lower:
            raise ValueError("Yerel adreslere erişim engellendi.")
            
        # DNS Rebinding & SSRF Protection: Resolve and check all IP addresses
        try:
            addr_info = socket.getaddrinfo(host, None)
            for item in addr_info:
                ip_str = item[4][0]
                ip_obj = ipaddress.ip_address(ip_str)
                if (ip_obj.is_loopback or 
                    ip_obj.is_private or 
                    ip_obj.is_link_local or 
                    ip_obj.is_multicast or 
                    ip_obj.is_reserved or 
                    ip_obj.is_unspecified or
                    str(ip_obj) == "169.254.169.254"):
                    raise ValueError(f"Erişim engellendi: IP {ip_str} özel, yerel veya geçersiz bir ağ adresidir.")
        except Exception as dns_err:
            if "engellendi" in str(dns_err) or "Erişim engellendi" in str(dns_err):
                raise dns_err
            raise ValueError(f"DNS çözümleme hatası: {str(dns_err)}")
    except Exception as e:
        if "engellendi" in str(e):
            raise RuntimeError(f"Güvenlik Hatası (SSRF): {str(e)}")
        raise RuntimeError(f"URL doğrulama hatası: {str(e)}")

def validate_filepath_for_sandbox(filepath, mode='r'):
    """
    Filesystem Sandbox Containment.
    Enforces canonical path resolution (realpath), symlink traversal protection,
    strict prefix containment via commonpath, and blocks sensitive files.
    """
    if not isinstance(filepath, str):
        raise TypeError("Dosya yolu metin tipinde olmalıdır.")
        
    # Unicode NFC normalization & null byte prevention
    filepath = unicodedata.normalize('NFC', filepath)
    if '\0' in filepath:
        raise PermissionError("Güvenlik İhlali: Dosya yolunda geçersiz karakter tespit edildi.")
        
    allowed_root = _PROJECT_ROOT
    
    # Resolve real path
    # If the file does not exist yet (e.g. write mode), resolve the parent directory's realpath
    if os.path.exists(filepath) or os.path.islink(filepath):
        resolved_path = os.path.realpath(filepath)
    else:
        parent_dir = os.path.dirname(filepath) or '.'
        resolved_parent = os.path.realpath(parent_dir)
        resolved_path = os.path.join(resolved_parent, os.path.basename(filepath))
        
    # Strict directory containment check
    try:
        common = os.path.commonpath([allowed_root, resolved_path])
        if common != allowed_root:
            raise PermissionError("Hata: Dosya sisteminde bu dizine erişim güvenlik nedeniyle engellenmiştir!")
    except Exception:
        raise PermissionError("Hata: Dosya yolunda geçersiz dizin yapısı tespit edildi!")
        
    # Sibling directory prefix bypass check
    if not (resolved_path == allowed_root or resolved_path.startswith(allowed_root + os.sep)):
        raise PermissionError("Hata: Dosya sisteminde bu dizine erişim güvenlik nedeniyle engellenmiştir!")
        
    # Sensitive file protection
    base_name = os.path.basename(resolved_path)
    if base_name in _SENSITIVE_FILES or base_name.startswith('.env'):
        raise PermissionError("Hata: Hassas yapılandırma dosyalarına erişim güvenlik nedeniyle engellenmiştir!")
        
    for ext in _SENSITIVE_EXTENSIONS:
        if base_name.endswith(ext):
            raise PermissionError("Hata: Güvenlik anahtarı ve kimlik dosyalarına erişim engellenmiştir!")
            
    # Protect Python source code from unauthorized overwrite or read if dangerous
    if mode in ('w', 'a', 'wb', 'ab') and (base_name.endswith('.py') or base_name.endswith('.ts') or base_name.endswith('.json')):
        if base_name in ("package.json", "tsconfig.json", "metadata.json") or base_name.endswith('.py'):
            raise PermissionError("Hata: Sistem ve derleyici dosyalarına yazma erişimi engellenmiştir!")
            
    return resolved_path

def _web_getir(url, headers=None):
    validate_url_for_ssrf(url)
    req = urllib.request.Request(url, headers=headers or {'User-Agent': 'Varyn/1.0'})
    with urllib.request.urlopen(req, timeout=5) as response:
        return response.read().decode('utf-8')

def _web_gonder(url, data, headers=None):
    validate_url_for_ssrf(url)
    if isinstance(data, dict):
        data = json.dumps(data).encode('utf-8')
        if headers is None:
            headers = {}
        headers['Content-Type'] = 'application/json'
    elif isinstance(data, str):
        data = data.encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers or {'User-Agent': 'Varyn/1.0'})
    with urllib.request.urlopen(req, timeout=5) as response:
        return response.read().decode('utf-8')

def get_builtin_module(name, capabilities=None, stdout_ref=None, guest_env=None):
    """
    Returns an isolated dictionary copy of built-in modules for a VM/Interpreter instance.
    Enforces capabilities for sensitive modules (web, dosya, sistem).
    """
    cap_set = capabilities if isinstance(capabilities, set) else set(capabilities or [])
    canonical = _BUILTIN_NAME_MAP.get(name)
    if not canonical:
        return None
        
    if canonical == 'matematik':
        return {
            'karekök': math.sqrt, 'karekok': math.sqrt,
            'faktöriyel': math.factorial, 'faktoriyel': math.factorial,
            'sinüs': math.sin, 'sinus': math.sin,
            'kosinüs': math.cos, 'kosinus': math.cos,
            'tanjant': math.tan,
            'radyan': math.radians,
            'derece': math.degrees,
            'üs': math.pow, 'us': math.pow,
            'mutlak': math.fabs,
            'aşağı_yuvarla': math.floor, 'asagi_yuvarla': math.floor,
            'yukarı_yuvarla': math.ceil, 'yukari_yuvarla': math.ceil,
            'ebob': math.gcd, 'en_buyuk_ortak_bolen': math.gcd,
            'pi_sayısı': math.pi, 'pi_sayisi': math.pi,
            'pi': math.pi, 'e': math.e
        }
    elif canonical == 'rastgele':
        def _rastgele_sayi(min_val, max_val):
            return random.randint(int(min_val), int(max_val))

        def _rastgele_sec(liste):
            if not liste:
                return None
            return random.choice(liste)

        def _rastgele_karistir(liste):
            copied = list(liste)
            random.shuffle(copied)
            return copied

        def _sifre_olustur(uzunluk):
            import secrets
            characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
            return "".join(secrets.choice(characters) for _ in range(int(uzunluk)))

        return {
            'ondalık_seç': random.random, 'ondalik_sec': random.random,
            'tamsayı_seç': random.randint, 'tamsayi_sec': random.randint,
            'aralıkta_seç': random.randrange, 'aralikta_sec': random.randrange,
            'seç': random.choice, 'sec': random.choice,
            'karıştır': random.shuffle, 'karistir': random.shuffle,
            'örnek_seç': random.sample, 'ornek_sec': random.sample,
            'rastgele_sayı': _rastgele_sayi, 'rastgele_sayi': _rastgele_sayi,
            'rastgele_seç': _rastgele_sec, 'rastgele_sec': _rastgele_sec,
            'rastgele_karıştır': _rastgele_karistir, 'rastgele_karistir': _rastgele_karistir,
            'şifre_oluştur': _sifre_olustur, 'sifre_olustur': _sifre_olustur
        }
    elif canonical == 'zaman':
        def _zaman_damgasi():
            return time.time()
            
        def _bicimlendir(format_str, t=None):
            if t is None:
                t = time.localtime()
            return time.strftime(format_str, t)

        return {
            'bekle': time.sleep, 'yerel_zaman': time.localtime, 'tarih_saat': time.ctime,
            'saniye': time.time,
            'zaman_damgası': _zaman_damgasi, 'zaman_damgasi': _zaman_damgasi,
            'biçimlendir': _bicimlendir, 'bicimlendir': _bicimlendir
        }
    elif canonical == 'web':
        if Capability.NETWORK not in cap_set:
            raise VarynError(
                "Yetki Hatası (PermissionError)",
                "Ağ erişimi güvenlik nedeniyle engellendi. 'ag' izni gereklidir.",
                1
            )
        return {
            'getir': _web_getir,
            'gönder': _web_gonder, 'gonder': _web_gonder
        }
    elif canonical == 'sistem':
        # NEVER leak host os.environ or internal process arguments
        env_dict = dict(guest_env or DEFAULT_GUEST_ENV) if (Capability.ENV_VARS in cap_set) else {}
        
        def _dosya_var_mi(filepath):
            if Capability.FILESYSTEM not in cap_set and Capability.FILESYSTEM_READ not in cap_set:
                raise PermissionError("Dosya varlığı kontrolü için 'dosya_sistemi' izni gereklidir.")
            resolved = validate_filepath_for_sandbox(filepath)
            return os.path.exists(resolved)

        def _klasor_yarat(filepath):
            if Capability.FILESYSTEM not in cap_set and Capability.FILESYSTEM_WRITE not in cap_set:
                raise PermissionError("Klasör oluşturma için 'dosya_sistemi' izni gereklidir.")
            resolved = validate_filepath_for_sandbox(filepath, mode='w')
            os.makedirs(resolved, exist_ok=True)
            return True

        return {
            'isim': 'varyn_sandbox',
            'platform': sys.platform,
            'argümanlar': [], 'argumanlar': [],
            'çevre': env_dict, 'cevre': env_dict,
            'dosya_var_mı': _dosya_var_mi, 'dosya_var_mi': _dosya_var_mi,
            'klasör_yarat': _klasor_yarat, 'klasor_yarat': _klasor_yarat
        }
    elif canonical == 'json':
        return {
            'çöz': json.loads, 'coz': json.loads,
            'kodla': json.dumps
        }
    elif canonical == 'dosya':
        if Capability.FILESYSTEM not in cap_set and Capability.FILESYSTEM_READ not in cap_set:
            raise VarynError(
                "Yetki Hatası (PermissionError)",
                "Dosya sistemi erişim izni ('dosya_sistemi') verilmedi.",
                1
            )
            
        def _dosya_oku(filepath):
            resolved = validate_filepath_for_sandbox(filepath, mode='r')
            with open(resolved, 'r', encoding='utf-8') as f:
                return f.read()
                
        def _dosya_yaz(filepath, content):
            if Capability.FILESYSTEM not in cap_set and Capability.FILESYSTEM_WRITE not in cap_set:
                raise PermissionError("Dosya yazma işlemi için 'dosya_sistemi' izni gereklidir.")
            resolved = validate_filepath_for_sandbox(filepath, mode='w')
            with open(resolved, 'w', encoding='utf-8') as f:
                f.write(str(content))
                
        def _dosya_ekle(filepath, content):
            if Capability.FILESYSTEM not in cap_set and Capability.FILESYSTEM_WRITE not in cap_set:
                raise PermissionError("Dosyaya ekleme işlemi için 'dosya_sistemi' izni gereklidir.")
            resolved = validate_filepath_for_sandbox(filepath, mode='a')
            with open(resolved, 'a', encoding='utf-8') as f:
                f.write(str(content))
                
        return {
            'oku': _dosya_oku,
            'yaz': _dosya_yaz,
            'ekle': _dosya_ekle
        }
    return None

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
            resolved = validate_filepath_for_sandbox(file, mode=mode)
            if mode not in ('r', 'w', 'a', 'rb', 'wb', 'ab', 'rt', 'wt', 'at'):
                raise ValueError("Geçersiz veya güvensiz dosya açma modu.")
            return builtins.open(resolved, mode, *args, **kwargs)
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

def load_external_package(name, lineno, stdout_ref, capabilities=None, guest_env=None):
    # Validate package name
    if not isinstance(name, str) or not re.match(r'^[a-zA-Z0-9_-]+$', name):
        raise VarynError(
            "Kütüphane Hatası (ImportError)",
            f"Geçersiz kütüphane adı: '{name}'. Kütüphane isimleri yalnızca harf, rakam ve alt çizgi içerebilir.",
            lineno
        )
        
    # Check built-in modules first
    builtin = get_builtin_module(name, capabilities=capabilities, stdout_ref=stdout_ref, guest_env=guest_env)
    if builtin is not None:
        return builtin

    from varyn.package_manager import verify_package_signature
    from varyn.sandbox import verify_python_code
    import varyn.plugin_api
    sys.modules['plugin_api'] = varyn.plugin_api
    
    package_dirs = [
        os.path.realpath(os.path.expanduser("~/.varyn/packages")),
        LOCAL_PACKAGES_DIR,
    ]
    
    found_pkg_dir = None
    for pdir in package_dirs:
        potential_dir = os.path.join(pdir, name)
        if os.path.isdir(potential_dir):
            # Verify directory containment (prevent symlink / traversal escapes)
            real_pdir = os.path.realpath(pdir)
            real_target = os.path.realpath(potential_dir)
            if os.path.commonpath([real_pdir, real_target]) == real_pdir:
                found_pkg_dir = real_target
                break
            
    if not found_pkg_dir:
        raise VarynError(
            "Kütüphane Hatası (ImportError)",
            f"'{name}' kütüphanesi bulunamadı. Lütfen 'varynpip' ile yüklendiğinden veya yerel olarak mevcut olduğundan emin olun.",
            lineno
        )
        
    config_file = os.path.join(found_pkg_dir, "varynpaket.json")
    if not os.path.isfile(config_file):
        raise VarynError(
            "Kütüphane Hatası (ImportError)",
            f"'{name}' kütüphanesinde 'varynpaket.json' yapılandırma dosyası eksik.",
            lineno
        )
        
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            meta = json.load(f)
    except Exception as e:
        raise VarynError(
            "Kütüphane Hatası (ImportError)",
            f"'{name}' kütüphanesinin 'varynpaket.json' dosyası okunamadı veya geçersiz JSON: {str(e)}",
            lineno
        )
        
    # 1. Signature check
    sig_ok, sig_msg = verify_package_signature(name)
    if not sig_ok:
        raise VarynError(
            "Güvenlik Hatası (SignatureError)",
            f"'{name}' kütüphanesi güvenlik/imza testini geçemedi: {sig_msg}",
            lineno
        )
        
    # 1.5. Automatic dependency loading
    bagimliliklar = meta.get("bagimliliklar", [])
    for dep in bagimliliklar:
        m = re.match(r'^([a-zA-Z0-9_]+)', dep.strip())
        if m:
            dep_name = m.group(1)
            if dep_name not in sys.modules:
                try:
                    load_external_package(dep_name, lineno, stdout_ref, capabilities=capabilities, guest_env=guest_env)
                except Exception as e:
                    if isinstance(e, VarynError):
                        raise e
                    raise VarynError(
                        "Kütüphane Hatası (ImportError)",
                        f"'{name}' kütüphanesinin bağımlılığı olan '{dep_name}' yüklenemedi: {str(e)}",
                        lineno
                    )
        
    pkg_type = meta.get("tur", "varyn")
    permissions = meta.get("izinler", [])
    
    # Event: paket_yuklendi
    if hasattr(varyn.plugin_api, "plugin") and hasattr(varyn.plugin_api.plugin, "trigger_event"):
        varyn.plugin_api.plugin.trigger_event("paket_yuklendi", name)
    
    if pkg_type == "varyn":
        entry_file = os.path.join(found_pkg_dir, f"{name}.varyn")
        if not os.path.isfile(entry_file):
            entry_file = os.path.join(found_pkg_dir, "main.varyn")
            
        if not os.path.isfile(entry_file):
            raise VarynError(
                "Kütüphane Hatası (ImportError)",
                f"'{name}' kütüphanesinde bir giriş dosyası ('{name}.varyn' veya 'main.varyn') bulunamadı.",
                lineno
            )
            
        try:
            with open(entry_file, "r", encoding="utf-8") as f:
                code_content = f.read()
        except Exception as e:
            raise VarynError(
                "Kütüphane Hatası (ImportError)",
                f"'{name}' kütüphanesinin giriş dosyası okunamadı: {str(e)}",
                lineno
            )
            
        try:
            from .lexer import lex_varyn
            from .parser import Parser
            pkg_tokens = lex_varyn(code_content)
            pkg_parser = Parser(pkg_tokens)
            pkg_ast = pkg_parser.parse_program()
            
            use_legacy = os.environ.get("VARYN_USE_LEGACY_INTERPRETER") == "1"
            if use_legacy:
                from .interpreter import Interpreter
                pkg_interpreter = Interpreter(capabilities=capabilities, guest_env=guest_env)
                pkg_interpreter.stdout = stdout_ref
                pkg_interpreter.eval(pkg_ast, pkg_interpreter.global_env)
                res = dict(pkg_interpreter.global_env.values)
            else:
                from .vm import VirtualMachine
                pkg_vm = VirtualMachine(inputs_list=None, capabilities=capabilities, guest_env=guest_env)
                pkg_vm.stdout = stdout_ref
                pkg_vm.eval(pkg_ast, pkg_vm.global_env)
                res = dict(pkg_vm.global_env.values)
                
            return res
        except Exception as e:
            if isinstance(e, VarynError):
                raise VarynError(
                    f"Kütüphane Hatası ({e.friendly_type})",
                    f"'{name}' kütüphanesi yüklenirken hata oluştu (Satır {e.lineno}): {e.message}",
                    lineno
                )
            raise VarynError(
                "Kütüphane Hatası (ImportError)",
                f"'{name}' kütüphanesi yürütülürken hata: {str(e)}",
                lineno
            )
            
    elif pkg_type == "python":
        entry_file = os.path.join(found_pkg_dir, f"{name}.py")
        if not os.path.isfile(entry_file):
            entry_file = os.path.join(found_pkg_dir, "main.py")
            
        if not os.path.isfile(entry_file):
            raise VarynError(
                "Kütüphane Hatası (ImportError)",
                f"'{name}' kütüphanesinde Python giriş dosyası ('{name}.py' veya 'main.py') bulunamadı.",
                lineno
            )
            
        try:
            with open(entry_file, "r", encoding="utf-8") as f:
                code_content = f.read()
        except Exception as e:
            raise VarynError(
                "Kütüphane Hatası (ImportError)",
                f"'{name}' kütüphanesinin Python dosyası okunamadı: {str(e)}",
                lineno
            )
            
        # 2. Strict AST Python Sandbox verification
        sandbox_ok, sandbox_errors = verify_python_code(code_content, name, permissions)
        if not sandbox_ok:
            raise VarynError(
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
                "plugin_api": varyn.plugin_api
            }
            exec(code_content, exec_globals, exec_globals)
            local_scope = exec_globals
            
            if "plugin" not in local_scope:
                raise VarynError(
                    "Güvenlik Hatası (PluginError)",
                    f"'{name}' kütüphanesinde 'plugin()' fonksiyonu tanımlanmamış.",
                    lineno
                )
                
            plugin_func = local_scope["plugin"]
            if not callable(plugin_func):
                raise VarynError(
                    "Güvenlik Hatası (PluginError)",
                    f"'{name}' kütüphanesindeki 'plugin' bir fonksiyon değil.",
                    lineno
                )
                
            plugin_apis = plugin_func()
            if not isinstance(plugin_apis, dict):
                raise VarynError(
                    "Güvenlik Hatası (PluginError)",
                    f"'{name}' kütüphanesinin 'plugin()' fonksiyonu bir sözlük döndürmeli.",
                    lineno
                )
                
            # Dynamic module registration
            import types
            mod = types.ModuleType(name)
            for k, v in local_scope.items():
                setattr(mod, k, v)
            mod.plugin = plugin_func
            sys.modules[name] = mod
                
            return dict(plugin_apis)
        except Exception as e:
            if isinstance(e, VarynError):
                raise e
            raise VarynError(
                "Kütüphane Hatası (ImportError)",
                f"'{name}' Python eklentisi yüklenirken hata oluştu: {str(e)}",
                lineno
            )
    else:
        raise VarynError(
            "Kütüphane Hatası (ImportError)",
            f"'{name}' kütüphanesinin türü ('{pkg_type}') desteklenmiyor. Geçerli türler: 'varyn', 'python'",
            lineno
        )
