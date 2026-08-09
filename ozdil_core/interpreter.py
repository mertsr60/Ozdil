# -*- coding: utf-8 -*-
import os
import sys
import json
import math
import random
import time
import re

# Absolute path resolution for packages
_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_CURRENT_DIR, ".."))
LOCAL_PACKAGES_DIR = os.path.join(_PROJECT_ROOT, "oz_packages")

from .errors import OzdilError, ReturnException, BreakException, ContinueException, InputRequestException
from .ast_nodes import (
    Program, Atama, Eger, Iken, Dongu, Islem, Dondur, Getir,
    IkiliIslem, TekliIslem, Degisken, Deger, Cagir, Nitelik,
    Endeks, Liste, Sozluk, Ifade, DurNode, DevamEtNode, Sinif, Dene
)
from .environment import Environment

def tr_upper(s):
    res = []
    for char in s:
        if char == 'i': res.append('İ')
        elif char == 'ı': res.append('I')
        else: res.append(char.upper())
    return "".join(res)

def tr_lower(s):
    res = []
    for char in s:
        if char == 'İ': res.append('i')
        elif char == 'I': res.append('ı')
        else: res.append(char.lower())
    return "".join(res)

def bound_method(func, instance):
    def wrapper(*args):
        return func(instance, *args)
    return wrapper

class OzClass:
    def __init__(self, name, methods, interpreter):
        self.name = name
        self.methods = methods
        self.interpreter = interpreter
        
    def __call__(self, *args):
        instance = OzInstance(self)
        init_method = self.methods.get('__init__')
        if init_method:
            bound_init = bound_method(init_method, instance)
            bound_init(*args)
        elif len(args) > 0:
            raise OzdilError("Tür Hatası (TypeError)", f"'{self.name}' sınıfı parametre almıyor.", 1)
        return instance

class OzInstance:
    def __init__(self, klass):
        self.__klass = klass
        self.__dict_attrs = {}
        
    def __getattr__(self, attr):
        if attr in self.__dict_attrs:
            return self.__dict_attrs[attr]
        if attr in self.__klass.methods:
            return bound_method(self.__klass.methods[attr], self)
        raise AttributeError(f"'{self.__klass.name}' nesnesinin '{attr}' adında bir özelliği yok.")
        
    def __setattr__(self, attr, value):
        if attr.startswith('_OzInstance__') or attr.startswith('_OzClass__'):
            super().__setattr__(attr, value)
        else:
            self.__dict_attrs[attr] = value
            
    def __repr__(self):
        return f"<{self.__klass.name} nesnesi>"

_LIST_METHODS = {
    'ekle': 'append', 'append': 'append',
    'çıkar': 'remove', 'cikar': 'remove', 'remove': 'remove',
    'temizle': 'clear', 'clear': 'clear',
    'sırala': 'sort', 'sirala': 'sort', 'sort': 'sort',
    'ters_çevir': 'reverse', 'ters_cevir': 'reverse', 'reverse': 'reverse',
    'bul': 'index', 'index': 'index',
    'say': 'count', 'count': 'count',
    'sil': 'pop', 'pop': 'pop'
}

_DICT_METHODS = {
    'temizle': 'clear', 'clear': 'clear',
    'sil': 'pop', 'pop': 'pop'
}

def get_attribute(obj, attr, lineno):
    if isinstance(obj, list):
        if attr in _LIST_METHODS:
            return getattr(obj, _LIST_METHODS[attr])
        if attr in ('uzunluk', 'len'):
            return lambda: len(obj)
    elif isinstance(obj, dict):
        if attr in _DICT_METHODS:
            return getattr(obj, _DICT_METHODS[attr])
        if attr in ('anahtarlar', 'keys'):
            return lambda: list(obj.keys())
        if attr in ('değerler', 'degerler', 'values'):
            return lambda: list(obj.values())
        if attr in ('çıkar', 'cikar', 'remove'):
            return lambda key: obj.pop(key, None)
    elif isinstance(obj, str):
        if attr in ('büyük_harf', 'buyuk_harf', 'upper'):
            return lambda: tr_upper(obj)
        if attr in ('küçük_harf', 'kucuk_harf', 'lower'):
            return lambda: tr_lower(obj)
            
    if isinstance(obj, dict) and attr in obj:
        return obj[attr]
        
    if hasattr(obj, attr):
        return getattr(obj, attr)
        
    obj_type_name = obj._OzInstance__klass.name if isinstance(obj, OzInstance) else type(obj).__name__
    raise OzdilError(
        "Öznitelik Hatası (AttributeError)",
        f"'{obj_type_name}' nesnesinin '{attr}' adında bir özelliği veya fonksiyonu yok.",
        lineno
    )

def validate_url_for_ssrf(url):
    import urllib.parse
    import socket
    try:
        parsed = urllib.parse.urlparse(url)
        host = parsed.hostname
        if not host:
            raise ValueError("Geçersiz URL veya sunucu adı bulunamadı.")
        
        host_lower = host.lower()
        if host_lower in ("localhost", "127.0.0.1", "0.0.0.0", "::1"):
            raise ValueError("Yerel adreslere erişim engellendi.")
        
        if host_lower.startswith("10.") or host_lower.startswith("192.168.") or host_lower.startswith("169.254."):
            raise ValueError("Özel ağ veya bulut metadata adreslerine erişim engellendi.")
        
        if host_lower.startswith("172."):
            parts = host_lower.split('.')
            if len(parts) >= 2 and parts[1].isdigit():
                sec = int(parts[1])
                if 16 <= sec <= 31:
                    raise ValueError("Özel ağ adreslerine erişim engellendi.")
                    
        # DNS Rebinding & SSRF Koruması: Hostname IP adresini çözümleyip kontrol et
        try:
            ip = socket.gethostbyname(host)
            if ip in ("127.0.0.1", "0.0.0.0"):
                raise ValueError("Yerel IP adreslerine erişim engellendi.")
            if ip.startswith("10.") or ip.startswith("192.168.") or ip.startswith("169.254."):
                raise ValueError("Çözümlenen IP özel veya metadata ağındadır.")
            if ip.startswith("172."):
                parts = ip.split('.')
                if len(parts) >= 2 and parts[1].isdigit():
                    sec = int(parts[1])
                    if 16 <= sec <= 31:
                        raise ValueError("Çözümlenen IP özel ağdadır.")
        except Exception as dns_err:
            if "engellendi" in str(dns_err):
                raise dns_err
    except Exception as e:
        if "engellendi" in str(e):
            raise RuntimeError(f"Güvenlik Hatası (SSRF): {str(e)}")
        raise RuntimeError(f"URL doğrulama hatası: {str(e)}")

def _web_getir(url):
    import urllib.request
    try:
        validate_url_for_ssrf(url)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        raise RuntimeError(f"Web isteği başarısız oldu: {str(e)}")

def _web_gonder(url, data_dict):
    import urllib.request
    import urllib.parse
    try:
        validate_url_for_ssrf(url)
        data_bytes = urllib.parse.urlencode(data_dict).encode('utf-8')
        req = urllib.request.Request(url, data=data_bytes, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        raise RuntimeError(f"Web gönderme isteği başarısız oldu: {str(e)}")

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

def load_external_package(name, lineno, stdout_ref):
    if name in _PACKAGE_CACHE:
        return _PACKAGE_CACHE[name]
        
    import os
    import json
    import re
    import math
    import random
    import time
    
    from ozdil.package_manager import verify_package_signature
    from ozdil.sandbox import verify_python_code
    import ozdil.plugin_api
    import sys
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
        
    # 1.5. Bağımlılıkları otomatik yükle (sys.modules kaydı için)
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
            
            pkg_interpreter = Interpreter()
            pkg_interpreter.stdout = stdout_ref
            
            pkg_interpreter.eval(pkg_ast, pkg_interpreter.global_env)
            res = pkg_interpreter.global_env.values
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
            exec_globals = {
                "__builtins__": __builtins__,
                "print": lambda *args: stdout_ref.append(" ".join(str(x) for x in args) + "\n"),
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

class Interpreter:
    def __init__(self, inputs_list=None):
        self.stdout = []
        self.inputs_list = list(inputs_list) if inputs_list else []
        self.global_env = Environment()
        self.init_builtins()
        
        # O(1) AST nodes to evaluation methods routing table
        self.eval_map = {
            Program: self.eval_Program,
            Ifade: self.eval_Ifade,
            Deger: self.eval_Deger,
            Degisken: self.eval_Degisken,
            Atama: self.eval_Atama,
            Liste: self.eval_Liste,
            Sozluk: self.eval_Sozluk,
            Endeks: self.eval_Endeks,
            Nitelik: self.eval_Nitelik,
            IkiliIslem: self.eval_IkiliIslem,
            TekliIslem: self.eval_TekliIslem,
            Cagir: self.eval_Cagir,
            Eger: self.eval_Eger,
            Iken: self.eval_Iken,
            Dongu: self.eval_Dongu,
            Islem: self.eval_Islem,
            Sinif: self.eval_Sinif,
            Dene: self.eval_Dene,
            Dondur: self.eval_Dondur,
            Getir: self.eval_Getir,
            DurNode: self.eval_DurNode,
            DevamEtNode: self.eval_DevamEtNode
        }
        
    def init_builtins(self):
        def oz_yazdir(*args):
            def tr_val(val):
                if val is True: return "doğru"
                if val is False: return "yanlış"
                if val is None: return "boş"
                if isinstance(val, list):
                    return "[" + ", ".join(tr_val(x) for x in val) + "]"
                if isinstance(val, dict):
                    return "{" + ", ".join(f"{tr_val(k)}: {tr_val(v)}" for k, v in val.items()) + "}"
                return str(val)
            text = " ".join(tr_val(x) for x in args)
            self.stdout.append(text + "\n")
            
        def oz_girdi(prompt=""):
            if self.inputs_list:
                val = str(self.inputs_list.pop(0))
                self.stdout.append(str(prompt) + val + "\n")
                return val
            else:
                raise InputRequestException(str(prompt))
                
        self.global_env.define('yazdır', oz_yazdir)
        self.global_env.define('yazdir', oz_yazdir)
        self.global_env.define('girdi', oz_girdi)
        self.global_env.define('input', oz_girdi)
        self.global_env.define('uzunluk', len)
        
        self.global_env.define('tam_sayı', int)
        self.global_env.define('tam_sayi', int)
        self.global_env.define('ondalık', float)
        self.global_env.define('ondalik', float)
        self.global_env.define('metin', str)
        self.global_env.define('aralık', range)
        self.global_env.define('aralik', range)
        
        # Register math direct calls for convenience/backwards compatibility
        self.global_env.define('karekök', math.sqrt)
        self.global_env.define('karekok', math.sqrt)
        self.global_env.define('faktöriyel', math.factorial)
        self.global_env.define('faktoriyel', math.factorial)
        self.global_env.define('sinüs', math.sin)
        self.global_env.define('sinus', math.sin)
        self.global_env.define('kosinüs', math.cos)
        self.global_env.define('kosinus', math.cos)
        self.global_env.define('tanjant', math.tan)
        self.global_env.define('radyan', math.radians)
        self.global_env.define('derece', math.degrees)
        self.global_env.define('üs', math.pow)
        self.global_env.define('us', math.pow)
        self.global_env.define('mutlak', math.fabs)
        self.global_env.define('aşağı_yuvarla', math.floor)
        self.global_env.define('asagi_yuvarla', math.floor)
        self.global_env.define('yukarı_yuvarla', math.ceil)
        self.global_env.define('yukari_yuvarla', math.ceil)
        self.global_env.define('ebob', math.gcd)
        self.global_env.define('en_buyuk_ortak_bolen', math.gcd)
        self.global_env.define('pi_sayısı', math.pi)
        self.global_env.define('pi_sayisi', math.pi)
        
        # Register random direct calls
        self.global_env.define('ondalık_seç', random.random)
        self.global_env.define('ondalik_sec', random.random)
        self.global_env.define('tamsayı_seç', random.randint)
        self.global_env.define('tamsayi_sec', random.randint)
        self.global_env.define('aralıkta_seç', random.randrange)
        self.global_env.define('aralikta_sec', random.randrange)
        self.global_env.define('seç', random.choice)
        self.global_env.define('sec', random.choice)
        self.global_env.define('karıştır', random.shuffle)
        self.global_env.define('karistir', random.shuffle)
        self.global_env.define('örnek_seç', random.sample)
        self.global_env.define('ornek_sec', random.sample)
        
        # Register time direct calls
        self.global_env.define('bekle', time.sleep)
        self.global_env.define('yerel_zaman', time.localtime)
        self.global_env.define('tarih_saat', time.ctime)

    def eval(self, node, env):
        if node is None:
            return None
        handler = self.eval_map.get(node.__class__)
        if handler:
            return handler(node, env)
        return None

    def eval_Program(self, node, env):
        for stmt in node.body:
            self.eval(stmt, env)
        return None

    def eval_Ifade(self, node, env):
        return self.eval(node.expr, env)

    def eval_Deger(self, node, env):
        return node.value

    def eval_Degisken(self, node, env):
        return env.lookup(node.name, node.lineno)

    def eval_Atama(self, node, env):
        val = self.eval(node.value, env)
        target = node.target
        target_cls = target.__class__
        if target_cls is Degisken:
            env.assign(target.name, val, node.lineno, modifier=node.modifier)
        elif target_cls is Endeks:
            obj = self.eval(target.value, env)
            idx = self.eval(target.index, env)
            try:
                obj[idx] = val
            except Exception as e:
                raise OzdilError("Tür Hatası (TypeError)", f"Endeks ataması başarısız: {str(e)}", node.lineno)
        elif target_cls is Nitelik:
            obj = self.eval(target.value, env)
            attr = target.attr
            try:
                setattr(obj, attr, val)
            except Exception as e:
                raise OzdilError("Öznitelik Hatası (AttributeError)", f"Öznitelik ataması başarısız: {str(e)}", node.lineno)
        else:
            raise OzdilError("Yazım Hatası (SyntaxError)", "Geçersiz atama hedefi.", node.lineno)
        return val

    def eval_Liste(self, node, env):
        return [self.eval(elt, env) for elt in node.elts]

    def eval_Sozluk(self, node, env):
        keys = [self.eval(k, env) for k in node.keys]
        vals = [self.eval(v, env) for v in node.values]
        return dict(zip(keys, vals))

    def eval_Endeks(self, node, env):
        obj = self.eval(node.value, env)
        idx = self.eval(node.index, env)
        try:
            return obj[idx]
        except Exception as e:
            raise OzdilError("Dizin Hatası (IndexError)", f"Sınır dışı erişim veya geçersiz anahtar: {str(e)}", node.lineno)

    def eval_Nitelik(self, node, env):
        obj = self.eval(node.value, env)
        return get_attribute(obj, node.attr, node.lineno)

    def eval_IkiliIslem(self, node, env):
        op = node.op
        left_val = self.eval(node.left, env)
        
        if op == 'veya':
            return left_val or self.eval(node.right, env)
        if op == 've':
            return left_val and self.eval(node.right, env)
            
        right_val = self.eval(node.right, env)
        
        try:
            if op == '+': return left_val + right_val
            if op == '-': return left_val - right_val
            if op == '*': return left_val * right_val
            if op in ('/', '%'):
                if right_val == 0:
                    raise OzdilError("Sıfıra Bölme Hatası (ZeroDivisionError)", "Bir sayı sıfıra bölünemez veya mod alınamaz.", node.lineno)
                if op == '/':
                    return left_val / right_val
                else:
                    return left_val % right_val
            if op == '**': return left_val ** right_val
            if op == '==': return left_val == right_val
            if op == '!=': return left_val != right_val
            if op == '<': return left_val < right_val
            if op == '>': return left_val > right_val
            if op == '<=': return left_val <= right_val
            if op == '>=': return left_val >= right_val
        except Exception as e:
            if isinstance(e, OzdilError):
                raise e
            raise OzdilError("Tür Hatası (TypeError)", f"'{op}' işlemi için uyumsuz veri türleri ({type(left_val).__name__} ve {type(right_val).__name__})", node.lineno)

    def eval_TekliIslem(self, node, env):
        operand_val = self.eval(node.operand, env)
        op = node.op
        try:
            if op == '+': return +operand_val
            if op == '-': return -operand_val
            if op == 'değil': return not operand_val
        except Exception as e:
            raise OzdilError("Tür Hatası (TypeError)", f"'{op}' işlemi için uyumsuz veri türü ({type(operand_val).__name__})", node.lineno)

    def eval_Cagir(self, node, env):
        func = self.eval(node.func, env)
        args = [self.eval(arg, env) for arg in node.args]
        if not callable(func):
            raise OzdilError("Tür Hatası (TypeError)", f"Nesne çağrılabilir bir işlem veya fonksiyon değil.", node.lineno)
        try:
            return func(*args)
        except ReturnException as r:
            return r.value
        except (InputRequestException, BreakException, ContinueException) as ctrl_err:
            raise ctrl_err
        except Exception as e:
            if isinstance(e, OzdilError):
                raise e
            raise OzdilError("Yürütme Hatası (RuntimeError)", f"İşlem yürütülürken hata: {str(e)}", node.lineno, original_exception=e)

    def eval_Eger(self, node, env):
        if self.eval(node.test, env):
            for stmt in node.body:
                self.eval(stmt, env)
        elif node.orelse:
            for stmt in node.orelse:
                self.eval(stmt, env)
        return None

    def eval_Iken(self, node, env):
        while self.eval(node.test, env):
            try:
                for stmt in node.body:
                    self.eval(stmt, env)
            except BreakException:
                break
            except ContinueException:
                continue
        return None

    def eval_Dongu(self, node, env):
        iter_val = self.eval(node.iter_expr, env)
        try:
            iterator = iter(iter_val)
        except TypeError:
            raise OzdilError("Tür Hatası (TypeError)", f"'{type(iter_val).__name__}' nesnesi üzerinde döngü kurulamaz.", node.lineno)
            
        target_name = node.target.name
        for val in iterator:
            env.define(target_name, val)
            try:
                for stmt in node.body:
                    self.eval(stmt, env)
            except BreakException:
                break
            except ContinueException:
                continue
        return None

    def eval_Islem(self, node, env):
        def make_oz_func(fn_node, fn_env):
            num_args = len(fn_node.args)
            fn_name = fn_node.name
            fn_body = fn_node.body
            fn_args = fn_node.args
            fn_lineno = fn_node.lineno
            def oz_func(*args):
                if len(args) != num_args:
                    raise OzdilError("Tür Hatası (TypeError)", f"'{fn_name}' işlemi {num_args} parametre bekliyor, fakat {len(args)} tane verildi.", fn_lineno)
                local_env = Environment(fn_env)
                # Optimize parameter assignments with dictionary update
                local_env.values.update(zip(fn_args, args))
                
                try:
                    for stmt in fn_body:
                        self.eval(stmt, local_env)
                except ReturnException as r:
                    return r.value
                return None
            return oz_func
            
        env.define(node.name, make_oz_func(node, env))
        return None

    def eval_Sinif(self, node, env):
        class_env = Environment(env)
        for stmt in node.body:
            self.eval(stmt, class_env)
        methods = class_env.values
        klass_obj = OzClass(node.name, methods, self)
        env.define(node.name, klass_obj)
        return None

    def eval_Dene(self, node, env):
        try:
            for stmt in node.body:
                self.eval(stmt, env)
        except (ReturnException, BreakException, ContinueException, InputRequestException) as ctrl_err:
            raise ctrl_err
        except Exception as e:
            err_name = ""
            orig_e = e
            if isinstance(e, OzdilError):
                if e.original_exception:
                    orig_e = e.original_exception
                err_name = e.friendly_type
                m = re.search(r'\(([^)]+)\)', err_name)
                if m:
                    err_name = m.group(1)
            else:
                err_name = type(e).__name__
                
            if orig_e:
                err_name = type(orig_e).__name__
                
            handler_found = False
            for err_type, err_var, handler_body in node.handlers:
                if err_type is None or err_type == err_name or (isinstance(e, OzdilError) and err_type in e.friendly_type):
                    handler_found = True
                    local_env = Environment(env)
                    if err_var:
                        local_env.define(err_var, e)
                    for stmt in handler_body:
                        self.eval(stmt, local_env)
                    break
            if not handler_found:
                raise e
        return None

    def eval_Dondur(self, node, env):
        val = self.eval(node.value, env) if node.value else None
        raise ReturnException(val)

    def eval_Getir(self, node, env):
        canonical = _BUILTIN_NAME_MAP.get(node.name)
        if canonical and canonical in _BUILTIN_MODULE_CACHE:
            env.define(node.name, _BUILTIN_MODULE_CACHE[canonical])
            return

        if node.name in ('matematik', 'math'):
            math_ns = {
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
            try:
                import os
                package_dirs = [
                    os.path.abspath(os.path.expanduser("~/.ozdil/packages")),
                    LOCAL_PACKAGES_DIR,
                ]
                found = False
                for pdir in package_dirs:
                    if os.path.isdir(os.path.join(pdir, "matematik")):
                        found = True
                        break
                if found:
                    ext_ns = load_external_package("matematik", node.lineno, self.stdout)
                    for k, v in ext_ns.items():
                        if k not in math_ns:
                            math_ns[k] = v
            except Exception:
                pass
            _BUILTIN_MODULE_CACHE['matematik'] = math_ns
            env.define(node.name, math_ns)
        elif node.name in ('rastgele', 'random'):
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
                characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
                return "".join(random.choice(characters) for _ in range(int(uzunluk)))

            random_ns = {
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
            try:
                import os
                package_dirs = [
                    os.path.abspath(os.path.expanduser("~/.ozdil/packages")),
                    LOCAL_PACKAGES_DIR,
                ]
                found = False
                for pdir in package_dirs:
                    if os.path.isdir(os.path.join(pdir, "rastgele")):
                        found = True
                        break
                if found:
                    ext_ns = load_external_package("rastgele", node.lineno, self.stdout)
                    for k, v in ext_ns.items():
                        if k not in random_ns:
                            random_ns[k] = v
            except Exception:
                pass
            _BUILTIN_MODULE_CACHE['rastgele'] = random_ns
            env.define(node.name, random_ns)
        elif node.name in ('zaman', 'time'):
            def _zaman_damgasi():
                return time.time()
            
            def _bicimlendir(format_str, t=None):
                if t is None:
                    t = time.localtime()
                return time.strftime(format_str, t)

            time_ns = {
                'bekle': time.sleep, 'yerel_zaman': time.localtime, 'tarih_saat': time.ctime,
                'saniye': time.time,
                'zaman_damgası': _zaman_damgasi, 'zaman_damgasi': _zaman_damgasi,
                'biçimlendir': _bicimlendir, 'bicimlendir': _bicimlendir
            }
            _BUILTIN_MODULE_CACHE['zaman'] = time_ns
            env.define(node.name, time_ns)
        elif node.name in ('web', 'internet'):
            web_ns = {
                'getir': _web_getir,
                'gönder': _web_gonder, 'gonder': _web_gonder
            }
            _BUILTIN_MODULE_CACHE['web'] = web_ns
            env.define(node.name, web_ns)
        elif node.name in ('sistem', 'system'):
            sistem_ns = {
                'isim': os.name,
                'platform': sys.platform,
                'argümanlar': sys.argv, 'argumanlar': sys.argv,
                'çevre': dict(os.environ), 'cevre': dict(os.environ),
                'dosya_var_mı': os.path.exists, 'dosya_var_mi': os.path.exists,
                'klasör_yarat': os.makedirs, 'klasor_yarat': os.makedirs
            }
            _BUILTIN_MODULE_CACHE['sistem'] = sistem_ns
            env.define(node.name, sistem_ns)
        elif node.name == 'json':
            json_ns = {
                'çöz': json.loads, 'coz': json.loads,
                'kodla': json.dumps
            }
            _BUILTIN_MODULE_CACHE['json'] = json_ns
            env.define(node.name, json_ns)
        elif node.name in ('dosya', 'file'):
            def _dosya_oku(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return f.read()
            def _dosya_yaz(filepath, content):
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(str(content))
            def _dosya_ekle(filepath, content):
                with open(filepath, 'a', encoding='utf-8') as f:
                    f.write(str(content))
            dosya_ns = {
                'oku': _dosya_oku,
                'yaz': _dosya_yaz,
                'ekle': _dosya_ekle
            }
            _BUILTIN_MODULE_CACHE['dosya'] = dosya_ns
            env.define(node.name, dosya_ns)
        else:
            try:
                pkg_ns = load_external_package(node.name, node.lineno, self.stdout)
                env.define(node.name, pkg_ns)
                
                import ozdil.plugin_api
                for func_name, func_obj in ozdil.plugin_api.plugin.functions.items():
                    env.define(func_name, func_obj)
                for cmd_name, cmd_obj in ozdil.plugin_api.plugin.commands.items():
                    env.define(cmd_name, cmd_obj)
                    
            except OzdilError as oz_err:
                raise oz_err
            except Exception as e:
                raise OzdilError("Kütüphane Hatası (ImportError)", f"'{node.name}' kütüphanesi yüklenirken hata oluştu: {str(e)}", node.lineno)
        return None

    def eval_DurNode(self, node, env):
        raise BreakException()

    def eval_DevamEtNode(self, node, env):
        raise ContinueException()

