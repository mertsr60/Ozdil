# -*- coding: utf-8 -*-
import os
import sys
import json
import math
import random
import time
import re
import socket
import ipaddress

# Global SSRF protection: Monkey-patch socket resolution and connections to block private/loopback IPs
_original_getaddrinfo = socket.getaddrinfo
_original_connect = socket.socket.connect

def sandboxed_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    if not host:
        return _original_getaddrinfo(host, port, family, type, proto, flags)
    
    host_lower = str(host).lower().strip()
    if host_lower in ("localhost", "0.0.0.0", "::1") or "localhost" in host_lower or "127.0.0.1" in host_lower:
        raise PermissionError("Güvenlik Hatası (SSRF): Yerel ağ adreslerine erişim engellendi.")
        
    res = _original_getaddrinfo(host, port, family, type, proto, flags)
    for item in res:
        ip_str = item[4][0]
        try:
            ip_obj = ipaddress.ip_address(ip_str)
            if (ip_obj.is_loopback or 
                ip_obj.is_private or 
                ip_obj.is_link_local or 
                ip_obj.is_multicast or 
                ip_obj.is_reserved or 
                ip_obj.is_unspecified):
                raise PermissionError(f"Güvenlik Hatası (SSRF): '{ip_str}' özel, yerel veya geçersiz bir ağ adresidir.")
        except ValueError:
            pass
    return res

def sandboxed_connect(self, address):
    if isinstance(address, tuple) and len(address) > 0:
        host = address[0]
        if host:
            try:
                ip_obj = ipaddress.ip_address(host)
                if (ip_obj.is_loopback or 
                    ip_obj.is_private or 
                    ip_obj.is_link_local or 
                    ip_obj.is_multicast or 
                    ip_obj.is_reserved or 
                    ip_obj.is_unspecified):
                    raise PermissionError(f"Güvenlik Hatası (SSRF): '{host}' özel, yerel veya geçersiz bir ağ adresidir.")
            except ValueError:
                pass
    return _original_connect(self, address)

socket.getaddrinfo = sandboxed_getaddrinfo
socket.socket.connect = sandboxed_connect

# Absolute path resolution for packages
_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_CURRENT_DIR, ".."))
LOCAL_PACKAGES_DIR = os.path.join(_PROJECT_ROOT, "varyn_packages")

from .errors import VarynError, ReturnException, BreakException, ContinueException, InputRequestException
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
            raise VarynError("Tür Hatası (TypeError)", f"'{self.name}' sınıfı parametre almıyor.", 1)
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

from .object_model import get_attribute, is_dangerous_attribute
from .capabilities import SecurityContext, Capability, ResourceLimits

from .package_loader import (
    validate_url_for_ssrf,
    validate_filepath_for_sandbox,
    make_restricted_builtins,
    load_external_package,
    get_builtin_module
)

class Interpreter:
    def __init__(self, inputs_list=None, capabilities=None, limits=None, guest_env=None):
        self.stdout = []
        self.inputs_list = list(inputs_list) if inputs_list else []
        self.security_context = SecurityContext(capabilities, limits, guest_env)
        self.package_cache = {}
        self.global_env = Environment()
        self.call_depth = 0
        self.instruction_count = 0
        self.start_time = 0.0
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
        def varyn_yazdir(*args):
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
            
        def varyn_girdi(prompt=""):
            if self.inputs_list:
                val = str(self.inputs_list.pop(0))
                self.stdout.append(str(prompt) + val + "\n")
                return val
            else:
                raise InputRequestException(str(prompt))
                
        self.global_env.define('yazdır', varyn_yazdir)
        self.global_env.define('yazdir', varyn_yazdir)
        self.global_env.define('girdi', varyn_girdi)
        self.global_env.define('input', varyn_girdi)
        self.global_env.define('uzunluk', len)
        
        self.global_env.define('tam_sayı', int)
        self.global_env.define('tam_sayi', int)
        self.global_env.define('ondalık', float)
        self.global_env.define('ondalik', float)
        self.global_env.define('metin', str)
        
        def _safe_range(*args):
            r = range(*args)
            if len(r) > self.security_context.limits.max_collection_size:
                raise VarynError("Kaynak Aşımı Hatası (ResourceExhaustionError)", "Maksimum aralık/liste boyutu aşıldı.", 1)
            return r
            
        self.global_env.define('aralık', _safe_range)
        self.global_env.define('aralik', _safe_range)
        
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
                raise VarynError("Tür Hatası (TypeError)", f"Endeks ataması başarısız: {str(e)}", node.lineno)
        elif target_cls is Nitelik:
            obj = self.eval(target.value, env)
            attr = target.attr
            if is_dangerous_attribute(attr):
                raise VarynError("Öznitelik Hatası (AttributeError)", f"Güvenlik İhlali: '{attr}' özniteliğine atama engellendi.", node.lineno)
            if isinstance(obj, dict):
                obj[attr] = val
            elif hasattr(obj, 'set_attr'):
                obj.set_attr(attr, val)
            elif isinstance(obj, OzInstance):
                obj.set_attr(attr, val)
            else:
                raise VarynError("Öznitelik Hatası (AttributeError)", f"'{type(obj).__name__}' nesnesine öznitelik atanamaz.", node.lineno)
        else:
            raise VarynError("Yazım Hatası (SyntaxError)", "Geçersiz atama hedefi.", node.lineno)
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
            raise VarynError("Dizin Hatası (IndexError)", f"Sınır dışı erişim veya geçersiz anahtar: {str(e)}", node.lineno)

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
                    raise VarynError("Sıfıra Bölme Hatası (ZeroDivisionError)", "Bir sayı sıfıra bölünemez veya mod alınamaz.", node.lineno)
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
            if isinstance(e, VarynError):
                raise e
            raise VarynError("Tür Hatası (TypeError)", f"'{op}' işlemi için uyumsuz veri türleri ({type(left_val).__name__} ve {type(right_val).__name__})", node.lineno)

    def eval_TekliIslem(self, node, env):
        operand_val = self.eval(node.operand, env)
        op = node.op
        try:
            if op == '+': return +operand_val
            if op == '-': return -operand_val
            if op == 'değil': return not operand_val
        except Exception as e:
            raise VarynError("Tür Hatası (TypeError)", f"'{op}' işlemi için uyumsuz veri türü ({type(operand_val).__name__})", node.lineno)

    def eval_Cagir(self, node, env):
        func = self.eval(node.func, env)
        args = [self.eval(arg, env) for arg in node.args]
        if not callable(func):
            raise VarynError("Tür Hatası (TypeError)", f"Nesne çağrılabilir bir işlem veya fonksiyon değil.", node.lineno)
        
        self.call_depth += 1
        if self.call_depth > self.security_context.limits.max_call_depth:
            self.call_depth -= 1
            raise VarynError("Özyineleme Hatası (RecursionError)", f"Maksimum çağrı derinliği ({self.security_context.limits.max_call_depth}) aşıldı!", node.lineno)
            
        try:
            return func(*args)
        except ReturnException as r:
            return r.value
        except (InputRequestException, BreakException, ContinueException) as ctrl_err:
            raise ctrl_err
        except Exception as e:
            if isinstance(e, VarynError):
                raise e
            raise VarynError("Yürütme Hatası (RuntimeError)", f"İşlem yürütülürken hata: {str(e)}", node.lineno, original_exception=e)
        finally:
            self.call_depth -= 1

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
            raise VarynError("Tür Hatası (TypeError)", f"'{type(iter_val).__name__}' nesnesi üzerinde döngü kurulamaz.", node.lineno)
            
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
                    raise VarynError("Tür Hatası (TypeError)", f"'{fn_name}' işlemi {num_args} parametre bekliyor, fakat {len(args)} tane verildi.", fn_lineno)
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
            if isinstance(e, VarynError):
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
                if err_type is None or err_type == err_name or (isinstance(e, VarynError) and err_type in e.friendly_type):
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
        if node.name in self.package_cache:
            env.define(node.name, self.package_cache[node.name])
            return None
            
        try:
            pkg_ns = load_external_package(
                node.name,
                node.lineno,
                self.stdout,
                capabilities=self.security_context.capabilities,
                guest_env=self.security_context.guest_env
            )
            self.package_cache[node.name] = pkg_ns
            env.define(node.name, pkg_ns)
            
            import varyn.plugin_api
            for func_name, func_obj in getattr(varyn.plugin_api.plugin, "functions", {}).items():
                env.define(func_name, func_obj)
            for cmd_name, cmd_obj in getattr(varyn.plugin_api.plugin, "commands", {}).items():
                env.define(cmd_name, cmd_obj)
                
        except VarynError as varyn_err:
            raise varyn_err
        except Exception as e:
            raise VarynError("Kütüphane Hatası (ImportError)", f"'{node.name}' kütüphanesi yüklenirken hata oluştu: {str(e)}", node.lineno)
        return None

    def eval_DurNode(self, node, env):
        raise BreakException()

    def eval_DevamEtNode(self, node, env):
        raise ContinueException()

